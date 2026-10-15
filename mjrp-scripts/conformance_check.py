#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-14 · fonte d3f64f76 · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""
conformance_check.py - the canonical conformance of the children (ADR-0019): catalog x child project.

Born 2026-10-13 (fin-control gap audit): the bootstrap installed the KERNEL in the fin-control, the doctor stayed
green, and yet the canonical artifacts of Discovery (info-arch.md, a design system that declares themes, a ROADMAP in
Now/Next/Later with outcomes, uat@2, `screen:` + `sensors.visual`) were never built. Nothing compared a child with
what the harness now calls canonical, so a standard that evolves in the harness reached the children only if somebody
remembered. This module is that comparison - and the gate that makes the harness write the migration note when the
standard changes.

Pieces (names fixed by ADR-0019 § Nomes), all stdlib:
  - the CATALOG, mjrp-scripts/canonical_catalog.json: items (id, version, title, path, applies_to, since, grace_days,
    born_of, owner_skill, check, migration, template, pattern_sources, pattern_digest, superseded), pattern_carriers,
    not_canonical, history. `title` (the Portuguese label of the message) is the one key added to the ADR's list;
  - the CHECK: one clause, a list of clauses (all), or {"any": [...]} (some); nestable. Clause kinds are a closed set
    with closed parameters: exists, glob, contains, frontmatter_key, contract_key, name_pattern, delegated, script
    (2026-10-14 19:57, decision of the MJRP: the fin-control Board came out empty and no declarative clause can say
    "the Control Center renders this product" - `script` runs a stdlib sensor that lives next to this file, vendored
    with it, on the project: exit 0 passes, 1 is a gap with its first lines, 2 is "não avaliável");
  - the MIGRATION NOTES, mjrp-scripts/migrations/CM-NNNN-<slug>.md: one per version step (from -> to), a chain, immutable;
    frontmatter only id, item, from, to;
  - the child's contract `conformance:` -> applied: [CM-...], received: {"<item>@<version>": date} (stamped only by
    new_project.py --refresh-kernel; none in a project that reads the kernel in place, ADR-0020 D.2), waived: [{item, reason, until}];
  - the LEARN GATE (--learn-gate, a sensor of the harness contract run by the doctor's A1): runs each item's check against
    its owning template, hashes the pattern sources that are not templates, and checks the catalog is whole.

Severity: a gap is a warning until max(since, received) + grace_days, an error after; a note listed in `applied` whose
check (of the version it targeted) fails is an error at once; "not evaluable" is never a pass. Waivers and editorial
rebaselines are the human's valves: they only count with the commit trailers `Conformance-waiver:` and
`Catalog-editorial:`, which the commit-msg hook refuses next to an agent's Co-Authored-By.

Usage:
  python3 conformance_check.py <project> [--gaps] [--pending] [--json]
  python3 conformance_check.py . --learn-gate
  python3 conformance_check.py . --rebaseline <item>
  python3 conformance_check.py --check-msg <commit-message-file>        (the commit-msg hook)
Exit: 0 conforms · 1 an overdue gap, or an invalid catalog / failing learn gate · 2 not evaluable.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
CATALOG_FILE = HERE / "canonical_catalog.json"
NOTES_DIR = HERE / "migrations"
ROOT_OF_SOURCE = HERE.parent          # where templates and pattern_sources resolve: the harness checkout
CATALOG_REL = "mjrp-scripts/canonical_catalog.json"

ITEM_FIELDS = ("id", "version", "title", "path", "applies_to", "since", "check", "pattern_sources", "pattern_digest",
               "migration", "owner_skill", "born_of")
WHEN_STATIC = ("always", "has_screen")
NOTE_SECTIONS = ("## Por que", "## O que muda", "## O que o filho faz", "## Como se confere", "## Quando não se aplica")
MIGRATION_ID = re.compile(r"^CM-\d{4}$")
MAX_WAIVER_DAYS = 90
MAX_WAIVER_COMMITS = 2                # the waiver and one renewal; the third is ignored
TRAILER_WAIVER, TRAILER_EDITORIAL = "Conformance-waiver", "Catalog-editorial"
AGENT_SIGNATURE = re.compile(r"^Co-Authored-By:.*(claude|anthropic|codex|gemini|copilot|cursor|gpt|openai)", re.I | re.M)

# clause kind -> (required, optional); a parameter outside both is an invalid catalog
CLAUSES = {
    "exists": ({"paths"}, set()),
    "glob": ({"pattern"}, {"min"}),
    "contains": ({"pattern"}, {"path", "paths", "label", "min"}),
    "frontmatter_key": ({"glob", "key"}, {"min", "if", "label"}),
    "contract_key": ({"key"}, set()),
    "name_pattern": ({"glob"}, {"regex", "deny_words", "skip", "label"}),
    "delegated": ({"code", "requires"}, set()),
    "script": ({"script"}, {"label"}),
}
SCRIPT_NAME = re.compile(r"^[a-z0-9_]+\.py$")      # a file next to this one, never a path: the clause cannot reach outside
SCRIPT_TIMEOUT = 120
SCRIPT_LINES = 3


class Unknown(Exception):
    """A check that cannot tell. Reported as "não avaliável" - an unknown is never a pass."""


class ScriptUnknown(Unknown):
    """A `script` clause that could not run (script missing, crashed, timed out, exit 2): the child cannot tell whether it
    conforms. Unlike the other unknowns this one is a WARNING in the I6 - the obligation is real and unjudged, and a note
    would leave the child silent for as long as the script stays broken (verification 2026-10-14 P2-4)."""


class CatalogError(Exception):
    pass


# ---------------------------------------------------------------- check shape --------------------------------

def validate_check(check, where="check"):
    """Raises CatalogError for an unknown kind, a missing or extra parameter, or a regex that does not compile."""
    if isinstance(check, list):
        if not check:
            raise CatalogError(f"{where}: lista de cláusulas vazia")
        for c in check:
            validate_check(c, where)
        return
    if not isinstance(check, dict):
        raise CatalogError(f"{where}: cláusula deve ser objeto ou lista")
    if "any" in check:
        if set(check) != {"any"} or not isinstance(check["any"], list) or not check["any"]:
            raise CatalogError(f"{where}: `any` é uma lista não vazia e a única chave")
        for c in check["any"]:
            validate_check(c, where)
        return
    kind = check.get("kind")
    if kind not in CLAUSES:
        raise CatalogError(f"{where}: kind '{kind}' fora de {', '.join(CLAUSES)}")
    req, opt = CLAUSES[kind]
    keys = set(check) - {"kind"}
    if req - keys:
        raise CatalogError(f"{where}: {kind} sem {', '.join(sorted(req - keys))}")
    if keys - req - opt:
        raise CatalogError(f"{where}: {kind} com parâmetro desconhecido {', '.join(sorted(keys - req - opt))}")
    if kind == "contains" and not (("path" in check) ^ ("paths" in check)):
        raise CatalogError(f"{where}: contains leva `path` ou `paths`")
    if kind == "name_pattern" and not (check.get("regex") or check.get("deny_words")):
        raise CatalogError(f"{where}: name_pattern leva ao menos `regex` ou `deny_words`")
    for rx in (check.get("pattern") if kind in ("contains",) else None, check.get("regex")):
        if rx:
            try:
                re.compile(rx)
            except re.error as e:
                raise CatalogError(f"{where}: regex não compila ({e})")
    if kind == "script" and not SCRIPT_NAME.match(str(check["script"])):
        raise CatalogError(f"{where}: script é o nome de um arquivo .py ao lado do conformance_check.py, não um caminho")
    if kind == "delegated":
        if not check["requires"]:
            raise CatalogError(f"{where}: delegated sem `requires`")
        validate_check(check["requires"], where)


# ---------------------------------------------------------------- catalog ------------------------------------

def load_catalog(path=None, with_meta=False):
    """The validated catalog: a list of items (`since` as date, `_raw` the item as written). Raises CatalogError.
    With with_meta, returns (items, raw_document)."""
    path = Path(path) if path else CATALOG_FILE
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise CatalogError(f"catálogo ausente: {path}")
    except json.JSONDecodeError as e:
        raise CatalogError(f"catálogo ilegível ({path.name}): {e}")
    items = raw.get("items") if isinstance(raw, dict) else None
    if not isinstance(items, list) or not items:
        raise CatalogError("catálogo sem a lista `items`")
    default_grace = raw.get("default_grace_days", 30)
    seen, migrations, out = set(), set(), []
    for it in items:
        iid = it.get("id", "?") if isinstance(it, dict) else "?"
        missing = [f for f in ITEM_FIELDS if not (isinstance(it, dict) and f in it and it[f] not in (None, ""))]
        if missing:
            raise CatalogError(f"item '{iid}': faltam campos {', '.join(missing)}")
        if iid in seen:
            raise CatalogError(f"id repetido: {iid}")
        seen.add(iid)
        if not MIGRATION_ID.match(str(it["migration"])) or it["migration"] in migrations:
            raise CatalogError(f"item '{iid}': migration '{it['migration']}' fora do formato CM-NNNN ou repetida")
        migrations.add(it["migration"])
        grace = it.get("grace_days", default_grace)
        if not isinstance(it["version"], int) or not isinstance(grace, int):
            raise CatalogError(f"item '{iid}': version e grace_days são inteiros")
        ap = it["applies_to"]
        if not isinstance(ap, dict) or not isinstance(ap.get("profiles"), list):
            raise CatalogError(f"item '{iid}': applies_to precisa de `profiles` (lista)")
        when = ap.get("when", "always")
        if when not in WHEN_STATIC and not when.startswith("has_path:"):
            raise CatalogError(f"item '{iid}': applies_to.when '{when}' fora de always · has_screen · has_path:<caminho>")
        if it.get("max_severity") not in (None, "warning"):
            raise CatalogError(f"item '{iid}': max_severity só pode ser 'warning'")
        validate_check(it["check"], f"item '{iid}'")
        sup = it.get("superseded", [])
        if not isinstance(sup, list):
            raise CatalogError(f"item '{iid}': superseded é lista")
        for s in sup:
            if not isinstance(s, dict) or "version" not in s or "check" not in s:
                raise CatalogError(f"item '{iid}': superseded precisa de version e check")
            validate_check(s["check"], f"item '{iid}' superseded v{s['version']}")
            migrations.add(s.get("migration") or "")
        if not isinstance(it["pattern_sources"], list) or not isinstance(it["pattern_digest"], dict):
            raise CatalogError(f"item '{iid}': pattern_sources é lista e pattern_digest é mapa caminho → hash")
        try:
            since = date.fromisoformat(str(it["since"]))
        except ValueError:
            raise CatalogError(f"item '{iid}': since '{it['since']}' não é AAAA-MM-DD")
        item = dict(it)
        item["since"] = since
        item["grace_days"] = grace
        item["superseded"] = sup
        item["_raw"] = it
        out.append(item)
    return (out, raw) if with_meta else out


def find_catalog(root):
    """The catalog a project is judged by: the copy in its own mjrp-scripts/, or - for a nested project that has none -
    the one of the repository it lives in (nearest parent). None when there is none."""
    p = Path(root).resolve()
    for d in [p, *p.parents]:
        if (d / "mjrp-scripts" / "canonical_catalog.json").is_file():
            return d / "mjrp-scripts" / "canonical_catalog.json"
    return None


def _source_text(spec, base):
    """`path` or `path#Heading`: the whole file, or the section that starts at that heading line (up to the next one
    of the same or a higher level). A source that is not there is None."""
    rel, _, head = spec.partition("#")
    p = Path(base) / rel
    if not p.is_file():
        return None
    text = p.read_text(encoding="utf-8", errors="replace")
    if not head:
        return text
    lines = text.splitlines()
    for i, l in enumerate(lines):
        m = re.match(r"^(#+)\s+(.*)$", l)
        if m and m.group(2).strip().lower() == head.strip().lower():
            level, out = len(m.group(1)), [l]
            for l2 in lines[i + 1:]:
                m2 = re.match(r"^(#+)\s", l2)
                if m2 and len(m2.group(1)) <= level:
                    break
                out.append(l2)
            return "\n".join(out)
    return None


def source_digest(spec, base=None):
    t = _source_text(spec, base or ROOT_OF_SOURCE)
    return None if t is None else "sha256:" + hashlib.sha256(t.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- clauses ------------------------------------

def _dotted(cfg, key):
    cur = cfg
    for part in key.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def _frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text or "", re.S)
    return m.group(1) if m else ""


def _glob(root, pattern):
    return sorted(p for p in Path(root).glob(pattern) if p.is_file())


def c_exists(root, cfg, c):
    for rel in c["paths"]:
        p = Path(root) / rel
        if p.is_dir() if rel.endswith("/") else p.is_file():
            return []
    return [f"{' ou '.join(c['paths'])} ausente"]


def c_glob(root, cfg, c):
    n = len(_glob(root, c["pattern"]))
    return [] if n >= c.get("min", 1) else [f"nenhum arquivo em {c['pattern']}" if n == 0 else f"só {n} arquivo(s) em {c['pattern']}"]


def c_contains(root, cfg, c):
    paths = c.get("paths") or [c["path"]]
    present = [Path(root) / p for p in paths if (Path(root) / p).is_file()]
    if not present:
        return [f"{' ou '.join(paths)} ausente"]
    for p in present:
        if len(re.findall(c["pattern"], p.read_text(encoding="utf-8", errors="replace"), re.M)) >= c.get("min", 1):
            return []
    return [f"{' / '.join(paths)}: {c.get('label') or 'falta ' + c['pattern']}"]


def c_frontmatter_key(root, cfg, c):
    files = _glob(root, c["glob"])
    if len(files) < c.get("min", 1):
        return [f"nenhum arquivo em {c['glob']}"]        # an empty glob FAILS: nothing to carry the key is a gap
    cond = c.get("if")
    bad = []
    for p in files:
        fm = _frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        if cond and not re.search(rf"^{re.escape(cond['key'])}:\s*{re.escape(str(cond['equals']))}\s*(#.*)?$", fm, re.M):
            continue
        if not re.search(rf"^{re.escape(c['key'])}:\s*\S", fm, re.M):
            bad.append(p.parent.name if p.name in ("spec.md", "plan.md", "tasks.md") else p.name)
    if not bad:
        return []
    return [f"{len(bad)} arquivo(s) de {c['glob']} sem `{c['key']}:` no frontmatter ({', '.join(bad[:4])}{'...' if len(bad) > 4 else ''})"]


def c_contract_key(root, cfg, c):
    return [] if _dotted(cfg, c["key"]) not in (None, "", [], {}) else [f"contrato sem `{c['key']}`"]


def c_name_pattern(root, cfg, c):
    deny, skip = set(c.get("deny_words", [])), set(c.get("skip", []))
    rx = re.compile(c["regex"]) if c.get("regex") else None
    bad = []
    for p in _glob(root, c["glob"]):                     # an empty glob PASSES: there is no name to violate
        if p.name in skip:
            continue
        if (rx and not rx.match(p.name)) or any(ord(ch) > 127 for ch in p.stem) or any(t in deny for t in re.split(r"[-_.\s]+", p.stem.lower())):
            bad.append(str(p.relative_to(root)))
    if not bad:
        return []
    return [f"{len(bad)} arquivo(s) com nome fora do padrão ou que não está em inglês: {', '.join(bad[:4])}{'...' if len(bad) > 4 else ''}"]


def c_script(root, cfg, c):
    """The sensor `c["script"]`, next to this file (vendored with it), run on the project: 0 passes; 1 is a gap - its
    first lines and the command for the whole list; 2, a crash or a missing script are Unknown (never a pass)."""
    path = HERE / c["script"]
    if not path.is_file():
        raise ScriptUnknown(f"{c['script']} ausente ao lado do conformance_check.py — rode `new_project.py <filho> --refresh-kernel`")
    try:
        p = subprocess.run([sys.executable, str(path), str(root), "--quiet"], capture_output=True, text=True,
                           timeout=SCRIPT_TIMEOUT)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise ScriptUnknown(f"{c['script']} não rodou ({e.__class__.__name__})")
    if p.returncode == 0:
        return []
    if p.returncode == 1:
        lines = [l.strip() for l in p.stdout.splitlines() if l.strip()]
        head, detail = (lines[0] if lines else c["script"]), [l for l in lines[1:] if l.startswith("[")][:SCRIPT_LINES]
        more = f"; lista inteira: `python3 mjrp-scripts/{c['script']} .`"
        return [f"{c.get('label') or head}: " + " | ".join(detail or [head]) + more]
    why = (p.stderr or p.stdout).strip().splitlines()
    raise ScriptUnknown(f"{c['script']} saiu {p.returncode}: {why[0] if why else 'sem mensagem'}")


LEAVES = {"exists": c_exists, "glob": c_glob, "contains": c_contains, "frontmatter_key": c_frontmatter_key,
          "contract_key": c_contract_key, "name_pattern": c_name_pattern, "script": c_script}


def run_check(check, root, cfg, delegated=None):
    """The reasons a check fails ([] = passes). `delegated` collects the codes of delegated clauses whose `requires` held."""
    if isinstance(check, list):
        out = []
        for c in check:
            out += run_check(c, root, cfg, delegated)
        return out
    if "any" in check:
        reasons = []
        for c in check["any"]:
            r = run_check(c, root, cfg, delegated)
            if not r:
                return []
            reasons += r
        return ["nenhuma das alternativas vale: " + " | ".join(reasons)]
    if check["kind"] == "delegated":
        r = run_check(check["requires"], root, cfg, delegated)
        if r:
            return [f"pré-condição de {check['code']} não vale: " + "; ".join(r)]
        if delegated is not None:
            delegated.append(check["code"])
        return []
    return LEAVES[check["kind"]](root, cfg, check)


# ---------------------------------------------------------------- notes and chains ---------------------------

def _note_fields(text):
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^(\w+):\s*(.*)$", _frontmatter(text), re.M)}


def read_notes(notes_dir=None):
    """Every note: [{id, item, from, to, path, text}]."""
    nd = Path(notes_dir) if notes_dir else NOTES_DIR
    out = []
    for p in sorted(nd.glob("CM-*.md")) if nd.is_dir() else []:
        text = p.read_text(encoding="utf-8")
        f = _note_fields(text)
        try:
            frm, to = int(f.get("from", "")), int(f.get("to", ""))
        except ValueError:
            frm = to = None
        out.append({"id": f.get("id"), "item": f.get("item"), "from": frm, "to": to, "path": p, "text": text})
    return out


def chain(item, notes):
    """The notes of one item, in order of `from`."""
    return sorted((n for n in notes if n["item"] == item["id"] and n["from"] is not None), key=lambda n: n["from"])


def check_of_version(item, version):
    if version == item["version"]:
        return item["check"]
    for s in item["superseded"]:
        if s["version"] == version:
            return s["check"]
    return None


# ---------------------------------------------------------------- evaluation ---------------------------------

def applies(item, cfg, root, has_screen):
    """True / False / None (cannot tell: the item needs the screen definition and the caller has none)."""
    ap = item["applies_to"]
    if cfg.get("profile") not in ap["profiles"]:
        return False
    if ap.get("process_levels") and cfg.get("process_level") and cfg.get("process_level") not in ap["process_levels"]:
        return False
    when = ap.get("when", "always")
    if when == "has_screen":
        return has_screen
    if when.startswith("has_path:"):
        rel = when.split(":", 1)[1]
        return any(Path(root).glob(rel)) if any(ch in rel for ch in "*?[") else (Path(root) / rel).exists()
    return True


def _as_date(v):
    if isinstance(v, datetime):
        return v.date()
    if isinstance(v, date):
        return v
    try:
        return date.fromisoformat(str(v))
    except ValueError:
        return None


def kernel_in_repo(cfg):
    """ADR-0020 D.2: a project nested in the harness repository reads the kernel in place (`kernel: {source: in-repo}`):
    it receives nothing, so it has no `received` stamp - the grace of every item counts from the item's own `since`."""
    k = (cfg or {}).get("kernel")
    return isinstance(k, dict) and str(k.get("source") or "").strip() == "in-repo"


def received_date(item, cfg):
    if kernel_in_repo(cfg):
        return None
    r = (cfg.get("conformance") or {}).get("received") or {}
    return _as_date(r.get(f"{item['id']}@{item['version']}")) if isinstance(r, dict) else None


def grace_until(item, cfg):
    """max(since, received) + grace_days: the carência counts from the day THIS child received the obligation."""
    rec = received_date(item, cfg)
    return max(item["since"], rec) + timedelta(days=item["grace_days"]) if rec else item["since"] + timedelta(days=item["grace_days"])


def severity(item, today, cfg=None):
    """warning inside the grace, error after - except an item with `max_severity: warning` (the MJRP's call for checks that
    are heuristics, e.g. english-names), which never escalates."""
    if item.get("max_severity") == "warning":
        return "warning"
    return "warning" if today <= grace_until(item, cfg or {}) else "error"


def git_trailer_commits(root, trailer, item_id):
    """Dates of the commits touching the contract whose message carries `<trailer>: <item> — ...`, newest first;
    None when git cannot answer (no repository): not evaluable never becomes approval."""
    try:
        p = subprocess.run(["git", "log", "--format=%cs%x1f%B%x1e", "--", ".mjrp-project.yml"], cwd=str(root),
                           capture_output=True, text=True, timeout=30)
    except Exception:
        return None
    if p.returncode != 0:
        return None
    dates = []
    for rec in p.stdout.split("\x1e"):
        if "\x1f" not in rec:
            continue
        cs, body = rec.strip().split("\x1f", 1)
        if re.search(rf"^{re.escape(trailer)}:\s*{re.escape(item_id)}\b", body, re.M):
            d = _as_date(cs)
            if d:
                dates.append(d)
    return dates


def waiver_for(item, cfg, today, root, commits=None):
    """(waiver, honored, why_not). A waiver needs: reason; `until` valid, not past, at most 90 days after the commit that
    carries the human's trailer; that trailer commit to exist (git); and not to be the third in a row for the item."""
    w = (cfg.get("conformance") or {}).get("waived") or []
    for x in w if isinstance(w, list) else []:
        if not (isinstance(x, dict) and x.get("item") == item["id"]):
            continue
        until = _as_date(x.get("until"))
        if until is None:
            return x, False, "a dispensa não tem `until` válido"
        if until < today:
            return x, False, f"a dispensa venceu em {until}"
        if not x.get("reason"):
            return x, False, "a dispensa não diz o motivo"
        dates = (commits or git_trailer_commits)(root, TRAILER_WAIVER, item["id"])
        if dates is None:
            return x, False, "sem git não há como conferir o trailer `Conformance-waiver:` — a dispensa não vale"
        if not dates:
            return x, False, f"a dispensa não tem commit com o trailer `{TRAILER_WAIVER}: {item['id']} — <motivo>` (só o humano a escreve)"
        if len(dates) > MAX_WAIVER_COMMITS:
            return x, False, f"a dispensa já foi renovada além do limite ({len(dates)} commits com o trailer; vale a original e uma renovação)"
        if until > max(dates) + timedelta(days=MAX_WAIVER_DAYS):
            return x, False, f"a dispensa passa de {MAX_WAIVER_DAYS} dias do commit que a escreveu (até {until})"
        return x, True, ""
    return None, False, ""


def evaluate(root, cfg, today, items=None, has_screen=None, notes_dir=None, trailer_commits=None):
    """One result per applicable item: {id, status: ok|gap|unknown|waived, severity, reasons, delegated, item, no_stamp}
    (an `unknown` caused by a `script` clause that could not run also carries `warn: True`: the I6 warns on it).
    Plus, for an item whose applied note targeted an OLDER version, a gap judged by that version's own check (error).
    Nothing is written. `has_screen`: True/False from the one definition of "has a screen" (visual_gate.screen_on_disk),
    None when the caller cannot tell - then screen items come back `unknown`."""
    items = items if items is not None else load_catalog()
    notes = read_notes(notes_dir)
    applied = set((cfg.get("conformance") or {}).get("applied") or [])
    out = []
    for it in items:
        ap = applies(it, cfg, root, has_screen)
        if ap is False:
            continue
        res = {"id": it["id"], "severity": severity(it, today, cfg), "reasons": [], "delegated": [], "item": it,
               "no_stamp": received_date(it, cfg) is None, "grace_until": grace_until(it, cfg)}
        if ap is None:
            out.append({**res, "status": "unknown", "reasons": ["não sei se o projeto tem tela (visual_gate.py ausente)"]})
            continue
        waiver, honored, why_not = waiver_for(it, cfg, today, root, trailer_commits)
        if honored:
            out.append({**res, "status": "waived", "reasons": [f"dispensado até {waiver.get('until')}: {waiver.get('reason')}"]})
            continue
        try:
            res["reasons"] = list(dict.fromkeys(run_check(it["check"], root, cfg, res["delegated"])))
        except Unknown as e:
            out.append({**res, "status": "unknown", "reasons": [str(e)], "warn": isinstance(e, ScriptUnknown)})
            continue
        status = "gap" if res["reasons"] else "ok"
        if status == "gap" and why_not:
            res["reasons"].append(why_not)
        # `applied` is not a word: the LAST applied note of the chain is judged by the check of the version it targeted
        done = [n for n in chain(it, notes) if n["id"] in applied]
        if done:
            last = done[-1]
            if last["to"] == it["version"]:
                if status == "gap":
                    res["severity"] = "warning" if it.get("max_severity") == "warning" else "error"
                    res["reasons"].append(f"{last['id']} consta em `conformance.applied`, mas a checagem reprova")
            else:
                old = check_of_version(it, last["to"])
                if old is None:
                    out.append({**res, "status": "gap", "severity": "warning" if it.get("max_severity") == "warning" else "error", "reasons": [f"{last['id']} aplicada, mas o catálogo não guarda o check de {it['id']}@{last['to']} (superseded)"]})
                else:
                    try:
                        why = run_check(old, root, cfg)
                    except Unknown as e:
                        why = [f"não avaliável ({e})"]
                    if why:
                        out.append({**res, "status": "gap", "severity": "warning" if it.get("max_severity") == "warning" else "error",
                                    "reasons": [f"{last['id']} consta em `conformance.applied` e a checagem de {it['id']}@{last['to']} reprova: " + "; ".join(why)]})
        out.append({**res, "status": status})
    return out


def _warning_until(it, until):
    """ADR-0019 § 3: "aviso até AAAA-MM-DD, erro depois" - an item that never escalates (max_severity: warning) says so."""
    if it.get("max_severity") == "warning":
        return "só aviso (nunca vira erro)"
    return f"aviso até {until.isoformat()}, erro depois" if until else "aviso, vira erro depois da carência"


def describe(r):
    """The line the human reads (Portuguese): falta X (exigido desde D, nasceu de Y) -> rode <skill> (nota CM-NNNN)."""
    it = r["item"]
    if r["status"] == "unknown":
        return f"{it['id']}@{it['version']}: não avaliável — {'; '.join(r['reasons'])}"
    prazo = "erro" if r["severity"] == "error" else _warning_until(it, r.get("grace_until"))
    return (f"{it['id']}@{it['version']}: falta {it['title']} — {'; '.join(r['reasons'])} (exigido desde {it['since'].isoformat()}, "
            f"nasceu de {it['born_of']}) → rode {it['owner_skill']} (nota {it['migration']}) · {prazo}")


def _pending_deadline(it, cfg, today):
    """The tail of a pending note's line: the end of the item's grace for THIS project, or that it already escalated."""
    until = grace_until(it, cfg)
    if severity(it, today, cfg) == "error":
        return f"erro desde {(until + timedelta(days=1)).isoformat()}"
    return _warning_until(it, until)


def check_note(root, cfg, note_id, items, notes):
    """(exit, text): the check of the version the note LEADS TO (its `to`), plus whether the item's current version
    passes - a note whose own check is stricter than the current one is satisfied by the current form (the conform
    mode then records the whole chain). Writes nothing."""
    n = next((x for x in notes if x["id"] == note_id), None)
    if n is None:
        return 2, f"conformance_check: nota {note_id} não existe no catálogo deste projeto"
    it = next((i for i in items if i["id"] == n["item"]), None)
    chk = check_of_version(it, n["to"]) if it else None
    if chk is None:
        return 2, f"conformance_check: {note_id}: o catálogo não guarda o check de {n['item']}@{n['to']}"
    try:
        why = run_check(chk, root, cfg)
    except Unknown as e:
        return 2, f"{note_id} ({it['id']}@{n['from']}→{n['to']}): não avaliável — {e}"
    lines = [f"{note_id} ({it['id']}@{n['from']}→{n['to']}): " + ("passou" if not why else "reprovou — " + "; ".join(why))]
    if n["to"] != it["version"]:
        try:
            cur = run_check(it["check"], root, cfg)
        except Unknown as e:
            cur = [f"não avaliável ({e})"]
        lines.append(f"versão atual ({it['id']}@{it['version']}): " + ("passou" if not cur else "reprovou — " + "; ".join(cur)))
    return (1 if why else 0), "\n".join(lines)


def pending(root, cfg, items=None, notes_dir=None, has_screen=None, today=None, trailer_commits=None):
    """Notes of the chain the child has not applied, in chain order. [(item, note_or_None)]. Never applies anything.
    An item that does not apply to the project (profile, process_level, `when`) has no pending note; an item is dropped
    only by a VALID waiver (the human's trailer found, within 90 days, at most one renewal) - not by a line in the contract.
    `has_screen` None keeps the screen items (cannot tell)."""
    items = items if items is not None else load_catalog()
    applied = (cfg.get("conformance") or {}).get("applied") or []
    today = today or date.today()
    notes = read_notes(notes_dir)
    out = []
    for it in items:
        if applies(it, cfg, root, has_screen) is False:
            continue
        if waiver_for(it, cfg, today, root, trailer_commits)[1]:
            continue
        ch = chain(it, notes)
        if not ch:
            out.append((it, None))
        out += [(it, n) for n in ch if n["id"] not in applied]
    return out


# ---------------------------------------------------------------- received stamp (refresh only) -------------

def stamp_received(contract_path, cfg, items, today, root, has_screen):
    """The ONLY writer of `conformance.received`: for each applicable <item>@<version> not yet in the map, today's date.
    Returns the keys stamped. Never rewrites an existing stamp, never touches `applied` or `waived`.
    A project that reads the kernel in place (ADR-0020 D.2) is never stamped: it receives nothing, the source holds it."""
    if kernel_in_repo(cfg):
        return []
    have = (cfg.get("conformance") or {}).get("received") or {}
    new = {f"{it['id']}@{it['version']}": today.isoformat() for it in items
           if applies(it, cfg, root, has_screen) is True and f"{it['id']}@{it['version']}" not in have}
    if not new:
        return []
    path = Path(contract_path)
    lines = path.read_text(encoding="utf-8").split("\n")
    entries = [f"      {k}: {v}" for k, v in new.items()]
    ci = next((i for i, l in enumerate(lines) if re.match(r"^  conformance:\s*(#.*)?$", l)), None)   # the key, with or without a comment
    if ci is None and any(re.match(r"^  conformance:\s*\S", l) and not re.match(r"^  conformance:\s*#", l) for l in lines):
        return []          # an inline map (or any value on the key's line) that we do not rewrite: never open a second block
    if ci is None:
        while lines and lines[-1] == "":
            lines.pop()
        lines += ["  conformance:                   # ADR-0019: applied = notas cumpridas; received = escrito só pelo --refresh-kernel; waived = dispensa do humano",
                  "    applied: []", "    received:"] + entries + [""]
    else:
        end = next((i for i in range(ci + 1, len(lines)) if lines[i].strip() and not lines[i].startswith("    ")), len(lines))
        ri = next((i for i in range(ci + 1, end) if re.match(r"^    received:", lines[i])), None)
        if ri is None:
            lines[ci + 1:ci + 1] = ["    received:"] + entries
        else:
            lines[ri] = "    received:"
            lines[ri + 1:ri + 1] = entries
    path.write_text("\n".join(lines), encoding="utf-8")
    return list(new)


# ---------------------------------------------------------------- learn gate ---------------------------------

def _skill_exists(base, name):
    root = Path(base) / "mjrp-skills"
    return any(p.is_dir() and p.name == name for p in root.rglob(name)) if root.is_dir() else True   # no skills dir: nothing to judge


def _template_destination(item):
    """Where the owning skill copies the template: the first file the item's check reads (a glob's `*` becomes a folder)."""
    def walk(c):
        if isinstance(c, list):
            for x in c:
                d = walk(x)
                if d:
                    return d
        elif isinstance(c, dict):
            if "any" in c:
                return walk(c["any"])
            if c.get("kind") == "contains":
                return (c.get("paths") or [c.get("path")])[0]
            if c.get("kind") == "frontmatter_key":
                return c["glob"].replace("*", "F00-template")
        return None
    return walk(item["check"]) or item["path"]


def template_problems(item, base):
    """The Learn gate's strongest rule: the item's check runs against the item's own template, copied to the artifact's
    path in a scratch directory. Divergence of catalog and model cannot be re-stamped away."""
    src = Path(base) / item["template"]
    if not src.is_file():
        return [f"{item['id']}: o template não existe: {item['template']}"]
    with tempfile.TemporaryDirectory() as t:
        dest = Path(t) / _template_destination(item)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, dest)
        cfg = {"profile": item["applies_to"]["profiles"][0]}
        reasons = run_check(item["check"], t, cfg)
    return [f"{item['id']}: o template {item['template']} reprova o check do próprio item — {'; '.join(reasons)} "
            f"(o modelo e o catálogo divergem: mude o modelo, ou o item com uma nota nova)"] if reasons else []


