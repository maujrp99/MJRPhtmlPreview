#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-09 · fonte 99b47e5 · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""prototype_sync_check.py -- a prototype, its screen inventory and its wireframes move together.

09/10/2026 19:36 (MJRP): the Control Center v3.5 changed after approval and its data went stale, but only 3 of its
7 screens had a wireframe and the info-arch.md still named the v3.3 as its source -- the rule existed only in prose
(structure_rules.json `wireframes`, mjrp-designing-ui), so it depended on the agent remembering. MJRP: "alterou
protótipo, automaticamente wireframe e info-arch precisam ser atualizados". Decided: hook + sensor; every version
of a prototype has the wireframe of every screen.

The rule:
  - a prototype is `design/inception/<name>-vN.html` (N may be dotted: v3.5);
  - every commit that adds or changes it also brings `docs/specs/info-arch.md` and the wireframes of that version,
    `design/wireframes/<name>-vN-<screen>.png`, one per screen;
  - the screens are those of the previous version that had wireframes, plus any new one; a screen dropped on
    purpose is declared in info-arch.md as `<!-- wireframe-retired: <screen> -->`;
  - info-arch.md names the newest prototype file (`<name>-vN.html`).

Modes:
  python3 prototype_sync_check.py <project root>
      drift report (doctor W14): prints one line per gap, always exits 0.
  python3 prototype_sync_check.py <repo root> --staged [--msg <commit message file>]
      commit gate (commit-msg hook): exit 1 blocks the commit.
Escape -- the human's call, written in the commit message: a trailer line `Prototype-sync: skip -- <reason>`.
"""
import re
import subprocess
import sys
from pathlib import Path

PROTO = re.compile(r"^(?P<name>[a-z0-9]+(?:-[a-z0-9]+)*)-v(?P<ver>\d+(?:\.\d+)*)\.html$")
STAGED_PROTO = re.compile(r"^(?P<proj>(?:.+/)?)design/inception/(?P<file>[^/]+\.html)$")
RETIRED = re.compile(r"<!--\s*wireframe-retired:\s*([a-z0-9-]+)\s*-->")
SKIP = re.compile(r"^Prototype-sync:\s*skip\b", re.I | re.M)
INFO_ARCH = Path("docs") / "specs" / "info-arch.md"
INCEPTION = Path("design") / "inception"
WIREFRAMES = Path("design") / "wireframes"
RULE_SINCE = "2026-10-09"   # the wireframes folder and this rule were born on this day; older prototypes are legacy


def vkey(ver):
    return tuple(int(x) for x in ver.split("."))


def prototypes(proj):
    """{name: [(version, path), ...] oldest first} for the prototypes in design/inception/."""
    out = {}
    d = proj / INCEPTION
    if not d.is_dir():
        return out
    for f in d.iterdir():
        m = PROTO.match(f.name)
        if f.is_file() and m:
            out.setdefault(m["name"], []).append((m["ver"], f))
    for name in out:
        out[name].sort(key=lambda x: vkey(x[0]))
    return out


def screens(proj, name, ver):
    """The screens that have a wireframe PNG for this version."""
    d = proj / WIREFRAMES
    prefix = f"{name}-v{ver}-"
    if not d.is_dir():
        return set()
    return {f.name[len(prefix):-4] for f in d.iterdir() if f.name.startswith(prefix) and f.name.endswith(".png")}


def retired(proj):
    p = proj / INFO_ARCH
    return set(RETIRED.findall(p.read_text(encoding="utf-8"))) if p.is_file() else set()


def required(proj, name, ver, versions):
    """Screens this version must have: the previous version's (with wireframes) minus the retired, plus its own."""
    prev = set()
    for v, _ in reversed([x for x in versions if vkey(x[0]) < vkey(ver)]):
        prev = screens(proj, name, v)
        if prev:
            break
    return (prev - retired(proj)) | screens(proj, name, ver)


def _git(root, *args):
    try:
        r = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return ""
    return r.stdout.strip() if r.returncode == 0 else ""


def _ctime(proj, path):
    """Unix time of the newest commit touching path; 0 when git does not know it."""
    out = _git(proj, "log", "-1", "--format=%ct", "--", str(path))
    return int(out) if out.isdigit() else 0


