#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-05 · fonte b6f90ca · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
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
  - --amend is judged against the parent of the commit being amended;
  - going over it (git commit --no-verify) is the human's call, never the agent's.

The log path comes from the contract (`mjrp_harness.session_history`, for content projects Core/log.md);
default docs/log.md. Python 3 stdlib only (constitution, ADR-0015: this is core).

Usage:
  python3 mjrp-scripts/log_entry_check.py [--amend]     (from the hook: judges what is staged)
Exit: 0 passed or exempt · 1 blocked.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from doctor import log_rel  # the same contract reading as the doctor

ENTRY = re.compile(r"^## \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}\]", re.MULTILINE)
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


def log_path(root, project):
    rel = log_rel(Path(root) / project if project else Path(root))
    return f"{project}/{rel}" if project else rel


def entries(root, spec):
    code, text = git(root, "show", spec)
    return set(ENTRY.findall(text)) if code == 0 else set()


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
    fails = []
    for proj in touched:
        log = log_path(root, proj)
        if not (root / log).exists() and git(root, "cat-file", "-e", f":{log}")[0] != 0:
            continue  # project without a log yet (scaffold in progress): nothing to compare
        new = entries(root, f":{log}")
        old = entries(root, f"{base}:{log}") if has_head else set()
        if not (new - old):
            where = proj or "raiz"
            fails.append((where, log, "o commit não acrescenta entrada nova" if log in files
                          else "o log não está no commit"))
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
    print("  `TZ=America/Sao_Paulo date \"+%Y-%m-%d %H:%M\"` — S-61. Isentos: só derivado (folder-index.md, daily-checks/,")
    print("  _backups/), merge, script declarado. Ir por cima (--no-verify) é decisão do humano, nunca do agente.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
