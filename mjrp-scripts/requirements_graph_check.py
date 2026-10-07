#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-07 · fonte 3d3763e · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""requirements_graph_check.py -- checks the requirements graph of a project against its single declaration,
requirements_graph_rules.json (S-63, kernel page requirements-graph).

Nodes: requirement and NFR files in docs/specs/requirements/ (frontmatter), epics in prd.md (heading + the
paragraph below it, which carries the inline edges and the ^EP-xx block anchor), outcomes and releases in
ROADMAP.md (^OUT-xx, ^REL-xx block anchors), observable states in info-arch.md and behavior.md (block anchors; a path-qualified link resolves in a nested project), features in
docs/specs/features/Fxx-slug/ (spec.md frontmatter; REQ-xx and TASK-xx are local IDs).

Edges are written in one direction only; each one is enforced only from the status the rules declare
(lesson of SDD_chain_artifacts_check, 16/09: checking every pattern in every pair gave 366 false positives).

Informational until it proves quiet (S-63 step 7): exits 0 and prints the findings. --strict exits 1 when there
are findings and 2 when the project has no requirements graph yet (contract: 0 passed, 1 failed, 2 not
evaluable). Python 3 stdlib only (constitution, ADR-0015: this is core).

Tags (MJRP 2026-10-06): every outcome carries 1-3 category tags (`tags:: #a #b` in its ROADMAP section); every
epic inherits them and may add up to 3 of its own. Free vocabulary: format and count only. --tags lists them.

Evidence (S-67, MJRP 2026-10-04): a status is checked against reality, never trusted. In progress needs an open
feature or recent activity; Done needs a Done feature or `delivered_by:` with the commit; Accepted also needs
`accepted_in:` pointing to the human's acceptance; Ready is warned when its observable state changed afterwards.

Usage:
  python3 mjrp-scripts/requirements_graph_check.py [root] [--strict] [--summary] [--tags] [--rules path]
  python3 mjrp-scripts/requirements_graph_check.py [root] --staged          (pre-commit: exit 1 on a contradiction in a staged node)
  python3 mjrp-scripts/requirements_graph_check.py [root] --changed --gate  (Stop hook: exit 2 on a contradiction in an uncommitted node)
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from doctor import read_yaml, log_rel  # same YAML reader and log path as the doctor -- no duplicate parser

WIKILINK = re.compile(r"\[\[([^\]|#]*)(?:#([^\]|]*))?(?:\|[^\]]*)?\]\]")
INLINE_FIELD = re.compile(r"^\s*(?:[-*]\s+)?([a-z_]+)::\s*(.+)$")
BLOCK_ANCHOR = re.compile(r"\s\^([A-Za-z0-9-]+)\s*$")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def frontmatter(text):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    data = read_yaml(text[3:end]) or {}
    return (data if isinstance(data, dict) else {}), text[end + 4:]


def as_list(v):
    if v is None or v == "":
        return []
    return v if isinstance(v, list) else [v]


def link_targets(value):
    """Every [[file#anchor]] in a value -> list of (file, id). id = anchor without ^, or the file stem."""
    out = []
    for item in as_list(value):
        for f, a in WIKILINK.findall(str(item)):
            f = f.strip()
            a = (a or "").strip()
            out.append((f, a.lstrip("^") if a else Path(f).stem))
    return out


def local_ids(value, pattern):
    return [m for item in as_list(value) for m in re.findall(pattern, str(item))]