def git_digest_changes(base, item_id):
    """[(commit_message, version_changed)] for every commit of the catalog that changed this item's pattern_digest."""
    try:
        # the history that counts is the principal branch's: an unmerged branch may rewrite its own catalog freely
        ok_main = subprocess.run(["git", "rev-parse", "--verify", "-q", "main"], cwd=str(base), capture_output=True).returncode == 0
        log = subprocess.run(["git", "log", "main" if ok_main else "HEAD", "--first-parent", "--format=%H", "-n", "200", "--", CATALOG_REL], cwd=str(base),
                             capture_output=True, text=True, timeout=60)
    except Exception:
        return None
    if log.returncode != 0:
        return None

    def at(rev):
        p = subprocess.run(["git", "show", f"{rev}:{CATALOG_REL}"], cwd=str(base), capture_output=True, text=True)
        if p.returncode != 0:
            return None
        try:
            return next((x for x in json.loads(p.stdout)["items"] if x["id"] == item_id), None)
        except (json.JSONDecodeError, KeyError):
            return None
    out = []
    for h in [x for x in log.stdout.split() if x]:
        cur, prev = at(h), at(h + "~1")
        if cur is None:
            continue
        if prev is None or prev.get("pattern_digest") != cur.get("pattern_digest"):
            msg = subprocess.run(["git", "log", "-1", "--format=%B", h], cwd=str(base), capture_output=True, text=True).stdout
            out.append((msg, prev is not None and prev.get("version") != cur.get("version"), prev is None))
    return out


