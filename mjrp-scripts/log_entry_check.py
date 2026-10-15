#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-14 · fonte b714d244 · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""log_entry_check.py -- every commit brings a new entry in the project log (S-61).

Born 2026-10-03 17:48: in the skills revision, four commits went out with no entry in docs/log.md, and on
2026-10-04 a context compaction found the human's latest decisions only in the AI Platform's summary, not in
the repository. The git hook commit-msg calls this script, so it guards every session that commits -- local or
in the cloud, on any AI Platform -- because git runs where the repository is.

Rule (MJRP, 2026-10-04 14:11):
  - every commit adds at least one new entry heading (`## [YYYY-MM-DD HH:MM] <type>`) to the log of each project
    it touches (the harness root, or a nested project with its own .mjrp-project.yml, such as apps/<app>/);
  - exempt: a commit that touches only derived files (folder-index.md, daily-checks/, _backups/), a merge,
    and a commit made by a declared scaffold script (environment MJRP_LOG_EXEMPT, set by new_project.py);
  - the entry goes to the log of the OWNING project only (2026-10-13, ADR-0020 D.1, accepted by the MJRP): when a
    commit touches more than one project, (a) if it touches any path the root contract declares in
    `mjrp_harness.log_owner.root_paths` the owner is the root, else (b) the owner is the project with the most
    non-derived files touched (the logs themselves do not count), a tie going to the root. The commit needs a new entry in the owner's log; the other
    projects it touches are dispensed (an extra entry in their log is allowed, never required). The declaration is
    read from the committed root contract (HEAD), like `self_logged`: the rule is decided in the contract, never at
    commit time, and a commit cannot edit the rule it is judged by. Born from the root log carrying pointer entries
    ("detail in the Control Center log") because the check demanded an entry in both logs (ADR-0020, S7);
  - exempt per project, a file that carries its own history (2026-10-11, ADR-0004 of the Control Center, accepted
    by the MJRP): the contract declares `mjrp_harness.self_logged: [{path, history}]`, and a commit is exempt in that
    project only when (i) it touches, in that project, only declared paths, and (ii) the staged blob of each one has,
    in its JSON `history` list, at least one item the base blob does not have (compared item by serialized item, so
    trimming the oldest items does not matter). A hand edit with no new history item still needs the log entry.
    The declaration is read from the committed contract (HEAD), never from the working tree. Born from the
    Control Center's screen edit: its commit carried the agent's uncommitted log entry, and the agent's next commit
    was then refused for "no new entry" (audit 2026-10-10, finding #6);
  - --amend is judged against the parent of the commit being amended;
  - an entry is its whole heading line, so two entries in the same minute are two entries (2026-10-09: the second
    commit of a minute was refused as "no new entry");
  - a new entry's <type> is one of KINDS (2026-10-09 21:26: an entry went out as `decisão`, and the Control Center,
    which reads the log, broke on the unknown type);
  - going over it (git commit --no-verify) is the human's call, never the agent's.

The log path comes from the contract (`mjrp_harness.session_history`, for content projects Core/log.md);
default docs/log.md. Python 3 stdlib only (constitution, ADR-0015: this is core).

Usage:
  python3 mjrp-scripts/log_entry_check.py [--amend]     (from the hook: judges what is staged)
Exit: 0 passed or exempt · 1 blocked.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from doctor import CONTRACT, log_rel, read_yaml  # the same contract reading as the doctor

ENTRY = re.compile(r"^## \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\].*$", re.MULTILINE)
KIND = re.compile(r"^## \[[^\]]+\] *([^\s—]*)")
KINDS = ("session", "decision", "inventory", "ingest", "harness-feedback", "review")   # the types the logs use;
# review: a critique pass (UX, architecture) pointing to its report — MJRP, 2026-10-09 22:49
DERIVED_NAMES = ("folder-index.md",)
DERIVED_DIRS = ("daily-checks/", "_backups/")


def git(root, *args):
    r = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    return r.returncode, r.stdout


def is_derived(path):
    name = path.rsplit("/", 1)[-1]
    if name in DERIVED_NAMES:
        return True
    return any(("/" + path).find("/" + d) != -1 for d in DERIVED_DIRS)


def project_of(root, path, projects):
    """The nested project that owns the path (longest prefix), or '' for the root project."""
    best = ""
    for p in projects:
        if p and path.startswith(p + "/") and len(p) > len(best):
            best = p
    return best


def nested_projects(root):
    _, out = git(root, "ls-files", "*.mjrp-project.yml", ".mjrp-project.yml")
    found = set()
    for line in out.splitlines():
        d = str(Path(line).parent)
        found.add("" if d == "." else d)
    found.add("")
    return found


def root_paths(root):
    """The repo-relative paths the committed root contract declares as always the root's (`log_owner.root_paths`):
    a folder (ends in `/`) or a file. Empty when there is no declaration; read from HEAD, never from the working tree."""
    code, text = git(root, "show", f"HEAD:{CONTRACT}")
    if code != 0:
        return []
    try:
        owner = (read_yaml(text) or {}).get("mjrp_harness", {}).get("log_owner") or {}
        items = owner.get("root_paths") or []
    except (AttributeError, TypeError, ValueError):
        return []
    if isinstance(items, str):
        items = [x.strip() for x in items.strip("[] ").split(",") if x.strip()]
    return [str(x).strip() for x in items if str(x).strip()] if isinstance(items, list) else []


def is_root_path(path, declared):
    return any(path == d or (d.endswith("/") and path.startswith(d)) for d in declared)