class Graph:
    def __init__(self, root, rules):
        self.root = Path(root)
        self.rules = rules
        self.p = {k: self.root / v for k, v in rules["paths"].items()}
        self.types = rules["node_types"]
        self.nodes = {}      # id -> {"type", "file", "status", "edges": {name: [targets]}}
        self.features = {}   # fid -> {"status", "imports", "reqs": {REQ: verified_by[]}, "tasks": {TASK: [REQ]}, "dir"}
        self.findings = []

    def find(self, rule, msg):
        self.findings.append((rule, msg))

    def tags_field(self):
        return (self.rules.get("tags") or {}).get("field", "tags")

    def type_of(self, nid):
        for name, t in self.types.items():
            pat = t.get("id_pattern")
            if pat and t.get("form") != "local_id" and re.match(pat, nid) and name != "observable_state":
                return name
        return None

    # ---- loading ---------------------------------------------------------------------------
    def load_anchors(self, key, wanted_types):
        path = self.p.get(key)
        if not path or not path.exists():
            return
        section, tags_in, anchors_in = 0, {}, {}
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if HEADING.match(line):
                section += 1
            f = INLINE_FIELD.match(BLOCK_ANCHOR.sub("", line))
            if f and f.group(1) == self.tags_field():
                tags_in.setdefault(section, []).extend(f.group(2).replace(",", " ").split())
            m = BLOCK_ANCHOR.search(line)
            if not m:
                continue
            nid = m.group(1)
            anchors_in.setdefault(section, []).append(nid)
            t = self.type_of(nid)
            if key in ("info_arch", "behavior") and t is None:
                t = "observable_state"
            if t in wanted_types:
                edges = {}
                self.nodes[nid] = {"type": t, "file": path.name, "status": None, "edges": edges}
        # tags (MJRP, 2026-10-06): the `tags::` line of an outcome's section belongs to the outcome anchored in it
        for sec, tags in tags_in.items():
            outs = [a for a in anchors_in.get(sec, []) if (self.nodes.get(a) or {}).get("type") == "outcome"]
            if len(outs) == 1:
                self.nodes[outs[0]]["tags"] = tags
            elif len(outs) > 1:
                self.find("tags", f"{', '.join(outs)}: uma linha `tags::` numa seção com mais de um resultado — um resultado por seção")

    def load_inline_nodes(self, key, node_type):
        """Nodes that live inside a document: the heading names them, the paragraph below carries the inline
        edges and ends with the ^ID block anchor (Obsidian does not anchor headings)."""
        path = self.p.get(key)
        if not path or not path.exists():
            return
        pat = self.types[node_type]["id_pattern"].strip("^$")
        current = None
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            h = HEADING.match(line)
            if h:
                m = re.match(r"(" + pat + r")\b", h.group(2).strip())
                current = m.group(1) if m else None
                if current:
                    self.nodes.setdefault(current, {"type": node_type, "file": path.name, "status": None,
                                                    "edges": {}, "anchored": False})
                continue
            if not current:
                continue
            f = INLINE_FIELD.match(BLOCK_ANCHOR.sub("", line))
            if f and f.group(1) == "folder":
                self.nodes[current]["folder"] = f.group(2).strip().strip("`").strip("/")
            elif f and f.group(1) == self.tags_field():
                self.nodes[current].setdefault("tags", []).extend(f.group(2).replace(",", " ").split())
            elif f:
                self.nodes[current]["edges"].setdefault(f.group(1), []).extend(link_targets(f.group(2)))
            a = BLOCK_ANCHOR.search(line)
            if a and a.group(1) == current:
                self.nodes[current]["anchored"] = True

    def load_requirements(self):
        d = self.p["requirements"]
        for f in sorted(d.rglob("*.md")):
            if f.name.lower() in ("readme.md", "folder-index.md", "index.md"):
                continue
            raw = f.read_text(encoding="utf-8", errors="replace")
            fm, body = frontmatter(raw)
            # S-110 (MJRP, 2026-10-05): every node in each declared language, as a `## <lang>` section of the same file
            for lang in self.languages():
                sec = re.search(r"^## " + re.escape(lang) + r"\s*\n(.*?)(?=^## |\Z)", body or "", re.M | re.S)
                if not sec or not sec.group(1).strip():
                    self.find("bilingual", f"{f.name}: sem a seção `## {lang}` (ou vazia) — o nó vem nas línguas {', '.join(self.languages())}")
            nid = f.stem
            t = self.type_of(nid)
            if t not in ("requirement", "nfr"):
                self.find("node_id", f"{f.name}: o nome do arquivo não é um ID de requisito (S-, UC-, EA-, NFR-)")
                continue
            if fm.get("id") and str(fm.get("id")) != nid:
                self.find("node_id", f"{f.name}: frontmatter id '{fm.get('id')}' difere do nome do arquivo")
            status = fm.get("status")
            valid = self.rules["statuses"] + self.rules.get("off_track_statuses", [])
            if status not in valid:
                self.find("status", f"{nid}: status '{status}' fora da lista {valid}")
            edges = {}
            for e in self.rules["edges"]:
                if e["name"] in fm:
                    edges[e["name"]] = link_targets(fm[e["name"]])
            if nid in self.nodes and self.nodes[nid].get("path"):
                self.find("node_id", f"{nid}: dois arquivos com o mesmo ID ({self.nodes[nid]['path'].relative_to(d)}, {f.relative_to(d)})")
            self.nodes[nid] = {"type": t, "file": f.name, "path": f, "status": status, "edges": edges,
                               "delivered_by": [str(x).strip().strip("`") for x in as_list(fm.get("delivered_by"))],
                               "accepted_in": str(fm.get("accepted_in") or "").strip()}

    def load_features(self):
        d = self.p["features"]
        if not d.exists():
            return
        fpat = self.types["feature"]["folder_pattern"]
        for fd in sorted(x for x in d.iterdir() if x.is_dir()):
            if not re.match(fpat, fd.name):
                self.find("node_id", f"features/{fd.name}: pasta fora do padrão Fxx-slug")
                continue
            fid = fd.name[:3]
            spec = fd / "spec.md"
            tasks = fd / "tasks.md"
            fm, body = frontmatter(spec.read_text(encoding="utf-8")) if spec.exists() else ({}, "")
            feat = {"dir": fd.name, "status": fm.get("status"), "imports": link_targets(fm.get("imports")),
                    "reqs": {}, "tasks": {}}
            for f in ("spec.md", "plan.md", "tasks.md"):
                if not (fd / f).exists():
                    self.find("feature_files", f"{fd.name}: falta {f}")
            cur = None
            for line in body.splitlines():
                m = re.match(r"^(?:#{2,6}\s+|[-*]\s+(?:\*\*)?\[?)(REQ-\d{2,})\b", line)
                if m:
                    cur = m.group(1)
                    feat["reqs"].setdefault(cur, [])
                    continue
                f = INLINE_FIELD.match(line)
                if cur and f and f.group(1) == "verified_by":
                    feat["reqs"][cur].append(f.group(2).strip())
            if tasks.exists():
                cur = None
                for line in tasks.read_text(encoding="utf-8").splitlines():
                    m = re.match(r"^(?:#{2,6}\s+|[-*]\s+(?:\[[ xX]\]\s+)?(?:\*\*)?\[?)(TASK-\d{2,})\b", line)
                    if m:
                        cur = m.group(1)
                        feat["tasks"].setdefault(cur, [])
                        box = re.match(r"^[-*]\s+\[([ xX])\]", line)
                        if box and box.group(1) == " ":
                            feat.setdefault("open_tasks", []).append(cur)
                    m = re.search(r"implements::\s*(.+)$", line)
                    if cur and m:
                        feat["tasks"][cur].extend(local_ids(m.group(1), r"REQ-\d{2,}"))
            self.features[fid] = feat

    def load(self):
        self.load_anchors("roadmap", {"outcome", "release"})
        self.load_anchors("info_arch", {"observable_state"})
        self.load_anchors("behavior", {"observable_state"})
        self.load_inline_nodes("prd", "epic")
        self.load_requirements()
        self.load_features()

    # ---- checks ----------------------------------------------------------------------------
    def status_rank(self, s):
        """Position in the lifecycle; -1 for an off-track status (Deferred) or an unknown one -- never enforced."""
        st = self.rules["statuses"]
        return st.index(s) if s in st else -1

    def enforced(self, edge, status):
        frm = edge.get("enforced_from", "always")
        return frm == "always" or (status is not None and self.status_rank(status) >= self.status_rank(frm))

    def nested_anchor(self, f, tid):
        """A link with a path (`apps/control-center/docs/specs/info-arch#^x`) points into a nested project's own
        document: resolve the anchor there. Returns an observable_state node or None."""
        if "/" not in f:
            return None
        doc = self.root / (f if f.endswith(".md") else f + ".md")
        if not doc.exists():
            return None
        for line in doc.read_text(encoding="utf-8", errors="replace").splitlines():
            m = BLOCK_ANCHOR.search(line)
            if m and m.group(1) == tid:
                return {"type": "observable_state", "file": f, "status": None, "edges": {}}
        return None

    def check_target(self, src, edge, target):
        f, tid = target
        node = self.nested_anchor(f, tid) or self.nodes.get(tid)
        allowed = edge["to"] if isinstance(edge["to"], list) else [edge["to"]]
        if node is None:
            self.find("target_exists", f"{src} —{edge['name']}→ [[{f}{'#^' + tid if f and tid != Path(f).stem else ''}]]: alvo não existe")
        elif node["type"] not in allowed:
            self.find("edge_type", f"{src} —{edge['name']}→ {tid}: alvo é {node['type']}, a aresta pede {'/'.join(allowed)}")

    def check_node_edges(self):
        for nid, node in self.nodes.items():
            for edge in self.rules["edges"]:
                srcs = edge["from"] if isinstance(edge["from"], list) else [edge["from"]]
                if node["type"] not in srcs:
                    continue
                targets = node["edges"].get(edge["name"], [])
                if edge.get("to") == "acceptance":
                    # S-79: an acceptance is an anchor of uat.md or a log entry, not a node -- resolved by
                    # acceptance_resolves (the uat.md anchors were reported as missing targets before)
                    raw = node.get("accepted_in", "")
                    if raw and not self.acceptance_resolves(raw):
                        self.find("target_exists", f"{nid} —accepted_in→ {raw}: aceite não encontrado (âncora do uat.md ou entrada do log)")
                    continue
                for t in targets:
                    self.check_target(nid, edge, t)
                if not self.enforced(edge, node["status"]):
                    continue
                if len(targets) < edge["min"]:
                    self.find(f"edge_{edge['name']}", f"{nid}: precisa de pelo menos {edge['min']} aresta '{edge['name']}'"
                              + (f" (cobrada a partir de {edge['enforced_from']})" if edge.get("enforced_from") != "always" else ""))
                if edge.get("max") is not None and len(targets) > edge["max"]:
                    self.find(f"edge_{edge['name']}", f"{nid}: no máximo {edge['max']} aresta '{edge['name']}', tem {len(targets)}")
            if node["type"] == "epic" and not node.get("anchored", True):
                self.find("anchor", f"{nid}: o parágrafo abaixo do heading não termina com ^{nid}")

    def effective_tags(self, nid):
        """An outcome's own tags; an epic's own tags plus those of the outcome it serves (MJRP, 2026-10-06)."""
        node = self.nodes.get(nid) or {}
        tags = list(node.get("tags", []))
        if node.get("type") == "epic" and (self.rules.get("tags") or {}).get("epic_inherits", True):
            for _, out in node["edges"].get("serves", []):
                tags += [t for t in (self.nodes.get(out) or {}).get("tags", []) if t not in tags]
        return tags

    def check_tags(self):
        """MJRP, 2026-10-06: every outcome carries 1-3 category tags; every epic inherits them and may add up to 3
        of its own. Free vocabulary -- only the format and the count are checked."""
        spec = self.rules.get("tags")
        if not spec:
            return
        pat = re.compile(spec.get("pattern", r"^#[a-z0-9]+(-[a-z0-9]+)*$"))
        limits = {"outcome": spec.get("outcome", {}), "epic": spec.get("epic_own", {})}
        for nid, node in self.nodes.items():
            if node["type"] not in limits:
                continue
            own, lim = node.get("tags", []), limits[node["type"]]
            for t in own:
                if not pat.match(t):
                    self.find("tags", f"{nid}: tag '{t}' fora do formato (#kebab-case em inglês, ex.: #visual-management)")
            if len(set(own)) != len(own):
                self.find("tags", f"{nid}: tag repetida em `{spec.get('field', 'tags')}::`")
            if len(own) < lim.get("min", 0):
                self.find("tags", f"{nid}: resultado sem tag — declare de {lim.get('min', 1)} a {lim.get('max', 3)} em `{spec.get('field', 'tags')}:: #tag` na seção dele no ROADMAP")
            if lim.get("max") is not None and len(own) > lim["max"]:
                what = "tags próprias" if node["type"] == "epic" else "tags"
                self.find("tags", f"{nid}: {len(own)} {what}, o máximo é {lim['max']}")

    def release_of(self, rid):
        node = self.nodes.get(rid) or {}
        own = node.get("edges", {}).get("planned_for", [])
        if own:
            return own[0][1]
        epic = (node.get("edges", {}).get("epic") or [(None, None)])[0][1]
        via = (self.nodes.get(epic) or {}).get("edges", {}).get("planned_for", [])
        return via[0][1] if via else None

    def check_features(self):
        imp_edge = next(e for e in self.rules["edges"] if e["name"] == "imports")
        ver_edge = next(e for e in self.rules["edges"] if e["name"] == "verified_by")
        open_st = set(self.rules["open_feature_statuses"])
        open_by_req = {}
        for fid, ft in self.features.items():
            if len(ft["imports"]) < imp_edge["min"]:
                self.find("feature_has_requirement", f"{ft['dir']}: não importa nenhum requisito")
            for t in ft["imports"]:
                self.check_target(ft["dir"], imp_edge, t)
                node = self.nodes.get(t[1])
                if node and node["type"] == "nfr":
                    self.find("nfr_not_imported", f"{ft['dir']}: importa {t[1]}, um NFR — NFR é restrição de todas as features, não se importa")
                if ft["status"] in open_st:
                    open_by_req.setdefault(t[1], []).append(ft["dir"])
            implemented = {r for reqs in ft["tasks"].values() for r in reqs}
            for task, reqs in ft["tasks"].items():
                if not reqs:
                    self.find("edge_implements", f"{ft['dir']}/{task}: não implementa nenhum REQ")
                for r in reqs:
                    if r not in ft["reqs"]:
                        self.find("target_exists", f"{ft['dir']}/{task} —implements→ {r}: o REQ não existe no spec.md da feature")
            for req, ver in ft["reqs"].items():
                if req not in implemented:
                    self.find("spec_req_implemented", f"{ft['dir']}/{req}: nenhuma TASK o implementa")
                if self.enforced(ver_edge, ft["status"]) and len(ver) < ver_edge["min"]:
                    self.find("edge_verified_by", f"{ft['dir']}/{req}: feature {ft['status']} sem verified_by")
            rels = {self.release_of(t[1]) for t in ft["imports"]} - {None}
            if len(rels) > 1:
                self.find("feature_single_release", f"{ft['dir']}: importa requisitos de releases diferentes ({', '.join(sorted(rels))})")
        for rid, dirs in open_by_req.items():
            if len(dirs) > 1:
                self.find("one_open_feature", f"{rid}: importado por mais de uma feature aberta ({', '.join(dirs)}) — fatie o requisito")

    # ---- evidence: the status is checked against reality, not trusted (S-67, MJRP 2026-10-04) --------------
    def git(self, *args):
        try:
            r = subprocess.run(["git", *args], cwd=self.root, capture_output=True, text=True)
            return r.returncode, r.stdout.strip()
        except FileNotFoundError:
            return 127, ""

    def last_commit_ts(self, path):
        # --follow + no pure renames: moving a node into its epic's folder (S-123) is not activity on it
        follow = ["--follow", "--diff-filter=AMC"] if Path(path).is_file() else []
        code, out = self.git("log", "-1", *follow, "--format=%ct", "--", str(Path(path).relative_to(self.root)))
        return int(out) if code == 0 and out.isdigit() else None

    def commit_exists(self, sha):
        return bool(re.match(r"^[0-9a-f]{7,40}$", sha)) and self.git("cat-file", "-e", sha + "^{commit}")[0] == 0

    def languages(self):
        """Languages every node is written in (rules `languages`; the contract's
        mjrp_harness.requirements.languages overrides; [] turns the rule off)."""
        if getattr(self, "_langs", None) is not None:
            return self._langs
        langs = self.rules.get("languages", [])
        contract = self.root / ".mjrp-project.yml"
        if contract.exists():
            try:
                data = read_yaml(contract.read_text(encoding="utf-8")) or {}
                req = ((data.get("mjrp_harness") or {}).get("requirements") or {})
                if "languages" in req:
                    langs = req.get("languages") or []
            except Exception:
                pass
        self._langs = list(langs)
        return self._langs

    def stale_days(self):
        days = (self.rules.get("defaults") or {}).get("stale_days", 14)
        contract = self.root / ".mjrp-project.yml"
        if contract.exists():
            try:
                data = read_yaml(contract.read_text(encoding="utf-8")) or {}
                days = int(((data.get("mjrp_harness") or {}).get("requirements") or {}).get("stale_days", days))
            except Exception:
                pass
        return days

    def log_entries(self):
        """(timestamp 'YYYY-MM-DD HH:MM', text) of every entry of the project log."""
        if not hasattr(self, "_log"):
            try:
                text = (self.root / log_rel(self.root)).read_text(encoding="utf-8", errors="replace")
            except OSError:
                text = ""
            parts = re.split(r"(?m)^(?=## \[)", text)
            self._log = [(m.group(1), p) for p in parts for m in [re.match(r"## \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]", p)] if m]
        return self._log

    def now_local(self):
        try:
            from zoneinfo import ZoneInfo
            return datetime.now(ZoneInfo("America/Sao_Paulo")).replace(tzinfo=None)
        except Exception:
            return datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None)

    def recent_activity(self, nid, node, importers):
        limit = self.stale_days()
        ts = [self.last_commit_ts(node["path"])] + [self.last_commit_ts(self.p["features"] / ft["dir"]) for ft in importers]
        ts = [t for t in ts if t]
        if ts and (time.time() - max(ts)) <= limit * 86400:
            return True
        since = (self.now_local() - timedelta(days=limit)).strftime("%Y-%m-%d %H:%M")
        return any(stamp >= since and re.search(r"\b" + re.escape(nid) + r"\b", text) for stamp, text in self.log_entries())

    def acceptance_resolves(self, ref):
        m = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})", ref)
        if m:
            return any(stamp == m.group(1) for stamp, _ in self.log_entries())
        for f, tid in link_targets(ref):
            uat = self.p.get("uat")
            if uat and uat.exists() and Path(f).stem == uat.stem:
                return any(BLOCK_ANCHOR.search(l) and BLOCK_ANCHOR.search(l).group(1) == tid
                           for l in uat.read_text(encoding="utf-8").splitlines())
        return False

    def state_doc(self, f):
        if "/" in f:
            return self.root / (f if f.endswith(".md") else f + ".md")
        for key in ("behavior", "info_arch"):
            if self.p.get(key) and self.p[key].stem == Path(f).stem:
                return self.p[key]
        return None

    def shown_states(self, doc):
        """Block IDs listed in `shows::` lines of a screen-state doc -- the states an approved prototype shows."""
        shown = set()
        if not doc or not doc.exists():
            return shown
        for line in doc.read_text(encoding="utf-8", errors="replace").splitlines():
            f = INLINE_FIELD.match(line)
            if f and f.group(1) == "shows":
                shown.update(tid for _, tid in link_targets(f.group(2)))
        return shown

    def check_evidence(self):
        closed = {"Done", "Accepted"}
        open_st = set(self.rules["open_feature_statuses"])
        importers_of = {}
        for ft in self.features.values():
            for _, rid in ft["imports"]:
                importers_of.setdefault(rid, []).append(ft)
            if ft["status"] in closed and ft.get("open_tasks"):
                self.find("feature_done_tasks_open", f"{ft['dir']}: {ft['status']} com tarefa aberta ({', '.join(ft['open_tasks'])})")
        for nid, node in self.nodes.items():
            if node["type"] != "requirement":
                continue
            st, imps = node["status"], importers_of.get(nid, [])
            if st in closed:
                by_feature = any(ft["status"] in closed for ft in imps)
                bad = [s for s in node["delivered_by"] if not self.commit_exists(s)]
                by_commit = any(self.commit_exists(s) for s in node["delivered_by"])
                if not (by_feature or by_commit):
                    self.find("evidence_done", f"{nid}: {st} sem evidência — nenhuma feature Done o importa e "
                              + (f"`delivered_by` aponta commit que não existe ({', '.join(bad)})" if bad else "não há `delivered_by` com o commit que entregou"))
            if st == "Accepted" and not (node["accepted_in"] and self.acceptance_resolves(node["accepted_in"])):
                self.find("evidence_accepted", f"{nid}: Accepted sem `accepted_in` que aponte o aceite do humano (entrada do uat.md ou do log)")
            if st == "In progress" and not any(ft["status"] in open_st for ft in imps) and not self.recent_activity(nid, node, imps):
                self.find("status_stale", f"{nid}: In progress sem feature aberta e sem atividade em {self.stale_days()} dias "
                          "(commit no nó ou na feature, ou citação no log)")
            if st == "Ready":
                rts = self.last_commit_ts(node["path"])
                for f, tid in node["edges"].get("points_to", []):
                    doc = self.state_doc(f)
                    dts = self.last_commit_ts(doc) if doc and doc.exists() else None
                    if rts and dts and dts > rts:
                        self.find("ready_state_changed", f"{nid}: o estado observável ^{tid} ({doc.name}) mudou depois do Ready — o critério pode ter envelhecido")
                    # a screen state is judged when an approved prototype shows it; behavior states have no screen
                    if doc and doc.exists() and doc.stem == "info-arch" and tid not in self.shown_states(doc):
                        self.find("state_judged", f"{nid}: Ready aponta para ^{tid} ({doc.name}), que nenhum protótipo aprovado "
                                  "mostra — falta a linha `shows::` no registro em § Protótipos aprovados")

    TIME_RULES = {"status_stale", "ready_state_changed"}

    def next_phase(self, nid, node):
        """The next PDLC step for one requirement node, read from the graph (S-67)."""
        st, edges = node["status"], node["edges"]
        imps = [ft for ft in self.features.values() if nid in [r for _, r in ft["imports"]]]
        if st in ("Backlog", "Prioritized"):
            return ("promover a Ready (mjrp-writing-reqs)" if edges.get("points_to")
                    else "FASE 2: estado observável — tela no info-arch.md ou exemplos no behavior.md")
        if st == "Ready":
            return "SDD Specify — nova feature que o importe" if not imps else "SDD em curso na feature " + imps[0]["dir"]
        if st == "In progress":
            if not imps:
                return "trabalho em sessão, sem feature — evidência: commit e log"
            fd = self.p["features"] / imps[0]["dir"]
            for f, phase in (("spec.md", "Specify"), ("plan.md", "Plan"), ("tasks.md", "Tasks")):
                if not (fd / f).exists() or not (fd / f).read_text(encoding="utf-8").strip():
                    return f"SDD {phase} na feature {imps[0]['dir']}"
            return (f"Implement na feature {imps[0]['dir']}" if imps[0].get("open_tasks")
                    else f"qualidade e fechamento da feature {imps[0]['dir']}")
        if st == "Done":
            return "aceite do humano (uat.md)"
        if st == "Deferred":
            return "adiado — nada a fazer"
        return "nada a fazer"

    def summary(self):
        reqs = {n: v for n, v in self.nodes.items() if v["type"] == "requirement"}
        by = {}
        for v in reqs.values():
            by[v["status"]] = by.get(v["status"], 0) + 1
        order = self.rules["statuses"] + self.rules.get("off_track_statuses", [])
        print("[requirements_graph] resumo — requisitos por status: "
              + " · ".join(f"{s} {by[s]}" for s in order if s in by))
        if self.features:
            fs = {}
            for ft in self.features.values():
                fs[ft["status"]] = fs.get(ft["status"], 0) + 1
            print("  features por status: " + " · ".join(f"{k} {v}" for k, v in fs.items()))
        contradicted = {msg.split(":")[0] for rule, msg in self.findings}
        print("  próxima fase por nó (aberto):")
        for nid in sorted(reqs, key=lambda x: (x.split("-")[0], int(re.sub(r"\D", "", x) or 0))):
            v = reqs[nid]
            if v["status"] in ("Accepted",):
                continue
            step = "reconciliar primeiro (Guardian) — o status contradiz o grafo" if nid in contradicted else self.next_phase(nid, v)
            if v["status"] == "Done" and nid not in contradicted:
                continue
            print(f"    {nid} [{v['status']}] → {step}")

    def check_node_folder(self):
        """S-123 (MJRP, 2026-10-05): requirement files are grouped in one folder per epic. Dormant until the
        project's epics declare `folder::` in prd.md -- a project with a flat requirements/ is not judged."""
        epics = {nid: n for nid, n in self.nodes.items() if n["type"] == "epic"}
        if not any(n.get("folder") for n in epics.values()):
            return
        d = self.p["requirements"]
        nfr_dir = self.rules["paths"].get("nfr_folder", "nfr")
        seen = {}
        for nid, n in epics.items():
            fd = n.get("folder")
            if not fd:
                self.find("node_folder", f"{nid}: épico sem folder:: — os outros épicos declaram a pasta dos seus requisitos")
                continue
            if fd in seen:
                self.find("node_folder", f"{nid}: folder:: {fd} já é a pasta de {seen[fd]}")
            seen[fd] = nid
            if not re.match(r"^ep-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$", fd) or not fd.startswith(nid.lower() + "-"):
                self.find("node_folder", f"{nid}: folder:: {fd} fora do padrão {nid.lower()}-<slug-em-inglês>")
        for nid, n in self.nodes.items():
            if not n.get("path"):
                continue
            where = str(n["path"].parent.relative_to(d)).replace("\\", "/")
            if n["type"] == "nfr":
                want = nfr_dir
            else:
                ep = (n["edges"].get("epic") or [(None, None)])[0][1]
                want = (epics.get(ep) or {}).get("folder")
                if not want:
                    continue
            if where != want:
                self.find("node_folder", f"{nid}: está em requirements/{where if where != '.' else ''}, o lugar é requirements/{want}/")
        known = set(seen) | {nfr_dir}
        for sub in sorted(x for x in d.iterdir() if x.is_dir()):
            if sub.name not in known:
                self.find("node_folder", f"requirements/{sub.name}/: pasta que nenhum épico declara")

    def run(self):
        self.load()
        self.check_node_folder()
        self.check_node_edges()
        self.check_tags()
        self.check_features()
        self.check_evidence()
        return self.findings