def _published_paths_by_id(base, ref, folders):
    """{note id: [path on `ref`]} for every CM-*.md under `folders` (relative to base) at `ref`; None if git cannot say."""
    by_id = {}
    for folder in sorted(folders):
        ls = subprocess.run(["git", "ls-tree", "-r", "--name-only", ref, "--", folder], cwd=str(base), capture_output=True, text=True, timeout=60)
        if ls.returncode != 0:
            return None
        for rel in ls.stdout.splitlines():
            if not re.match(r"CM-.*\.md$", Path(rel).name):
                continue
            shown = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=str(base), capture_output=True, timeout=60)
            if shown.returncode == 0:
                nid = _note_fields(shown.stdout.decode("utf-8", "replace")).get("id")
                by_id.setdefault(nid, []).append(rel)
    return by_id


def published_note_problems(notes, base):
    """ADR-0019 § 2: a published note is not rewritten. A note is published when it is on the principal branch (the same
    `main`/`--first-parent` reading as the digest rule above - an unmerged branch may still write its own drafts); its bytes
    must equal the bytes of the commit that first brought it there. There is no valve for a note (the editorial trailer is
    the digest's): correcting a wrong note is a new note. Born of the incident of 2026-10-14, when CM-0019 and CM-0003 were
    reworded on a branch after the refresh had already carried them to nine children (P1-3 of
    reports/audits/2026-10-14-product-structure-in-owners-verification.md).
    The note is found by its `id`, not by its path (P2-5 of the second verification, 2026-10-14): a published note renamed and
    edited on a branch is a new path to git, which would read as a draft and let the edit through; matched by `id` it is still
    the published note, and its bytes are judged against the ones published under its old name."""
    problems = []
    ok_main = subprocess.run(["git", "rev-parse", "--verify", "-q", "main"], cwd=str(base), capture_output=True).returncode == 0
    ref = "main" if ok_main else "HEAD"
    rels = {}
    for n in notes:
        try:
            rels[n["path"]] = Path(n["path"]).resolve().relative_to(Path(base).resolve()).as_posix()
        except ValueError:
            continue
    try:
        by_id = _published_paths_by_id(base, ref, {Path(r).parent.as_posix() for r in rels.values()})
    except Exception:
        by_id = None
    if by_id is None:
        return [f"sem git não há como conferir se as notas publicadas mudaram (ADR-0019 § 2)"]
    on_main = {r for paths in by_id.values() for r in paths}
    for n in notes:
        rel = rels.get(n["path"])
        if rel is None:
            continue
        candidates = list(dict.fromkeys(by_id.get(n["id"], []) + ([rel] if rel in on_main else [])))
        for pub in candidates:
            try:
                log = subprocess.run(["git", "log", ref, "--first-parent", "--diff-filter=A", "--format=%H", "--reverse", "--", pub],
                                     cwd=str(base), capture_output=True, text=True, timeout=60)
                first = (log.stdout.split() or [None])[0] if log.returncode == 0 else None
                shown = subprocess.run(["git", "show", f"{first}:{pub}"], cwd=str(base), capture_output=True, timeout=60) if first else None
            except Exception:
                return [f"sem git não há como conferir se as notas publicadas mudaram (ADR-0019 § 2)"]
            if log.returncode != 0:
                return [f"sem git não há como conferir se as notas publicadas mudaram (ADR-0019 § 2)"]
            if shown is None or shown.returncode != 0:
                continue                            # never reached the principal branch: still a draft
            if shown.stdout != Path(n["path"]).read_bytes():
                moved = f" (publicada como {Path(pub).name}, hoje {Path(n['path']).name})" if pub != rel else ""
                problems.append(f"{Path(n['path']).name}: a nota já foi publicada na main ({first[:8]}){moved} e os bytes mudaram — uma nota publicada não se reescreve "
                                f"(ADR-0019 § 2; não há válvula para nota). Volte aos bytes publicados com `git checkout {first[:8]} -- {pub}` e diga a mudança "
                                f"numa nota nova (um passo de versão do item)")
                break
    return problems


