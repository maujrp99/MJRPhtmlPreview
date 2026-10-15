#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-14 · fonte b714d244 · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""
product_structure_check.py - can the Control Center show this product? Reads a project the way the Control Center
reads it and says, per screen, what it cannot render: the judge of the `product-structure` catalog item.

Born 2026-10-14 19:57 (decision of the MJRP, critical): in the fin-control the epics were right (11 `^EP-`, 70 stories
with `epic:`) but there was no `^REL-` and no `planned_for:`, so the Control Center Board - built by release - came out
empty; the catalog did not see it (`releases@1` only asks that some `^REL` exists, and in ROADMAP.md OR the PRD, while
the Control Center reads releases only from ROADMAP.md). Nothing compared a child with what the screen needs.

The readers below mirror the Control Center's own parsers (apps/control-center/src/control_center/adapters/repo_fs/:
roadmap.py, prd.py, requirements.py, features.py, uat.py, mdtext.py) and its rules (rules/graph.py: the story status, the
"n de m" tally; modules/tracking/delivery.py: the release of a feature and of a UAT round). They are copied, not
imported: this script is harness core (stdlib only, ADR-0015) and is vendored into every child, where the Control
Center does not exist. A test of the Control Center (tests/adapters/test_product_structure_pin.py) pins these readers
to the real parsers on the Control Center itself and on the harness root: change a parser there and that test fails
until this file follows.