def touched_nodes(root, rules, mode):
    """IDs of requirement nodes and feature dirs touched by the staged (--staged) or uncommitted (--changed) work."""
    # --name-status -M: a pure rename (R100) changes no node content, so it cannot bring a new contradiction --
    # moving the nodes into their epic's folder (S-123) must not re-judge the old findings they carry
    args = ["diff", "--cached", "--name-status", "-M"] if mode == "staged" else ["status", "--porcelain", "-uall"]
    try:
        out = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True).stdout
    except FileNotFoundError:
        return set()
    req, feat = rules["paths"]["requirements"].rstrip("/") + "/", rules["paths"]["features"].rstrip("/") + "/"
    ids = set()
    for line in out.splitlines():
        if mode == "staged":
            cols = line.split("\t")
            if cols[0] == "R100":
                continue
            p = cols[-1].strip()
        else:
            p = line[3:].strip().strip('"')
            if " -> " in p:
                p = p.split(" -> ")[-1].strip('"')
        if p.startswith(req) and p.endswith(".md"):
            ids.add(Path(p).stem)
        elif p.startswith(feat):
            ids.add(p[len(feat):].split("/")[0])
    return ids


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    strict = "--strict" in argv
    rules_path = HERE / "requirements_graph_rules.json"
    if "--rules" in argv:
        rules_path = Path(argv[argv.index("--rules") + 1])
        args = [a for a in args if a != str(rules_path)]
    root = Path(args[0] if args else ".").resolve()
    rules = json.loads(rules_path.read_text(encoding="utf-8"))
    if not (root / rules["paths"]["requirements"]).is_dir():
        if "--staged" in argv or "--changed" in argv:
            return 0
        print("[requirements_graph] sem docs/specs/requirements/ — projeto ainda sem grafo de requisitos (não avaliável)")
        return 2 if strict else 0
    g = Graph(root, rules)
    findings = g.run()
    mode = "staged" if "--staged" in argv else "changed" if "--changed" in argv else None
    if mode:
        # S-67: refuse only what THIS work introduces or touches - a contradiction in a node it touched. Time rules
        # (stale, state changed after Ready) are the daily pass's, never a reason to block a commit.
        nodes = touched_nodes(root, rules, mode)
        mine = [(r, m) for r, m in findings if r not in Graph.TIME_RULES and re.split(r"[:/ ]", m, 1)[0] in nodes]
        if not mine:
            return 0
        print(f"[requirements_graph] {len(mine)} contradição(ões) nos nós que este trabalho toca:")
        for r, m in mine:
            print(f"  [{r}] {m}")
        print("  conserte o status ou a evidência (delivered_by, accepted_in, tarefas) — ou reconcilie: kernel requirements-graph § Reconciliação")
        return 2 if "--gate" in argv else 1
    n_nodes = len(g.nodes)
    if "--summary" in argv:
        g.summary()
    if "--tags" in argv:
        # MJRP, 2026-10-06: the category of each outcome and epic -- an epic shows its own tags plus the inherited ones
        print("[requirements_graph] tags por resultado e épico:")
        for nid in sorted(n for n, v in g.nodes.items() if v["type"] in ("outcome", "epic")):
            v = g.nodes[nid]
            serves = ", ".join(t for _, t in v["edges"].get("serves", []))
            print(f"  {nid}{' → ' + serves if serves else ''}: {' '.join(g.effective_tags(nid)) or '(sem tag)'}")
    if not findings:
        print(f"[requirements_graph] VERDE — {n_nodes} nó(s), {len(g.features)} feature(s), nenhuma regra violada")
        return 0
    print(f"[requirements_graph] {len(findings)} achado(s) em {n_nodes} nó(s) e {len(g.features)} feature(s):")
    for rule, msg in findings:
        print(f"  [{rule}] {msg}")
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