def _scripts_of(check):
    """The `script` names a check runs, at any depth."""
    if isinstance(check, list):
        return [n for c in check for n in _scripts_of(c)]
    if "any" in check:
        return _scripts_of(check["any"])
    if check.get("kind") == "delegated":
        return _scripts_of(check["requires"])
    return [check["script"]] if check.get("kind") == "script" else []


def learn_gate(items=None, notes_dir=None, base=None, doc=None, use_git=True):
    """The source-side gate (ADR-0019 § 4), a sensor of the harness contract. Returns the problems:
      1. every pattern carrier (a template in `pattern_carriers`) is a `template` or pattern source of some item, or is in
         `not_canonical`;
      2. each item with a `template` passes its own check run against that template;
      3. each pattern source WITHOUT a template matches its `pattern_digest`; a re-stamp without a version bump needs the
         human's `Catalog-editorial: <item> — <motivo>` trailer in the commit that changed the digest (git log);
      4. the catalog is whole: valid clauses (the loader), notes chain without hole or duplicate up to `version`, every
         older note's version has its `check` in `superseded`, `migration` is the last note, `owner_skill` exists;
      5. a published note's bytes never change (`published_note_problems`: equal to the commit that first brought it to main)."""
    if items is None:
        items, doc = load_catalog(with_meta=True)
    doc = doc or {}
    base = Path(base) if base else ROOT_OF_SOURCE
    problems, owned = [], set()
    for it in items:
        owned.update(it["pattern_sources"])
        if it.get("template"):
            owned.add(it["template"])
    declared = {e.get("path") for e in doc.get("not_canonical", []) if isinstance(e, dict)}
    for g in doc.get("pattern_carriers", []):
        for f in sorted(p for p in base.glob(g) if p.is_file()):
            rel = f.relative_to(base).as_posix()
            if rel not in owned and rel not in declared:
                problems.append(f"portador sem dono: {rel} — modelo que nenhum item do catálogo usa e que não está em `not_canonical` "
                                f"(um padrão novo não passa calado: crie o item e a nota, ou declare-o não canônico com o motivo)")
    notes = read_notes(notes_dir)
    ids = {it["migration"] for it in items} | {s.get("migration") for it in items for s in it["superseded"] if s.get("migration")}
    for it in items:
        if it.get("template"):
            problems += template_problems(it, base)
        else:
            for spec in it["pattern_sources"]:
                cur = source_digest(spec, base)
                if cur is None:
                    problems.append(f"{it['id']}: a pattern_source não existe: {spec}")
                elif cur != it["pattern_digest"].get(spec):
                    problems.append(f"{it['id']}: o padrão mudou — {spec}. Suba a versão do item e escreva a nota da cadeia, depois "
                                    f"`conformance_check.py . --rebaseline {it['id']}`; se foi só redação, o rebaseline vai num commit com "
                                    f"`{TRAILER_EDITORIAL}: {it['id']} — <motivo>` (do humano)")
            ch = git_digest_changes(base, it["id"]) if use_git else []
            if ch is None:
                problems.append(f"{it['id']}: sem git não há como conferir o trailer `{TRAILER_EDITORIAL}:` do rebaseline")
            else:
                for msg, bumped, first in ch:
                    if not bumped and not first and not re.search(rf"^{TRAILER_EDITORIAL}:\s*{re.escape(it['id'])}\b", msg, re.M):
                        problems.append(f"{it['id']}: o pattern_digest mudou sem subir a versão e o commit não tem o trailer "
                                        f"`{TRAILER_EDITORIAL}: {it['id']} — <motivo>` (só o humano o escreve)")
        ch = chain(it, notes)
        if not ch:
            problems.append(f"{it['id']}: sem nota de migração na cadeia — o catálogo mudou e o filho não tem como saber")
        else:
            for a, b in zip(ch, ch[1:]):
                if b["from"] != a["to"]:
                    problems.append(f"{it['id']}: a cadeia de notas tem buraco ou duplicata entre {a['id']} (→{a['to']}) e {b['id']} (de {b['from']})")
            if ch[-1]["to"] != it["version"]:
                problems.append(f"{it['id']}: a última nota ({ch[-1]['id']}) vai até a versão {ch[-1]['to']}, o item está na {it['version']} — escreva a nota nova")
            if ch[-1]["id"] != it["migration"]:
                problems.append(f"{it['id']}: `migration` ({it['migration']}) não é a última nota da cadeia ({ch[-1]['id']})")
            for n in ch:
                if n["to"] != it["version"] and check_of_version(it, n["to"]) is None:
                    problems.append(f"{it['id']}: a nota {n['id']} leva à versão {n['to']} e o item não guarda o check dela em `superseded`")
                for s in NOTE_SECTIONS:
                    if s not in n["text"]:
                        problems.append(f"{it['id']}: a nota {n['path'].name} não tem a seção `{s}`")
        for name in _scripts_of(it["check"]):
            # the clause runs in the CHILD: the script must exist here, travel with the kernel, and be a pattern source
            # (what it demands of the children changes only with a note, like any other standard)
            rel = f"mjrp-scripts/{name}"
            if not (base / rel).is_file():
                problems.append(f"{it['id']}: a cláusula script aponta para {rel}, que não existe")
            if rel not in it["pattern_sources"]:
                problems.append(f"{it['id']}: {rel} roda no filho e não está em `pattern_sources` — mudar o que ele cobra passaria sem nota")
            np_text = (base / "mjrp-scripts" / "new_project.py").read_text(encoding="utf-8") if (base / "mjrp-scripts" / "new_project.py").is_file() else ""
            if np_text and f'"{name}"' not in np_text:
                problems.append(f"{it['id']}: {rel} não está nos VENDORED_FILES do new_project.py — no filho a cláusula fica não avaliável")
        if not _skill_exists(base, it["owner_skill"]):
            problems.append(f"{it['id']}: owner_skill '{it['owner_skill']}' não existe em mjrp-skills/")
    if use_git:
        problems += published_note_problems(notes, base)
    for n in notes:
        if n["id"] not in ids:
            problems.append(f"{n['path'].name}: nota sem item no catálogo")
        elif n["from"] is None:
            problems.append(f"{n['path'].name}: frontmatter sem `from`/`to` numéricos")
    return problems