def drift(proj):
    """Gaps between the newest prototype of each name, its wireframes and info-arch.md (doctor W14)."""
    proj = Path(proj).resolve()   # git -C <proj> with absolute paths: a relative root would be read twice
    gaps = []
    for name, versions in sorted(prototypes(proj).items()):
        ver, path = versions[-1]
        rel = f"{INCEPTION}/{path.name}"
        when = _git(proj, "log", "-1", "--format=%cs", "--", str(path))
        if when and when < RULE_SINCE:
            continue
        have = screens(proj, name, ver)
        if not have:
            gaps.append(f"{rel}: nenhum wireframe desta versão em {WIREFRAMES}/ ({name}-v{ver}-<tela>.png)")
        missing = sorted(required(proj, name, ver, versions) - have)
        if missing:
            gaps.append(f"{rel}: falta o wireframe de {', '.join(missing)} (a versão anterior tinha; tela retirada "
                        f"se declara no info-arch.md com <!-- wireframe-retired: <tela> -->)")
        ia = proj / INFO_ARCH
        if not ia.is_file():
            gaps.append(f"{rel}: sem {INFO_ARCH} (o inventário da tela)")
        elif path.name not in ia.read_text(encoding="utf-8"):
            gaps.append(f"{INFO_ARCH} não cita o protótipo mais novo ({path.name})")
        t = _ctime(proj, path)
        if t:
            stale = [f"{INFO_ARCH}"] if ia.is_file() and _ctime(proj, ia) < t else []
            stale += [f"{name}-v{ver}-{s}.png" for s in sorted(have) if _ctime(proj, proj / WIREFRAMES / f"{name}-v{ver}-{s}.png") < t]
            if stale:
                gaps.append(f"{rel} mudou depois de: {', '.join(stale)}")
    return gaps


def staged_gaps(root, msg_text=""):
    """What a commit that adds or changes a prototype is missing (commit-msg gate)."""
    root = Path(root).resolve()
    if SKIP.search(msg_text or ""):
        return []
    out = _git(root, "diff", "--cached", "--name-only", "--diff-filter=AMR")
    staged = set(out.splitlines()) if out else set()
    gaps = []
    for s in sorted(staged):
        m = STAGED_PROTO.match(s)
        pm = PROTO.match(m["file"]) if m else None
        if not pm:
            continue
        prefix, name, ver = m["proj"], pm["name"], pm["ver"]
        proj = root / prefix if prefix else root
        if f"{prefix}{INFO_ARCH.as_posix()}" not in staged:
            gaps.append(f"{s}: o commit não traz {prefix}{INFO_ARCH.as_posix()} (o inventário acompanha o protótipo)")
        versions = prototypes(proj)
        need = required(proj, name, ver, versions.get(name, [(ver, None)]))
        wf = f"{prefix}{WIREFRAMES.as_posix()}/{name}-v{ver}-"
        staged_screens = {x[len(wf):-4] for x in staged if x.startswith(wf) and x.endswith(".png")}
        if not need and not staged_screens:
            gaps.append(f"{s}: o commit não traz nenhum wireframe da versão ({wf}<tela>.png)")
        missing = sorted(need - staged_screens)
        if missing:
            gaps.append(f"{s}: o commit não traz o wireframe refeito de {', '.join(missing)} ({wf}<tela>.png)")
    return gaps


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    root = Path(args[0]) if args else Path(".")
    if "--staged" in argv:
        msg = ""
        if "--msg" in argv:
            i = argv.index("--msg")
            if i + 1 < len(argv) and Path(argv[i + 1]).is_file():
                msg = Path(argv[i + 1]).read_text(encoding="utf-8", errors="replace")
        gaps = staged_gaps(root, msg)
        for g in gaps:
            print(f"  ✗ {g}")
        if gaps:
            print("\n  commit bloqueado: protótipo mudou sem o info-arch e os wireframes da versão no mesmo commit.\n"
                  "  refaça os wireframes de todas as telas (mjrp-designing-ui) e o info-arch; se não há o que refazer,\n"
                  "  a decisão é do humano: trailer 'Prototype-sync: skip — <motivo>' na mensagem.")
            return 1
        return 0
    for g in drift(root):
        print(f"  ! {g}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