What is a gap (each with file:line and the owner skill):
  - outcomes (ROADMAP.md): the file, its format, at least one outcome, each in Now/Next/Later, with its measure
    (`- **Medida:**` in its own `###` section - the only way the screen shows it) and its `tags::`; a declared
    `contributes_to::` that the screen would not resolve (rules/contribution.py: the target is the ROADMAP.md of a
    project with a contract, inside the same repository, not the roadmap itself, holds that `^OUT-xx` block - a `^REL`
    is not one - and the edges close no cycle);
  - releases: at least one `^REL-xx` in ROADMAP.md (a release only in the PRD never reaches the screen), and each one
    with at least one story that counts (a release with none shows "sem stories": either it has stories or it is not a
    release yet - the human's call);
  - epics (docs/specs/prd.md): the file, its format, at least one epic, each serving (`serves::`) an outcome that exists;
  - stories (docs/specs/requirements/): every node readable; every story that is not Deferred or Cancelled has an
    `epic:` that is an epic of the PRD and a `planned_for:` that is a release of ROADMAP.md (the epic's own
    `planned_for` does not reach the screen); a transversal NFR (`type: nfr`, `NFR-xx`) has neither, by the
    requirements-graph rule, and is only counted;
  - features (docs/specs/features/Fxx-*/): spec.md and tasks.md readable; a normal feature imports stories that exist
    and land in a release, a Fix feature (`track: Fix`) names UAT issues (`fixes:`) whose round lands in a release (a
    feature with no `track:` is read as normal - listed in the counts; the `feature-track` item asks for the key);
  - UAT (docs/specs/uat.md): readable, in uat@2 (the Gravidade column), each round's release name is a release.
A file that is not valid UTF-8 is a gap naming the file (the screen cannot read it), never an exit 2.
It also prints the counts the screen shows ("n de m" per release, epic and outcome; "sem release").

Usage:
  python3 mjrp-scripts/product_structure_check.py <project> [--json] [--quiet]
Exit: 0 every view renders · 1 gaps (listed) · 2 not evaluable (no project, no contract, not a code-app).
A feature with an open branch is read in the working tree here (the screen reads it at the branch head).
"""
import json
import os
import re
import sys
from pathlib import Path

# ------------------------------------------------------------------ owners ----------------------------------------
OWNER_PM = "mjrp-coaching-pm"
OWNER_REQS = "mjrp-writing-reqs"
OWNER_SDD = "mjrp-specifying-sdd-artifacts"

ROADMAP_FILE = "ROADMAP.md"
PRD_FILE = "docs/specs/prd.md"
REQUIREMENTS_DIR = "docs/specs/requirements"
FEATURES_DIR = "docs/specs/features"
UAT_FILE = "docs/specs/uat.md"
CONTRACT_FILE = ".mjrp-project.yml"

# ------------------------------------------------------------------ mdtext.py (mirror) ------------------------------
_MD_MARKER = re.compile(r"\^(?:[A-Z]+-)?(?:OUT|REL|EP)-\d+")
_MD_KIND = re.compile(r"\bkind::\s*\w+")


def flat(text):
    return re.sub(r"\s+", " ", text).strip()


def plain(text):
    text = _MD_KIND.sub("", _MD_MARKER.sub("", text))
    text = text.replace("**", "").replace("`", "")
    return flat(text).strip("* ").strip()


def table_cells(line):
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|") and not body.endswith("\\|"):
        body = body[:-1]
    cells, current, in_code = [], [], False
    chars = iter(range(len(body)))
    for i in chars:
        ch = body[i]
        if ch == "`":
            in_code = not in_code
        if ch == "\\" and body[i + 1:i + 2] == "|":
            current.append("|")
            next(chars, None)
        elif ch == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    cells.append("".join(current).strip())
    return cells


def is_separator(line):
    cells = table_cells(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells)


class FormatError(ValueError):
    """A file the screen cannot read: the line and the reason (the Control Center's `failed` read)."""

    def __init__(self, line, reason, file=None):
        super().__init__(reason)
        self.line, self.reason, self.file = line, reason, file


# ------------------------------------------------------------------ roadmap.py (mirror) -----------------------------
TITLE_LIMIT = 160
_PREFIX = r"(?:[A-Z]+-)?"
_ANY_MARKER = re.compile(rf"\^{_PREFIX}(?:OUT|REL)-\d+")
_OUT_END = re.compile(rf"\^(?P<id>{_PREFIX}OUT-\d+)\s*$")
_REL_END = re.compile(rf"^(?P<text>.*?)\s*\^(?P<id>{_PREFIX}REL-\d+)\s*$")
_CONTRIBUTES = re.compile(r"^contributes_to::\s*\[\[(?P<target>[^\]|]+)(?:\|[^\]]*)?\]\]")
_BULLET = re.compile(r"^- ")
_LABELED = re.compile(r"^- \*\*(?P<label>.+?)\*\*(?P<rest>.*)$")
_HORIZON = re.compile(r"(Now|Next|Later)\b")
_FIELD_LABELS = ("quem sente", "problema", "hoje", "medida", "sinal", "solução", "opções")


def _horizon(*headings):
    for heading in headings:
        found = _HORIZON.match(heading or "")
        if found:
            return found[1]
    return None


def _road_sections(lines):
    blocks, h2, h3, start = [], None, None, 0
    for i, line in enumerate(lines):
        if line.startswith(("## ", "### ")):
            blocks.append((h2, h3, start, i))
            start = i
            if line.startswith("## "):
                h2, h3 = line[3:].strip(), None
            else:
                h3 = line[4:].strip()
    blocks.append((h2, h3, start, len(lines)))
    return blocks


def _unit_start(lines, end, floor):
    i = end
    while i > floor and lines[i].strip() and not _BULLET.match(lines[i]):
        if not lines[i - 1].strip() or lines[i - 1].startswith("#"):
            break
        i -= 1
    return i


def _fields(lines):
    found = {}
    for i, line in enumerate(lines):
        match = _LABELED.match(line)
        if not match:
            continue
        label = plain(match["label"]).rstrip(":").casefold()
        parts = [match["rest"]]
        for follow in lines[i + 1:]:
            if not follow.strip() or _BULLET.match(follow):
                break
            parts.append(follow)
        found.setdefault(label, plain(" ".join(parts)).lstrip(":").strip())
    return found


def _pick(fields, *names):
    for name in names:
        for label, text in fields.items():
            if label.startswith(name) and text:
                return text
    return None


def parse_roadmap(text):
    """{"outcomes": [...], "releases": [...]} as the Control Center reads them, plus the line of each marker.
    Raises FormatError when the screen would show the roadmap as `failed/unsupported_format`."""
    lines = text.splitlines()
    marked = [i for i, line in enumerate(lines, 1) if _ANY_MARKER.search(line)]
    if not marked:
        raise FormatError(1, "sem marcadores ^OUT-xx / ^REL-xx")
    outcomes = {}
    for h2, h3, first, last in _road_sections(lines):
        block = lines[first:last]
        ends = [(i, _OUT_END.search(lines[i])) for i in range(first, last)]
        ends = [(i, m) for i, m in ends if m]
        single = len(ends) == 1 and h3 is not None
        fields = _fields(block) if single else {}
        tags = re.findall(r"#([\w-]+)", next((x for x in block if x.startswith("tags::")), ""))
        contributes = next((m["target"].strip() for m in map(_CONTRIBUTES.match, block) if m), None)
        for i, match in ends:
            if match["id"] in outcomes:
                continue
            unit = flat(" ".join(lines[_unit_start(lines, i, first):i + 1]))
            labeled = _LABELED.match(unit)
            is_field = bool(labeled) and plain(labeled["label"]).rstrip(":").casefold().startswith(_FIELD_LABELS)
            bare = re.sub(r"^[-*]\s+(?:\[[ xX]\]\s*)?", "", unit)
            title = h3 if (single and is_field) else plain(bare)[:TITLE_LIMIT]
            outcomes[match["id"]] = {
                "id": match["id"], "horizon": _horizon(h3, h2), "title": plain(title or match["id"]),
                "who": _pick(fields, "quem sente"), "problem": _pick(fields, "problema", "hoje"),
                "measure": _pick(fields, "medida", "sinal"), "tags": list(tags if single else ()),
                "contributes_to": contributes if single else None, "line": i + 1, "single": single,
            }
    releases = {}
    for number, line in enumerate(lines, 1):
        match = _REL_END.match(line)
        if not match or match["id"] in releases:
            continue
        body = re.sub(r"^[-*]\s*", "", match["text"])
        named = re.match(r"\*\*(?P<name>.+?)\*\*\s*[—–-]?\s*(?P<desc>.*)$", body)
        name, desc = (named["name"], named["desc"]) if named else (body, "")
        releases[match["id"]] = {"id": match["id"], "name": plain(name) or match["id"], "desc": plain(desc) or None,
                                 "line": number}
    if not outcomes and not releases:
        raise FormatError(marked[0], "marcador ^OUT-xx / ^REL-xx fora do fim da linha")
    return {"outcomes": list(outcomes.values()), "releases": list(releases.values())}


# ------------------------------------------------------------------ prd.py (mirror) ---------------------------------
INTAKE_EPIC = "EP-90"
_ROW_BOLD = re.compile(rf"^\*\*(?P<id>{_PREFIX}EP-\d+)\s*·\s*(?P<name>[^*]+?)\*\*")
_ROW_ID = re.compile(rf"^(?P<id>{_PREFIX}EP-\d+)\b")
_SECTION = re.compile(rf"^### (?P<id>{_PREFIX}EP-\d+)\s*·\s*(?P<name>.+?)\s*$")
_OUT = re.compile(rf"\^({_PREFIX}OUT-\d+)")


def _column(header, *names):
    for index, cell in enumerate(header):
        if plain(cell).casefold().startswith(names):
            return index
    return None


def _cell(cells, index):
    if index is None or index >= len(cells):
        return None
    return plain(cells[index]) or None


def _tables(lines):
    found, i = [], 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and is_separator(lines[i + 1]):
            rows, j = [], i + 2
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                rows.append((j + 1, table_cells(lines[j])))
                j += 1
            found.append((i + 1, table_cells(lines[i]), rows))
            i = j
        else:
            i += 1
    return found


def parse_prd(text):
    """{"epics": [{id, name, outcomes, exit_criterion, declared, line}]} as the Control Center reads them.
    Raises FormatError where the screen would show `failed/unsupported_format`."""
    lines = text.splitlines()
    table = {}
    for number, header, rows in _tables(lines):
        if not plain(header[0]).casefold().startswith(("epic", "épico", "epico")):
            continue
        state, exit_ = _column(header, "estado", "status"), _column(header, "critério", "criterio")
        placed = 0
        for row_number, cells in rows:
            first = cells[0] if cells else ""
            bold, bare = _ROW_BOLD.match(first), _ROW_ID.match(first)
            if bold:
                eid, name = bold["id"], plain(bold["name"])
            elif bare and len(cells) > 1:
                eid, name = bare["id"], plain(cells[1])
            else:
                raise FormatError(row_number, "linha da tabela de épicos sem `EP-xx`")
            placed += 1
            if eid != INTAKE_EPIC:
                table[eid] = {"name": name, "exit": _cell(cells, exit_), "declared": _cell(cells, state), "line": row_number}
        if not placed:
            raise FormatError(number, "tabela de épicos sem nenhuma linha")
    sections = {}
    for i, line in enumerate(lines):
        match = _SECTION.match(line)
        if not match:
            continue
        serves = ()
        for follow in lines[i + 1:]:
            if follow.startswith("#"):
                break
            if follow.startswith("serves::"):
                serves = tuple(dict.fromkeys(_OUT.findall(follow)))
                break
        sections[match["id"]] = (plain(match["name"]), serves, i + 1)
    epics = []
    for eid in dict.fromkeys([*table, *(k for k in sections if k != INTAKE_EPIC)]):
        row = table.get(eid)
        name, serves, sline = sections.get(eid, (row["name"] if row else eid, (), None))
        epics.append({"id": eid, "name": row["name"] if row else name, "outcomes": list(serves),
                      "exit_criterion": row["exit"] if row else None, "declared": row["declared"] if row else None,
                      "line": sline or (row["line"] if row else 1), "has_section": sline is not None})
    return {"epics": epics}


# ------------------------------------------------------------------ requirements.py (mirror) --------------------------
INDEX_NAME = "folder-index.md"
_KEY = re.compile(r"^(?P<key>[A-Za-z_][\w-]*):(?:[ \t]+(?P<value>.*))?$")
_COMMENT = re.compile(r"\s+#.*$")
_EPIC = re.compile(rf"\^({_PREFIX}EP-\d+)")
_RELEASE = re.compile(rf"\^({_PREFIX}REL-\d+)")
_NFR_ID = re.compile(r"^(?:[A-Z]{2,}-)?NFR-\d+$")   # a transversal NFR: no epic, no release (the requirements-graph rule)


def _scalar(raw):
    value = _COMMENT.sub("", (raw or "").strip()).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value or None


def parse_frontmatter(text):
    """(keys -> raw value, continuations, the line of each key). Raises FormatError as the Control Center does."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FormatError(1, "sem frontmatter (a primeira linha deveria ser ---)")
    found, more, at, key = {}, {}, {}, ""
    for number, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return found, {k: "\n".join(v) for k, v in more.items()}, at
        if not line.strip() or line.startswith("#"):
            continue
        if line.startswith((" ", "\t", "-")):
            more.setdefault(key, []).append(line.strip())
            continue
        match = _KEY.match(line.rstrip())
        if not match:
            raise FormatError(number, "linha do frontmatter que não é chave: valor")
        key = match["key"]
        found[key] = match["value"]
        at[key] = number
    raise FormatError(len(lines), "frontmatter sem a linha --- de fechamento")


def parse_node(text, path):
    fields, more, at = parse_frontmatter(text)
    node_id, status = _scalar(fields.get("id")), _scalar(fields.get("status"))
    if not node_id:
        raise FormatError(1, "frontmatter sem id")
    if not status:
        raise FormatError(1, "frontmatter sem status")

    def whole(key):
        return f"{fields.get(key) or ''}\n{more.get(key, '')}"

    first = lambda rx, t: (rx.search(t) or [None, None])[1]  # noqa: E731
    return {"id": node_id, "status": status, "epic": first(_EPIC, whole("epic")),
            "nfr": _scalar(fields.get("type")) == "nfr" or bool(_NFR_ID.match(node_id)),
            "release": first(_RELEASE, whole("planned_for")), "path": path,
            "has_epic_key": "epic" in fields, "has_planned_key": "planned_for" in fields,
            "epic_line": at.get("epic", 1), "planned_line": at.get("planned_for", at.get("epic", 1))}


def read_nodes(root):
    """[node] or raises FormatError(file=...) - one unreadable node fails the whole reading, as on the screen.
    None when the folder does not exist (the screen: "sem grafo")."""
    folder = Path(root) / REQUIREMENTS_DIR
    if not folder.is_dir():
        return None
    nodes = []
    for file in sorted(folder.rglob("*.md")):
        if file.name == INDEX_NAME:
            continue
        rel = file.relative_to(root).as_posix()
        try:
            nodes.append(parse_node(file.read_text(encoding="utf-8"), rel))
        except FormatError as exc:
            exc.file = rel
            raise
        except UnicodeDecodeError:
            raise FormatError(1, "o arquivo não é UTF-8 válido", rel)
        except OSError:
            raise FormatError(1, "não foi possível ler", rel)
    return nodes


# ------------------------------------------------------------------ rules/graph.py (mirror) ---------------------------
_STORY_WORDS = {
    "backlog": "backlog", "prioritized": "prioritized", "ready": "ready",
    "in progress": "doing", "done": "done", "accepted": "accepted", "deferred": "deferred",
    "cancelled": "cancelled", "canceled": "cancelled",
}
OFF_TRACK = ("deferred", "cancelled")


def story_status(raw):
    text = raw.casefold()
    for word in sorted(_STORY_WORDS, key=len, reverse=True):
        if re.search(rf"\b{word}\b", text):
            return _STORY_WORDS[word]
    return "backlog"


def tally(statuses):
    """(done, live): "n de m" on the screen - Done+Accepted over everything but Deferred and Cancelled."""
    return sum(s in ("done", "accepted") for s in statuses), sum(s not in OFF_TRACK for s in statuses)


# ------------------------------------------------------------------ features.py + uat.py (mirror) ---------------------
_FOLDER = re.compile(r"^(?P<id>F\d{2,})-[a-z0-9-]+$")
_LINK = re.compile(r"\[\[(?P<id>(?:S|UC|EA)-\d+)[^\]]*\]\]")
_UAT_ID = re.compile(r"UAT-\d+")
_BOX = re.compile(r"^- \[(?P<x>[ xX])\]")


def feature_front(text, file):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise FormatError(1, "sem frontmatter", file)
    out, at = {}, {}
    for number, line in enumerate(lines[1:], start=2):
        if line.strip() == "---":
            return out, at
        if ":" not in line:
            raise FormatError(number, "linha do frontmatter sem chave", file)
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
        at[key.strip()] = number
    raise FormatError(1, "frontmatter sem fim", file)


def tasks_seen(text, file):
    inside = seen = False
    done = total = 0
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.startswith(("## Implementation", "## Verification"))
            seen = seen or inside
            continue
        box = _BOX.match(line) if inside else None
        if box:
            total += 1
            done += box.group("x") != " "
    if not seen:
        raise FormatError(1, "sem seção ## Implementation nem ## Verification", file)
    return done, total


def read_feature(root, folder):
    """{id, folder, imports, track, fixes, has_track, line} or a FormatError (the card shows the failure)."""
    base = Path(root) / FEATURES_DIR / folder
    spec, tasks = base / "spec.md", base / "tasks.md"
    rel_spec = f"{FEATURES_DIR}/{folder}/spec.md"
    rel_tasks = f"{FEATURES_DIR}/{folder}/tasks.md"

    def text_of(path, rel):
        try:
            return path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise FormatError(1, "o arquivo não é UTF-8 válido", rel)

    front, at = feature_front(text_of(spec, rel_spec), rel_spec) if spec.is_file() else ({}, {})
    if tasks.is_file():
        tasks_seen(text_of(tasks, rel_tasks), rel_tasks)
    return {"id": _FOLDER.match(folder)["id"], "folder": folder, "spec": rel_spec, "spec_exists": spec.is_file(),
            "imports": [m["id"] for m in _LINK.finditer(front.get("imports", ""))],
            "track": "fix" if front.get("track", "").casefold() == "fix" else "normal",
            "has_track": bool(front.get("track", "").strip()), "fixes": _UAT_ID.findall(front.get("fixes", "")),
            "imports_line": at.get("imports", 1), "fixes_line": at.get("fixes", 1)}


_ROUND = re.compile(r"^## Rodada (?P<n>\d+)\s+—\s+(?P<release>[^·(]+?)\s*(?:[·(].*)?$")
_HEAD_V1 = ["ID", "Contexto", "Tipo", "Reportado em", "Descrição", "Status", "OK do humano"]
_HEAD_V2 = ["ID", "Contexto", "Tipo", "Gravidade", "Reportado em", "Descrição", "Status", "OK do humano"]
_SEVERITY = re.compile(r"^P[012]$")
_FIXING = re.compile(r"^fixing\s*\((?P<f>F\d{2,})\)")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _uat_cells(line):
    return [p.strip() for p in re.split(r"(?<!\\)\|", line)[1:-1]]


def _uat_state(status, human_ok):
    if _DATE.search(human_ok):
        return "closed", None
    fixing = _FIXING.match(status)
    if fixing:
        return "fixing", fixing.group("f")
    for word in ("fixed", "open"):
        if status.startswith(word):
            return word, None
    raise ValueError("Status fora da gramática")


def parse_uat(text):
    """{"format", "rows": [{id, round, release_name, state, feature, line, round_line}], "header": bool}."""
    fmt, rows, round_n, release, round_line, header = None, [], 0, None, None, False
    for number, line in enumerate(text.splitlines(), start=1):
        found = _ROUND.match(line)
        if found:
            round_n, release, round_line = int(found.group("n")), found.group("release").strip(), number
            continue
        if line.startswith("| ID "):
            head = _uat_cells(line + " |") if not line.rstrip().endswith("|") else _uat_cells(line)
            fmt = "uat@2" if head == _HEAD_V2 else "uat@1" if head == _HEAD_V1 else None
            header = True
            if fmt is None:
                raise FormatError(number, "cabeçalho da tabela desconhecido")
            continue
        if not line.startswith("| UAT-"):
            continue
        cells = _uat_cells(line)
        want = 8 if fmt == "uat@2" else 7
        if fmt is None or len(cells) < want:
            raise FormatError(number, "linha fora do formato")
        if fmt == "uat@1":
            cells = [*cells[:3], "—", *cells[3:]]
        ident, _context, _kind, severity, _reported, _text, status, human = cells[:8]
        if severity != "—" and not _SEVERITY.match(severity):
            raise FormatError(number, "Gravidade fora de P0 · P1 · P2 · —")
        try:
            state, feature = _uat_state(status, human)
        except ValueError as exc:
            raise FormatError(number, str(exc))
        rows.append({"id": ident, "round": round_n, "release_name": release, "state": state, "feature": feature,
                     "line": number, "round_line": round_line})
    return {"format": fmt or "uat@2", "rows": rows, "header": header}


def feature_release(feature, by_id, uat_rows, releases):
    """modules/tracking/delivery.py `_release_of`: the release a feature card lands in - the one most of its stories
    (a normal feature) or of its UAT issues' rounds (a Fix) sit in. A tie is left to the screen's set order; here the
    smallest id, so the output is stable (the pin test never feeds a tie)."""
    if feature["track"] == "fix":
        found = [release_id(uat_rows[i]["release_name"], releases) for i in feature["fixes"] if i in uat_rows]
    else:
        found = [by_id[s]["release"] for s in feature["imports"] if s in by_id]
    known = [r for r in found if r]
    return max(sorted(set(known)), key=known.count) if known else None


def release_id(name, releases):
    """modules/tracking/delivery.py: the round's release (`1.0`) as an id - by name, by the start of a name, or by id."""
    if not name:
        return None
    for r in releases:
        if r["name"] == name or r["name"].startswith(f"{name} ") or r["id"] == name:
            return r["id"]
    return None


# ------------------------------------------------------------------ the check -------------------------------------------

class Report:
    def __init__(self, root):
        self.root, self.gaps, self.counts = Path(root), [], {}

    def gap(self, view, file, line, message, owner):
        self.gaps.append({"view": view, "file": file, "line": line, "message": message, "owner": owner})


BAD = object()      # a file that is there but is not valid UTF-8 (the gap is already reported; callers skip it)


def _read(root, rel, report=None, view="", owner=""):
    """The text of a project file; None when absent; BAD (plus a gap, when a report is given) when it is not valid UTF-8."""
    p = Path(root) / rel
    if not p.is_file():
        return None
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        if report is not None:
            report.gap(view, rel, 1, "o arquivo não é UTF-8 válido: a tela não o lê (regrave-o em UTF-8)", owner)
        return BAD


def _profile(root):
    text = _read(root, CONTRACT_FILE)
    if text is None:
        return None
    m = re.search(r"^  profile:\s*['\"]?([\w-]+)", text, re.M)
    return m.group(1) if m else ""


# ---- rules/contribution.py + usecases/contributions.py (mirror): what a declared `contributes_to::` resolves to ----------
_TARGET = re.compile(r"^(?P<path>[^#]*)#\^(?P<id>[A-Za-z][A-Za-z0-9-]*)\s*$")


def _repository_of(folder):
    """The repository a project belongs to (ADR-0020 A.4): the root of the repository when the project is nested below it
    and that root has a contract; any other project is its own repository."""
    here = Path(os.path.normpath(folder))
    if (here / ".git").exists():
        return here
    for parent in here.parents:
        if (parent / ".git").exists():
            return parent if (parent / CONTRACT_FILE).is_file() else here
    return here


def resolve_contribution(road_file, raw):
    """(kind, reason, (target file, outcome id) | None) - `rules/contribution.resolve` over the files on disk:
    resolved · missing (bare_id, own_roadmap, no_block) · unreachable (not_a_roadmap, outside_repository, unreadable)."""
    text = raw.strip()
    found = _TARGET.match(text)
    path, oid = ((found["path"].strip() or None, found["id"]) if found else (None, text.lstrip("#^").strip() or None))
    if path is None or oid is None:
        return "missing", "bare_id", None            # never falls back to the local graph
    joined = os.path.normpath(os.path.join(os.path.dirname(road_file), path))
    target = joined if os.path.splitext(joined)[1] else joined + ".md"
    if target == os.path.normpath(road_file):
        return "missing", "own_roadmap", None
    file = Path(target)
    if file.name != ROADMAP_FILE or not file.is_file() or not (file.parent / CONTRACT_FILE).is_file():
        return "unreachable", "not_a_roadmap", None
    if _repository_of(file.parent) != _repository_of(Path(road_file).parent):
        return "unreachable", "outside_repository", None
    try:
        road = parse_roadmap(file.read_text(encoding="utf-8"))
    except (FormatError, OSError, UnicodeDecodeError):
        return "unreachable", "unreadable", None
    if oid not in {o["id"] for o in road["outcomes"]}:
        return "missing", "no_block", None            # a `^REL` (or any block that is not an outcome) lands here
    return "resolved", None, (target, oid)


def _next_hop(node):
    """The (file, outcome) the outcome `node` contributes to, or None (it declares none, or it does not resolve)."""
    file, oid = node
    try:
        road = parse_roadmap(Path(file).read_text(encoding="utf-8"))
    except (FormatError, OSError, UnicodeDecodeError):
        return None
    doc = next((o for o in road["outcomes"] if o["id"] == oid), None)
    if not doc or not doc["contributes_to"]:
        return None
    kind, _why, target = resolve_contribution(file, doc["contributes_to"])
    return target if kind == "resolved" else None


def contribution_in_cycle(road_file, oid):
    """Does the outcome sit on a `contributes_to` cycle? (`rules/contribution.in_cycle`: each outcome has one target.)"""
    start = (os.path.normpath(road_file), oid)
    here, seen = _next_hop(start), set()
    while here is not None and here not in seen:
        if here == start:
            return True
        seen.add(here)
        here = _next_hop(here)
    return False


_CONTRIBUTION_WHY = {
    "bare_id": "alvo sem caminho (`[[<caminho>/ROADMAP#^OUT-xx]]`)",
    "own_roadmap": "o alvo é o próprio ROADMAP",
    "not_a_roadmap": "o alvo não existe ou não é o ROADMAP.md de um projeto com contrato (`.mjrp-project.yml` ao lado)",
    "outside_repository": "o alvo está fora deste repositório",
    "unreadable": "o ROADMAP do alvo não é legível",
    "no_block": "o alvo não tem esse resultado `^OUT-xx` (um `^REL` ou outro bloco não vale)",
    "cycle": "as arestas `contributes_to::` fecham um ciclo",
}


def check(root):
    """The Report of a code-app project. Raises FileNotFoundError / ValueError for "not evaluable"."""
    root = Path(root)
    r = Report(root)

    # ---- ROADMAP: outcomes and releases (Product, Release pages)
    outcomes, releases, road_ok = [], [], False
    road_text = _read(root, ROADMAP_FILE, r, "Produto", OWNER_PM)
    if road_text is BAD:
        pass
    elif road_text is None:
        r.gap("Produto", ROADMAP_FILE, 0, "ROADMAP.md ausente: a tela não tem resultados nem releases", OWNER_PM)
    else:
        try:
            road = parse_roadmap(road_text)
            outcomes, releases, road_ok = road["outcomes"], road["releases"], True
        except FormatError as e:
            r.gap("Produto", ROADMAP_FILE, e.line, f"a tela não lê o ROADMAP ({e.reason})", OWNER_PM)
    if road_ok:
        if not outcomes:
            r.gap("Produto", ROADMAP_FILE, 1, "nenhum resultado `^OUT-xx` no fim de uma linha", OWNER_PM)
        for o in outcomes:
            where = f"{o['id']} ({o['title'][:60]})"
            if o["horizon"] is None:
                r.gap("Produto", ROADMAP_FILE, o["line"], f"{where} fora de `## Now`/`## Next`/`## Later`: aparece em \"sem horizonte\"", OWNER_PM)
            if not o["single"]:
                r.gap("Produto", ROADMAP_FILE, o["line"], f"{where} não está sozinho numa seção `###`: a tela não lê a medida nem as tags dele", OWNER_PM)
                continue
            if not o["measure"]:
                r.gap("Produto", ROADMAP_FILE, o["line"], f"{where} sem medida: escreva `- **Medida:** <hoje → alvo> ^{o['id']}` na seção dele", OWNER_PM)
            if not o["tags"]:
                r.gap("Produto", ROADMAP_FILE, o["line"], f"{where} sem `tags::` (1 a 3) na seção dele", OWNER_PM)
            if o["contributes_to"]:
                kind, why, _target = resolve_contribution(root / ROADMAP_FILE, o["contributes_to"])
                if kind == "resolved" and contribution_in_cycle(root / ROADMAP_FILE, o["id"]):
                    kind, why = "missing", "cycle"
                if kind != "resolved":
                    r.gap("Produto", ROADMAP_FILE, o["line"], f"{where}: `contributes_to::` não chega ao alvo — {_CONTRIBUTION_WHY[why]}", OWNER_PM)
        if not releases:
            prd_peek = _read(root, PRD_FILE)
            in_prd = re.search(rf"\^{_PREFIX}REL-\d+", prd_peek if isinstance(prd_peek, str) else "")
            r.gap("Releases", ROADMAP_FILE, 1, "nenhum release `^REL-xx` no ROADMAP.md" +
                  (" (há `^REL` no PRD, mas a tela lê releases só do ROADMAP.md)" if in_prd else "") +
                  ": o Board por release fica vazio", OWNER_PM)
    rel_ids = {x["id"] for x in releases}
    out_ids = {x["id"] for x in outcomes}

    # ---- PRD: epics (Product, Epic pages)
    epics, prd_ok = [], False
    prd_text = _read(root, PRD_FILE, r, "Épicos", OWNER_PM)
    if prd_text is BAD:
        prd_text = None
    elif prd_text is None:
        r.gap("Épicos", PRD_FILE, 0, "docs/specs/prd.md ausente: a tela não tem épicos", OWNER_PM)
    else:
        try:
            epics, prd_ok = parse_prd(prd_text)["epics"], True
        except FormatError as e:
            r.gap("Épicos", PRD_FILE, e.line, f"a tela não lê o PRD ({e.reason})", OWNER_PM)
    if prd_ok:
        if not epics:
            r.gap("Épicos", PRD_FILE, 1, "nenhum épico (`### EP-xx · nome` com `serves::`)", OWNER_PM)
        for e in epics:
            if not e["outcomes"]:
                why = "sem a seção `### " + e["id"] + " · nome`" if not e["has_section"] else "sem `serves:: [[ROADMAP#^OUT-xx]]`"
                r.gap("Épicos", PRD_FILE, e["line"], f"{e['id']} {why}: aparece solto, fora de todo resultado", OWNER_PM)
            elif road_ok:
                for o in e["outcomes"]:
                    if o not in out_ids:
                        r.gap("Épicos", PRD_FILE, e["line"], f"{e['id']} serve {o}, que não existe no ROADMAP.md", OWNER_PM)
    epic_ids = {e["id"] for e in epics}

    # ---- requirements: the stories (Board, Release, Epic pages)
    nodes = None
    try:
        nodes = read_nodes(root)
        if nodes is None:
            r.gap("Board", REQUIREMENTS_DIR, 0, "sem grafo de requisitos (`docs/specs/requirements/`): a tela mostra o projeto \"sem grafo\"", OWNER_REQS)
        elif not nodes:
            r.gap("Board", REQUIREMENTS_DIR, 0, "nenhum requisito em `docs/specs/requirements/`", OWNER_REQS)
    except FormatError as e:
        r.gap("Board", e.file, e.line, f"a tela não lê os requisitos: {e.reason} (um nó ilegível derruba a leitura inteira)", OWNER_REQS)
        nodes = None
    epic_planned = set()
    if prd_text:
        for m in re.finditer(rf"^### ({_PREFIX}EP-\d+)[^\n]*\n(?:(?!#)[^\n]*\n)*?planned_for::", prd_text, re.M):
            epic_planned.add(m.group(1))
    for n in nodes or ():
        st = story_status(n["status"])
        if st in OFF_TRACK or n["nfr"]:
            continue
        if n["epic"] is None:
            r.gap("Board", n["path"], n["epic_line"], f"{n['id']} sem `epic: \"[[prd#^EP-xx]]\"`: fica fora de todo épico", OWNER_REQS)
        elif prd_ok and n["epic"] not in epic_ids:
            r.gap("Board", n["path"], n["epic_line"], f"{n['id']}: o épico {n['epic']} não existe no PRD", OWNER_REQS)
        if n["release"] is None:
            hint = " (o `planned_for` do épico não chega à tela)" if n["epic"] in epic_planned else ""
            r.gap("Board", n["path"], n["planned_line"], f"{n['id']} sem `planned_for: \"[[ROADMAP#^REL-xx]]\"`: cai em \"sem release\", fora do Board{hint} — que release é decisão do humano", OWNER_REQS)
        elif road_ok and n["release"] not in rel_ids:
            r.gap("Board", n["path"], n["planned_line"], f"{n['id']}: o release {n['release']} não existe no ROADMAP.md: a story some do Board", OWNER_REQS)

    # ---- features (Delivery board)
    by_id = {n["id"]: n for n in nodes or ()}
    uat_rows, uat = {}, None
    uat_text = _read(root, UAT_FILE, r, "Delivery", OWNER_SDD)
    if isinstance(uat_text, str):
        try:
            uat = parse_uat(uat_text)
            uat_rows = {x["id"]: x for x in uat["rows"]}
        except FormatError as e:
            r.gap("Delivery", UAT_FILE, e.line, f"a tela não lê o uat.md ({e.reason})", OWNER_SDD)
    fdir = root / FEATURES_DIR
    folders = sorted(p.name for p in fdir.iterdir() if p.is_dir() and _FOLDER.match(p.name)) if fdir.is_dir() else []
    no_track, landed = [], {}
    for folder in folders:
        try:
            f = read_feature(root, folder)
        except FormatError as e:
            r.gap("Delivery", e.file, e.line, f"{folder}: o card mostra a falha — {e.reason}", OWNER_SDD)
            continue
        except (OSError, UnicodeDecodeError):
            r.gap("Delivery", f"{FEATURES_DIR}/{folder}", 0, f"{folder}: não foi possível ler", OWNER_SDD)
            continue
        if not f["spec_exists"]:
            r.gap("Delivery", f["spec"], 0, f"{f['id']} sem spec.md: o card não tem stories nem trilha", OWNER_SDD)
            continue
        if not f["has_track"]:
            no_track.append(f["id"])       # the screen reads it as a normal feature: the `feature-track` item asks for it
        if f["track"] == "fix":
            if not f["fixes"]:
                r.gap("Delivery", f["spec"], f["fixes_line"], f"{f['id']} é Fix e não diz que issues corrige (`fixes: [UAT-xx]`)", OWNER_SDD)
            found = []
            for i in f["fixes"]:
                if uat is not None and i not in uat_rows:
                    r.gap("Delivery", f["spec"], f["fixes_line"], f"{f['id']}: {i} não está no uat.md", OWNER_SDD)
                elif i in uat_rows:
                    found.append(release_id(uat_rows[i]["release_name"], releases))
        else:
            if not f["imports"]:
                r.gap("Delivery", f["spec"], f["imports_line"], f"{f['id']} não importa nenhuma story (`imports: [\"[[S-xx-slug]]\"]`): o card fica sem release", OWNER_SDD)
            missing = [s for s in f["imports"] if s not in by_id]
            if nodes is not None and missing:
                r.gap("Delivery", f["spec"], f["imports_line"], f"{f['id']} importa story que não existe: {', '.join(missing[:5])}", OWNER_SDD)
            found = [by_id[s]["release"] for s in f["imports"] if s in by_id]
        landed[f["id"]] = feature_release(f, by_id, uat_rows, releases)
        known = [x for x in found if x and x in rel_ids]
        judged = nodes is not None if f["track"] == "normal" else uat is not None
        if (f["imports"] if f["track"] == "normal" else f["fixes"]) and judged and not known and road_ok:
            r.gap("Delivery", f["spec"], f["fixes_line"] if f["track"] == "fix" else f["imports_line"],
                  f"{f['id']}: nenhuma das stories ou issues dela está num release: o card cai no quadro sem release", OWNER_SDD)
    if uat is not None:
        if uat["header"] and uat["format"] == "uat@1":
            r.gap("Delivery", UAT_FILE, 1, "uat.md em uat@1 (sem a coluna Gravidade): a tela não mostra a gravidade", OWNER_SDD)
        lost = {}
        for row in uat["rows"]:
            if release_id(row["release_name"], releases) is None:
                lost.setdefault((row["round_line"], row["release_name"]), []).append(row["id"])
        for (line, name), ids in lost.items():
            what = f"a rodada \"{name}\" não é o nome de um release do ROADMAP.md" if name else "issues fora de uma `## Rodada <n> — <release>`"
            r.gap("Delivery", UAT_FILE, line or 1, f"{what}: {len(ids)} issue(s) no quadro sem release ({', '.join(ids[:4])})", OWNER_SDD)

    # ---- the counts the screen shows
    if nodes is not None:
        statuses = {n["id"]: story_status(n["status"]) for n in nodes}
        rel_counts = []
        for x in releases:
            mine = [statuses[n["id"]] for n in nodes if n["release"] == x["id"]]
            d, live = tally(mine)
            rel_counts.append({"id": x["id"], "name": x["name"], "done": d, "of": live})
            if not live:
                r.gap("Releases", ROADMAP_FILE, x["line"], f"{x['id']} ({x['name']}) sem nenhuma story que conte: o Board e a tela da release ficam \"sem stories\" — "
                      "ou ela ganha stories (`planned_for:`), ou ainda não é release (decisão do humano)", OWNER_PM)
        loose = [statuses[n["id"]] for n in nodes if n["release"] is None]
        d, live = tally(loose)
        epic_counts = []
        for e in epics:
            mine = [statuses[n["id"]] for n in nodes if n["epic"] == e["id"]]
            ed, elive = tally(mine)
            epic_counts.append({"id": e["id"], "done": ed, "of": elive})
        out_counts = []
        for o in outcomes:
            serving = {e["id"] for e in epics if o["id"] in e["outcomes"]}
            mine = [statuses[n["id"]] for n in nodes if n["epic"] in serving]
            od, olive = tally(mine)
            out_counts.append({"id": o["id"], "done": od, "of": olive})
        r.counts = {"stories": len(nodes), "releases": rel_counts,
                    "no_release": {"stories": len(loose), "done": d, "of": live,
                                   "shown": bool(releases) and bool(loose)},
                    "epics": epic_counts, "outcomes": out_counts,
                    "off_track": sum(s in OFF_TRACK for s in statuses.values()),
                    "nfr": sum(1 for n in nodes if n["nfr"])}
    by_release = {}
    for fid, rel in landed.items():
        by_release.setdefault(rel if rel in rel_ids else None, []).append(fid)
    r.counts["features"] = {"total": len(folders), "no_track": no_track, "by_release": by_release}
    return r


def render(r, name):
    out = []
    for g in r.gaps:
        loc = f"{g['file']}:{g['line']}" if g["line"] else g["file"]
        out.append(f"  [{g['view']}] {loc}: {g['message']} → {g['owner']}")
    c = r.counts
    if c.get("releases") is not None:
        out.append("")
        nfr = f"; {c['nfr']} NFR transversais, sem épico nem release por regra" if c.get("nfr") else ""
        out.append(f"  Como a tela conta ({c['stories']} nós; {c['off_track']} Deferred/Cancelled fora do progresso{nfr}):")
        for x in c["releases"]:
            out.append(f"    release {x['id']} · {x['name']}: {x['done']} de {x['of']}")
        nr = c["no_release"]
        out.append(f"    sem release: {nr['stories']} stories ({nr['done']} de {nr['of']})" +
                   ("" if nr["shown"] or not nr["stories"] else " — sem nenhum release declarado, o card nem aparece"))
        if c["epics"]:
            out.append("    épicos: " + " · ".join(f"{x['id']} {x['done']} de {x['of']}" for x in c["epics"]))
        if c.get("outcomes"):
            out.append("    resultados: " + " · ".join(f"{x['id']} {x['done']} de {x['of']}" for x in c["outcomes"]))
        ft = c.get("features")
        if ft and ft["total"]:
            placed = " · ".join(f"{k or 'sem release'} {len(v)}" for k, v in sorted(ft.get("by_release", {}).items(), key=lambda kv: (kv[0] is None, kv[0] or "")))
            out.append(f"    features: {ft['total']}" + (f" (no quadro: {placed})" if placed else "") + (f"; sem `track:` (lidas como normais; o item feature-track cobra): {', '.join(ft['no_track'])}" if ft["no_track"] else ""))
    head = (f"product_structure_check: {name} — " +
            ("VERDE: todas as vistas do Control Center têm o que mostrar" if not r.gaps else
             f"VERMELHO: {len(r.gaps)} lacuna(s) em {len({g['view'] for g in r.gaps})} vista(s)"))
    return "\n".join([head, *out])


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    as_json, quiet = "--json" in argv, "--quiet" in argv
    root = Path(args[0] if args else ".").resolve()
    if not root.is_dir():
        print(f"product_structure_check: {root} não é uma pasta — não avaliável", file=sys.stderr)
        return 2
    profile = _profile(root)
    if profile is None:
        print(f"product_structure_check: {root.name} sem {CONTRACT_FILE} — não avaliável", file=sys.stderr)
        return 2
    if profile != "code-app":
        print(f"product_structure_check: {root.name} tem perfil `{profile or '?'}` — só um code-app tem produto na tela; não avaliável", file=sys.stderr)
        return 2
    try:
        r = check(root)
    except (OSError, UnicodeDecodeError) as e:
        print(f"product_structure_check: {root.name}: leitura falhou ({e}) — não avaliável", file=sys.stderr)
        return 2
    if as_json:
        print(json.dumps({"project": root.name, "ok": not r.gaps, "gaps": r.gaps, "counts": r.counts},
                         ensure_ascii=False, indent=2))
    elif quiet:
        print(render(r, root.name).splitlines()[0])
        for g in r.gaps[:20]:
            print(f"  [{g['view']}] {g['file']}:{g['line']}: {g['message']} → {g['owner']}")
        if len(r.gaps) > 20:
            print(f"  … e mais {len(r.gaps) - 20}")
    else:
        print(render(r, root.name))
    return 1 if r.gaps else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