def rebaseline(item_id, catalog_path=None, base=None, notes_dir=None, now=None):
    """Re-stamp pattern_digest of one item (the only edit this makes to the catalog). The item's current version must
    already be the last note of its chain (the migration was written). A wording-only change, with no version bump, also
    goes through here - and is accepted by the gate only when the COMMIT carries `Catalog-editorial: <item> — <motivo>`,
    which the commit-msg hook refuses next to an agent's Co-Authored-By. Returns (ok, message)."""
    path = Path(catalog_path) if catalog_path else CATALOG_FILE
    items, doc = load_catalog(path, with_meta=True)
    it = next((x for x in items if x["id"] == item_id), None)
    if it is None:
        return False, f"item '{item_id}' não existe no catálogo"
    if it.get("template"):
        return False, f"{item_id} tem `template`: o portão roda o check contra o modelo, não há hash a reestampar"
    base = Path(base) if base else ROOT_OF_SOURCE
    new = {}
    for spec in it["pattern_sources"]:
        d = source_digest(spec, base)
        if d is None:
            return False, f"a pattern_source não existe: {spec}"
        new[spec] = d
    ch = chain(it, read_notes(notes_dir))
    if not ch or ch[-1]["to"] != it["version"]:
        return False, f"a nota da versão {it['version']} de {item_id} ainda não está escrita"
    for x in doc["items"]:
        if x["id"] == item_id:
            x["pattern_digest"] = new
    doc.setdefault("history", []).append({"at": (now or datetime.now()).strftime("%Y-%m-%d %H:%M"), "change": f"{item_id}: pattern_digest reestampado"})
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True, f"{item_id}: pattern_digest reestampado — comite com `{TRAILER_EDITORIAL}: {item_id} — <motivo>` se foi só redação (o humano)"