def owner_of(root, content, projects):
    """The one project that owes the log entry of a commit that touches several (ADR-0020 D.1): the root when any
    file is under `root_paths`; else the project with the most non-derived files; a tie goes to the root."""
    if any(is_root_path(f, root_paths(root)) for f in content):
        return ""
    logs = {log_path(root, p) for p in projects}
    work = [f for f in content if f not in logs] or content   # the log is the record of the work, it does not vote
    count = {}
    for f in work:
        proj = project_of(root, f, projects)
        count[proj] = count.get(proj, 0) + 1
    top = max(count.values())
    leaders = sorted(p for p, n in count.items() if n == top)
    return "" if "" in leaders else leaders[0]


def log_path(root, project):
    rel = log_rel(Path(root) / project if project else Path(root))
    return f"{project}/{rel}" if project else rel


def entries(root, spec):
    code, text = git(root, "show", spec)
    return set(ENTRY.findall(text)) if code == 0 else set()


def self_logged(root, project):
    """{repo-relative path: history field} that the project's committed contract declares as self-logged."""
    contract = f"{project}/{CONTRACT}" if project else CONTRACT
    code, text = git(root, "show", f"HEAD:{contract}")
    if code != 0:
        return {}
    try:
        items = (read_yaml(text) or {}).get("mjrp_harness", {}).get("self_logged") or []
    except (AttributeError, TypeError, ValueError):
        return {}
    declared = {}
    for item in items if isinstance(items, list) else []:
        if isinstance(item, dict) and str(item.get("path") or "").strip():
            rel = str(item["path"]).strip().strip("/")
            declared[f"{project}/{rel}" if project else rel] = str(item.get("history") or "history").strip()
    return declared


def history_items(root, spec, field):
    """The items of the JSON list `field` in the blob `spec`, serialized; None when the blob is absent or not JSON."""
    code, text = git(root, "show", spec)
    if code != 0:
        return None
    try:
        items = json.loads(text).get(field)
    except (ValueError, AttributeError):
        return None
    if not isinstance(items, list):
        return None
    return {json.dumps(item, sort_keys=True, ensure_ascii=False) for item in items}


def self_logged_exempt(root, project, files, base, has_head):
    """True when every file of this project in the commit is self-logged and brings a new history item."""
    declared = self_logged(root, project)
    if not files or not declared or any(f not in declared for f in files):
        return False
    for f in files:
        new = history_items(root, f":{f}", declared[f])
        old = (history_items(root, f"{base}:{f}", declared[f]) or set()) if has_head else set()
        if not new or not (new - old):
            return False
    return True


def check(root, amend=False):
    """Returns a list of (project, log, reason) failures; empty list = pass."""
    if os.environ.get("MJRP_LOG_EXEMPT"):
        print(f"[log_entry] isento: commit de script declarado ({os.environ['MJRP_LOG_EXEMPT']})")
        return []
    code, gitdir = git(root, "rev-parse", "--git-dir")
    if code == 0 and (root / gitdir.strip() / "MERGE_HEAD").exists():
        return []
    _, staged = git(root, "diff", "--cached", "--name-only", "--no-renames")
    files = [f for f in staged.splitlines() if f.strip()]
    content = [f for f in files if not is_derived(f)]
    if not content:
        return []
    has_head = git(root, "rev-parse", "-q", "--verify", "HEAD")[0] == 0
    base = "HEAD~1" if amend else "HEAD"
    if amend and git(root, "rev-parse", "-q", "--verify", "HEAD~1")[0] != 0:
        has_head = False
    projects = nested_projects(root)
    touched = sorted({project_of(root, f, projects) for f in content})
    if len(touched) > 1:
        touched = [owner_of(root, content, projects)]   # ADR-0020 D.1: only the owner's log needs the entry
    fails = []
    for proj in touched:
        mine = [f for f in content if project_of(root, f, projects) == proj]
        if self_logged_exempt(root, proj, mine, base, has_head):
            print(f"[log_entry] isento ({proj or 'raiz'}): só arquivo self_logged, com histórico novo dentro dele")
            continue
        log = log_path(root, proj)
        if not (root / log).exists() and git(root, "cat-file", "-e", f":{log}")[0] != 0:
            continue  # project without a log yet (scaffold in progress): nothing to compare
        new = entries(root, f":{log}")
        old = entries(root, f"{base}:{log}") if has_head else set()
        where = proj or "raiz"
        if not (new - old):
            fails.append((where, log, "o commit não acrescenta entrada nova" if log in files
                          else "o log não está no commit"))
        for head in sorted(new - old):
            kind = KIND.match(head).group(1)
            if kind not in KINDS:
                fails.append((where, log, f"a entrada `{head[:60]}` tem o tipo `{kind or '(vazio)'}`, fora de "
                                          f"{', '.join(KINDS)}"))
    return fails


def main(argv):
    root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel")[1].strip() or ".")
    fails = check(root, amend="--amend" in argv)
    if not fails:
        return 0
    print("")
    for where, log, why in fails:
        print(f"  commit bloqueado ({where}): {why} em {log}.")
    print("  Toda mudança leva uma entrada `## [AAAA-MM-DD HH:MM] <tipo>` no log do projeto que ela toca, com a hora de")
    print("  `TZ=America/Sao_Paulo date \"+%Y-%m-%d %H:%M\"` — S-61. Num commit que toca mais de um projeto, a entrada vai")
    print("  ao log do projeto DONO (ADR-0020): a raiz se tocar algum `log_owner.root_paths` do contrato da raiz; senão o")
    print("  projeto com mais arquivos tocados; empate, a raiz. Isentos: só derivado (folder-index.md, daily-checks/,")
    print("  _backups/), merge, script declarado, arquivo self_logged com histórico novo dentro dele. Ir por cima")
    print("  (--no-verify) é decisão do humano, nunca do agente.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