def message_problem(text):
    """The commit-msg rule: the human's valve trailers cannot sit next to an agent's Co-Authored-By."""
    if re.search(rf"^({TRAILER_WAIVER}|{TRAILER_EDITORIAL}):", text, re.M) and AGENT_SIGNATURE.search(text):
        return (f"os trailers `{TRAILER_WAIVER}:` e `{TRAILER_EDITORIAL}:` são válvulas do humano e este commit leva "
                "`Co-Authored-By:` de agente — o humano comita sem a assinatura do agente")
    return None


# ---------------------------------------------------------------- CLI ----------------------------------------

def load_child(root):
    """(cfg, error): the child's `mjrp_harness` block, through the doctor's own reader."""
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(HERE))
    import doctor
    cfile = Path(root) / ".mjrp-project.yml"
    if not cfile.is_file():
        return None, f"{root} sem .mjrp-project.yml"
    return (doctor.read_yaml(cfile.read_text(encoding="utf-8")) or {}).get("mjrp_harness") or {}, None


def child_has_screen(root, cfg):
    sys.path.insert(0, str(HERE))
    try:
        import visual_gate
    except ModuleNotFoundError:
        return None
    return bool(visual_gate.screen_on_disk(root, cfg.get("screen") if isinstance(cfg.get("screen"), list) else None))


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="conformidade canônica dos filhos (catálogo x projeto) — ADR-0019")
    ap.add_argument("path", nargs="?")
    ap.add_argument("--gaps", action="store_true", help="lista as lacunas (padrão)")
    ap.add_argument("--pending", action="store_true", help="lista as notas de migração pendentes")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--learn-gate", action="store_true")
    ap.add_argument("--rebaseline", metavar="ITEM")
    ap.add_argument("--check-note", metavar="CM-NNNN", help="roda o check da versão que a nota alvejou (e diz se a atual passa); não escreve")
    ap.add_argument("--check-msg", metavar="FILE", help="o commit-msg: recusa trailer do humano com Co-Authored-By de agente")
    a = ap.parse_args(argv)
    if a.check_msg:
        prob = message_problem(Path(a.check_msg).read_text(encoding="utf-8", errors="replace"))
        if prob:
            print(f"conformance_check: {prob}")
            return 1
        return 0
    if not a.path:
        ap.print_help()
        return 2
    catalog = find_catalog(a.path) if not (a.learn_gate or a.rebaseline) else CATALOG_FILE
    if catalog is None:
        print("conformance_check: ERRO — o projeto não tem mjrp-scripts/canonical_catalog.json; rode "
              "`python3 <harness>/mjrp-scripts/new_project.py <esta pasta> --refresh-kernel`")
        return 1
    try:
        items, doc = load_catalog(catalog, with_meta=True)
    except CatalogError as e:
        print(f"conformance_check: {e}")
        return 1 if "catálogo" in str(e) and "ausente" not in str(e) else 2
    if a.learn_gate:
        problems = learn_gate(items, doc=doc)
        for p in problems:
            print(f"  [ERRO learn-gate] {p}")
        print(f"conformance_check: {len(items)} item(ns), {len(problems)} problema(s)")
        return 1 if problems else 0
    if a.rebaseline:
        ok, msg = rebaseline(a.rebaseline)
        print(f"conformance_check: {msg}")
        return 0 if ok else 1
    root = Path(a.path).resolve()
    cfg, err = load_child(root)
    if err:
        print(f"conformance_check: {err} (não avaliável)")
        return 2
    sys.path.insert(0, str(HERE))
    import doctor
    nd = catalog.parent / "migrations"
    if a.check_note:
        code, text = check_note(root, cfg, a.check_note, items, read_notes(nd))
        print(text)
        return code
    res = evaluate(root, cfg, doctor._today(cfg), items, child_has_screen(root, cfg), nd)
    gaps = [r for r in res if r["status"] == "gap"]
    unknown = [r for r in res if r["status"] == "unknown"]
    pend = pending(root, cfg, items, nd, child_has_screen(root, cfg), doctor._today(cfg))
    if a.json:
        print(json.dumps({"root": str(root),
                          "gaps": [{"id": r["id"], "severity": r["severity"], "message": describe(r),
                                    "grace_until": r["grace_until"].isoformat()} for r in gaps],
                          "unknown": [{"id": r["id"], "message": describe(r)} for r in unknown],
                          "pending": [n["id"] if n else it["migration"] for it, n in pend]}, ensure_ascii=False, indent=2))
    else:
        if a.pending:
            for it, n in pend:
                print(f"  {n['id'] if n else '(sem nota)'} · {it['id']}@{n['from'] if n else '?'}→{n['to'] if n else it['version']} → {it['owner_skill']}"
                      f" · {_pending_deadline(it, cfg, doctor._today(cfg))}")
        if a.gaps or not a.pending:
            for r in gaps:
                print(f"  [{r['severity']}] {describe(r)}")
            for r in unknown:
                print(f"  [não avaliável] {describe(r)}")
        print(f"conformance_check: {root.name}: {len(gaps)} lacuna(s), {len(unknown)} não avaliável(is), {len(pend)} nota(s) pendente(s)")
    if any(r["severity"] == "error" for r in gaps):
        return 1
    return 2 if unknown and not gaps else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
