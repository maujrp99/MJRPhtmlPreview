#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-09-27 · fonte 55473fe · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""
doctor.py - the computational sensor of the harness.

Runs on any MJRP instance and returns an exit code. The criterion - which checks exist, why
each one exists, and what counts as error vs warning - lives in
docs/decisions/0002-doctor-verification-criteria.md (ADR-0002). This file is the
implementation; the ADR is the authority. On failure, every check names the incident that
created it: whoever reads the red understands why it is red.

  exit 0  green (warnings allowed)
  exit 1  at least one error
  exit 2  not evaluable (no contract, path missing) - neither green nor red

Usage:
  python3 mjrp-scripts/doctor.py [path]           evaluates the instance (runs the sensors)
  python3 mjrp-scripts/doctor.py --skip-sensors   uses the last recorded result
  python3 mjrp-scripts/doctor.py --json           machine-readable output
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time
from datetime import date, datetime
from pathlib import Path

try:
    import yaml                                    # when present, it is the one that parses
except ModuleNotFoundError:
    yaml = None                                    # when absent, the doctor parses on its own (see _yaml_min)


class YamlNaoSuportado(Exception):
    """The minimal parser hit YAML it cannot read. It SHOUTS instead of inventing."""


def _esc(v):
    v = v.strip()
    if not v or v.startswith("#"):
        return ""
    v = re.split(r"\s+#", v)[0].strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
    if v.startswith("{") and v.endswith("}"):
        d = {}
        for par in v[1:-1].split(","):
            if not par.strip():
                continue
            if ":" not in par:
                raise YamlNaoSuportado(f"mapa inline sem ':' — {v}")
            k, _, s = par.partition(":")
            d[k.strip()] = _esc(s)
        return d
    if v in ("true", "True"):
        return True
    if v in ("false", "False"):
        return False
    if v in ("null", "~", ""):
        return None
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return date.fromisoformat(v)               # F2 does arithmetic on dates: a string will not do
    return v


def _yaml_minimal(text):
    """Reads the subset of YAML the harness uses, without depending on PyYAML.

    Born from an incident: on 2026-09-08 the doctor did not run on the user's Mac because
    Homebrew 3.14 is externally managed and the contract's `pip install --user pyyaml` is
    refused. The doctor is the FRONT DOOR of any instance - requiring an install for it to run
    is friction exactly where there must be none.

    The first version SILENTLY DROPPED BLOCK LISTS: gates_open became a loose map, F2 saw no
    gate at all, and the report came out green by silence (2026-09-09, found by the selftest
    running on the user's machine). It now RAISES YamlNaoSuportado on anything it cannot read -
    and the doctor exits 2, not evaluable. A sensor that invents is worse than a sensor that is
    missing.
    """
    lines = []
    for bruta in text.splitlines():
        if not bruta.strip() or bruta.lstrip().startswith("#"):
            continue
        if bruta.lstrip().startswith(("%", "---", "...", "&", "*", "<<")):
            raise YamlNaoSuportado(f"construção fora do subconjunto — {bruta.strip()[:40]}")
        lines.append((len(bruta) - len(bruta.lstrip()), bruta.strip(), bruta))

    def block(i, ind):
        """Return (value, next index) of the block starting at i with indentation >= ind."""
        if i < len(lines) and lines[i][1].startswith("- "):
            seq = []
            while i < len(lines) and lines[i][0] >= ind and lines[i][1].startswith("- "):
                body = lines[i][1][2:].strip()
                # The ':' that decides scalar-vs-map has to be looked for in the body WITHOUT
                # its inline comment, and outside quotes. Otherwise `- pasta/  # nota: assim`
                # becomes a dict whose key is the path plus the comment. Found on 2026-09-10 by
                # doctor_selftest, which compares this parser against PyYAML on the real contract.
                escopo = "" if body[:1] in ("\"", "'") else re.split(r"\s+#", body)[0].strip()
                if body.startswith("{") or ":" not in escopo:
                    seq.append(_esc(body))
                    i += 1
                else:                              # an item that is a multi-line map
                    k, _, resto = body.partition(":")
                    item = {}
                    if resto.strip():
                        item[k.strip()] = _esc(resto)
                    i += 1
                    while i < len(lines) and lines[i][0] > ind and not lines[i][1].startswith("- "):
                        kk, _, vv = lines[i][1].partition(":")
                        item[kk.strip()] = _esc(vv)
                        i += 1
                    seq.append(item)
            return seq, i
        mapa = {}
        while i < len(lines):
            atual, body, _bruta = lines[i]
            if atual < ind:
                break
            if ":" not in body:
                raise YamlNaoSuportado(f"linha sem ':' fora de lista — {body[:40]}")
            chave, _, resto = body.partition(":")
            chave, resto = chave.strip(), resto.strip()
            if resto.startswith("#"):              # `key:   # comment` is still a block
                resto = ""
            elif not resto.startswith(("\"", "'")):
                resto = re.split(r"\s+#", resto)[0].strip()
            if resto in (">", "|", ">-", "|-"):    # bloco dobrado
                i += 1
                buf = []
                while i < len(lines) and lines[i][0] > atual:
                    buf.append(lines[i][1])
                    i += 1
                # o `>` do YAML termina em uma quebra (modo clip) — igualar ao PyYAML
                mapa[chave] = (" ".join(buf).strip() + "\n") if resto.startswith(">") and not resto.endswith("-") else " ".join(buf).strip()
            elif resto == "":
                if i + 1 < len(lines) and lines[i + 1][0] > atual:
                    mapa[chave], i = block(i + 1, lines[i + 1][0])
                elif i + 1 < len(lines) and lines[i + 1][1].startswith("- ") and lines[i + 1][0] == atual:
                    mapa[chave], i = block(i + 1, atual)       # lista alinhada com a chave
                else:
                    mapa[chave] = {}
                    i += 1
            else:
                mapa[chave] = _esc(resto)
                i += 1
        return mapa, i

    valor, _ = block(0, 0)
    return valor


def read_yaml(text):
    """PyYAML when available; the minimal parser when not. The doctor runs either way."""
    if yaml is not None:
        try:
            return yaml.safe_load(text) or {}
        except Exception:
            return {}
    return _yaml_minimal(text) or {}
    sys.exit(2)

CONTRACT = ".mjrp-project.yml"
SENSOR_CACHE = ".mjrp/sensors.json"
SENSOR_TIMEOUT = 300
# Cache format version. A record written by an older doctor has no fingerprint and cannot be
# trusted to describe the current tree - it is read as stale, not as a pass.
SENSOR_CACHE_VERSION = 2
# Paths that a sensor result must NOT depend on: they are produced BY the run. Without this
# filter the fingerprint would change every time the doctor writes its own cache, and no record
# would ever match the state that follows it. Same list the stop_gate uses, for the same reason.
DERIVED = ("__pycache__", "/.mjrp/", "_backups/", "dist/", "mjrp-skills-packages/",
           "daily-checks/")  # 16/09: o proprio rastro de aviso/erro nao pode invalidar
                              # o cache de sensor que ele mesmo atualiza (BACKLOG #60)
IDENTITY_DOCS = ["AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md", "VISION.md"]
INSTALLED_DIRS = [".agent/skills", "skills", ".claude/skills"]

ERRO, AVISO = "erro", "aviso"


class Report:
    def __init__(self):
        self.findings = []   # (id, level, msg, incident)
        self.notes = []      # (id, text) - what was evaluated and passed, or could not be evaluated

    def fail(self, cid, msg, incident):
        self.findings.append((cid, ERRO, msg, incident))

    def warn(self, cid, msg, incident):
        self.findings.append((cid, AVISO, msg, incident))

    def note(self, cid, msg):
        self.notes.append((cid, msg))

    @property
    def errors(self):
        return [f for f in self.findings if f[1] == ERRO]

    @property
    def warnings_(self):
        return [f for f in self.findings if f[1] == AVISO]


def sh(cmd, cwd, timeout=30):
    try:
        p = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), text=True,
                           capture_output=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, f"estourou {timeout}s"
    except Exception as e:
        return 127, str(e)


def git_toplevel(root):
    """A working tree do git a que `root` pertence, ou None. Sobe até um `.git` de ANCESTRAL:
    um subprojeto aninhado (apps/<app>/, sem `.git` próprio) conta como 'sob git' pelo repo do
    pai — achado 21/09: F3/W4 iam vermelho num nested legítimo. `.git` na própria raiz segue
    sendo o caso comum; nested é reconhecido, não penalizado."""
    code, out = sh(["git", "rev-parse", "--show-toplevel"], root)
    if code == 0 and out:
        return Path(out.splitlines()[0].strip())
    return None


def normalize_skill_text(text):
    """Forma canônica de um SKILL.md para hash. Ignora o que o empacotador/Cowork reescreve sem
    mudar o sentido: a linha `name:` (vira slug), a FORMA do `description:` (bloco `>` multilinha
    na fonte vs. linha única entre aspas no Cowork — achado 19/09: 20 falsos positivos no #62),
    espaço à direita e quebra de linha. O corpo fica intacto."""
    t = text.replace("\r\n", "\n")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", t, re.S)
    if not m:
        return "\n".join(l.rstrip() for l in t.split("\n")).strip()
    fm, body = m.group(1), m.group(2)
    lines = fm.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not km:
            i += 1
            continue
        key, val = km.group(1), km.group(2).strip()
        if val in (">", "|", ">-", "|-"):
            buf = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or lines[i].strip() == ""):
                buf.append(lines[i].strip())
                i += 1
            val = " ".join(x for x in buf if x)
        else:
            i += 1
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
            q = val[0]
            val = val[1:-1].replace("\\" + q, q)
        if key == "name":
            continue
        val = re.sub(r"\s+", " ", val).strip()
        out.append(f"{key}: {val}")
    canon = "\n".join(sorted(out)) + "\n---\n" + "\n".join(l.rstrip() for l in body.split("\n")).strip()
    return canon.strip()


def skill_digest(path):
    """Hash do conteúdo canônico (ver normalize_skill_text) — mesmo algoritmo do
    cowork_sync_check.skill_digest(texto); mudou aqui, muda lá."""
    t = path.read_text(encoding="utf-8", errors="replace")
    return hashlib.sha256(normalize_skill_text(t).encode()).hexdigest()[:16]


def frontmatter(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    if not m:
        return {}
    try:
        return read_yaml(m.group(1)) or {}
    except Exception:
        return {}


def find_skills(base, dirs):
    """{nome: caminho do SKILL.md} varrendo <base>/<dir>/**/SKILL.md."""
    out = {}
    for d in dirs:
        root = base / d
        if not root.is_dir():
            continue
        for f in root.rglob("SKILL.md"):
            out.setdefault(f.parent.name, []).append(f)
    return out


# ─────────────────────────────────────────────────────────────── checagens

def c1_conformance(root, cfg, rep):
    """instalado × fonte: sobra, divergiu por hash, duplicata."""
    inc = "22 skills que não existem mais na fonte no htmlPreview; 9 de 9 no visual-notes-hub; duplicatas ativas no mesmo diretório"
    # 17/09 (BACKLOG #63): C1 só enxerga INSTALLED_DIRS no filesystem local. O cache de sync do
    # Cowork (/root/.claude/skills/synced/<bucket>/) só existe dentro de uma sessão Cowork ativa
    # e nunca foi lido por este check, em nenhum ambiente - rodando daqui (device_bash/Mac) ou de
    # dentro do próprio Cowork. Sem esta linha o veredito de C1 é lido como "a instalação está
    # ok" quando o enunciado real é "o que dá para ver do disco está ok" - foi essa confusão que
    # deixou 39/54 skills divergentes 8 dias sem nenhum sensor acusar (achado 17/09). Verificação
    # de verdade é o #62, ainda não construído.
    rep.note("C1", "Cowork (skills sincronizadas numa sessão ativa) não verificado por este "
                   "check - só vê o filesystem local; ver BACKLOG #62/#63")
    if cfg.get("profile") == "meta":
        rep.note("C1", "n/a — este repositório é a fonte")
        return
    installed = find_skills(root, INSTALLED_DIRS)
    if not installed:
        rep.warn("C1", "nenhuma skill instalada nesta instância", inc)
        return
    src_root = Path(os.path.expanduser(cfg.get("source", "~/mjrp/projects/mjrp-harness")))
    if not (src_root / "mjrp-skills").is_dir():
        rep.warn("C1", f"fonte não encontrada em {src_root} — conformidade não avaliada", inc)
        return
    source = find_skills(src_root, ["mjrp-skills"])
    for name, paths in sorted(installed.items()):
        if len(paths) > 1:
            rep.fail("C1", f"'{name}' instalada em {len(paths)} lugares: " +
                     ", ".join(str(p.relative_to(root)) for p in paths), inc)
        if name not in source:
            rep.fail("C1", f"'{name}' instalada e não existe mais na fonte (fantasma)", inc)
        elif skill_digest(paths[0]) != skill_digest(source[name][0]):
            rep.fail("C1", f"'{name}' divergiu da fonte (hash diferente)", inc)
    for name in installed:
        alt = name[5:] if name.startswith("mjrp-") else "mjrp-" + name
        if alt in installed:
            rep.fail("C1", f"'{name}' e '{alt}' instaladas juntas — roteamento ambíguo", inc)
            break
    rep.note("C1", f"{len(installed)} skills instaladas conferidas contra a fonte")


SCHEMA = {
    "version": str, "profile": str, "process_level": str, "context": str,
    "gates": list, "gate_sla_days": int, "gates_open": list,
    "stack": dict,         # QUEM FAZ O QUE - atribuicao de papel (§5.2.1 da proposta)
    "tech_stack": dict,    # 15/09: a tecnologia do PRODUTO - nao tinha campo, e ia parar no stack:
    "models": dict, "environment": dict, "sensors": dict,
    "orchestration": str, "source": str,
    # `inventory`: as pastas que a skill mjrp-inventory audita (09/09). Entrou no contrato
    # before the schema - W3 flagged it, which is exactly its job.
    "inventory": list,
    "locale": dict,        # 10/09: timezone, labels, content - what skills and sensors read instead of assuming
    "memory": dict,        # 10/09: pending_expiry_days, layer0_budget_chars - the form of ## Now (F1)
    "kernel": dict,        # 14/09: version, source, pages - the wiki kernel this project carries (I5)
    "tools": dict,         # 14/09: category -> tool, one per category (docs/wiki/tools-catalog.md)
    # 16/09: chain, globs, id_patterns - read by SDD_chain_artifacts_check.py, never by A1 (BACKLOG
    # #58) - that script warns, it does not gate, so it lives outside `sensors:` on purpose.
    "sdd_chain": dict,
    # 19/09 (EP-07): the child projects whose docs/harness-feedback/ the harness_feedback_check.py
    # sweeps into docs/wiki/feedback-from-other-projects/ - folder names, siblings of this repo.
    "children": list,
    "children_root": str,  # optional: where the children live when they are not siblings of this repo
}
ENUMS = {
    "profile": {"code-app", "content", "meta"},
    "process_level": {"minimal", "standard", "full"},
    "context": {"eager", "lazy"},
    "orchestration": {"assisted", "autonomous"},
}


# 15/09: `stack:` e `tech_stack:` sao dois campos com nomes parecidos e sentidos opostos. O
# incidente: a wiki inverteu os dois em 14/09, e no dia seguinte 5 contratos foram preenchidos
# pela inversao. Isto NAO fixa valor - so reconhece as chaves que so fazem sentido em tech_stack.
CHAVES_DE_TECNOLOGIA = {
    "frontend", "backend", "hosting", "database", "language", "framework", "runtime",
    "build", "styling", "router", "testing", "lint", "ci", "secrets", "platform",
    "scripting", "data_source", "file_storage", "auth", "apis", "rendering",
}
PAPEIS = {"strategy", "build", "review", "design", "owns_loop", "ops", "content"}


def w6_stack_sense(cfg, rep):
    """`stack:` diz quem faz o que; a tecnologia do produto e `tech_stack:` (§5.2.1)."""
    inc = ("14/09 a wiki inverteu os sentidos de `stack:` e `models:`; em 15/09 cinco contratos "
           "foram preenchidos pela inversao antes de alguem abrir a §5.2.1")
    stack = cfg.get("stack")
    if not isinstance(stack, dict):
        return
    # `build` e `design` sao papeis E chaves de tecnologia - so contam as inequivocas
    suspeitas = sorted((set(stack) & CHAVES_DE_TECNOLOGIA) - PAPEIS)
    if suspeitas:
        rep.warn("W6", f"`stack:` tem {', '.join(suspeitas)} — isso parece tecnologia do produto, "
                       f"que e campo `tech_stack:`; `stack:` e atribuicao de papel (§5.2.1)", inc)


def i1_contract(cfg, rep):
    inc = "o marker do careertransition declara charter, destinations e notes — campos que a spec não prevê"
    if "ceremony" in cfg and "process_level" not in cfg:
        rep.fail("I1", "contrato usa `ceremony:`, renomeado para `process_level:` em 11/09/2026 "
                       "(em ágil, cerimônia é ritual; o campo mede quanto do método o projeto roda)", inc)
    for k in ("version", "profile", "process_level"):
        if k not in cfg:
            rep.fail("I1", f"contrato sem campo obrigatório '{k}'", inc)
    for k, v in cfg.items():
        if k not in SCHEMA:
            rep.warn("W3", f"contrato tem campo desconhecido '{k}' — a instância está à frente da spec", inc)
        elif not isinstance(v, SCHEMA[k]):
            rep.fail("I1", f"contrato: '{k}' deveria ser {SCHEMA[k].__name__}, veio {type(v).__name__}", inc)
        elif k in ENUMS and v not in ENUMS[k]:
            rep.fail("I1", f"contrato: '{k}: {v}' fora do domínio {sorted(ENUMS[k])}", inc)
    _i1_environment(cfg, rep)
    w6_stack_sense(cfg, rep)
    if not rep.errors:
        rep.note("I1", "contrato válido contra o schema")


def _i1_environment(cfg, rep):
    """The contract declares an environment; nothing checked that it holds HERE.

    The cheap half only. `environment.setup` is a command with side effects, and the doctor
    runs on every SessionStart - running it would be the harness installing things behind the
    user's back. The entry_check runs it (and clones the repo to do so), which is why it takes
    90 seconds and stays OUT of `sensors:`. What is left for here is what is both cheap and
    daily: does the runtime this contract requires exist on the machine reading it.
    """
    inc = ("08/09: o Zé rodou o doctor no Mac e teve que criar um venv à mão — o contrato "
           "declarava `pip install --user pyyaml`, que o Homebrew externally-managed recusa, "
           "e nada conferia que o `environment` declarado valia naquela máquina")
    env = cfg.get("environment")
    if not isinstance(env, dict) or not env:
        rep.warn("W3", "contrato sem `environment` — não há como saber o que a instância exige", inc)
        return
    if not str(env.get("setup", "")).strip():
        rep.fail("I1", "contrato: `environment.setup` vazio — declare `nenhum` se não há "
                       "pré-requisito; em branco não é o mesmo que nenhum", inc)
    faltando = []
    for prog in sorted(set(re.findall(r"\b(git|gh|node|npm|python3|uv|docker)\b",
                                     str(env.get("runtime", ""))))):
        if shutil.which(prog) is None:
            faltando.append(prog)
    if faltando:
        rep.fail("I1", f"contrato: `environment.runtime` exige {', '.join(faltando)}, "
                       f"que não está nesta máquina", inc)
    else:
        rep.note("I1", f"environment: runtime declarado disponível aqui")


ABS_PATH = re.compile(r"[`'\"( ](~?/Users/[A-Za-z0-9._-]+/[^\s`'\")\]]+)")


def i2_paths(root, cfg, rep, skill_files):
    """Every declared path exists. An absolute path outside the project is only evaluated
    where that filesystem can be seen - the manual audit already produced a false MISSING by
    running from a place that could not see the folders."""
    inc = "mjrp-vault-ops aponta para um vault que não está lá; três skills ainda citam /Users/mpedroso (Mac anterior); mjrp-adr grava em docs/architecture/, aposentado pela ADR-0001"
    checked, cegos, cegos_ns = 0, 0, set()
    vistos = set()

    def judge(raw, origem):
        """Evaluate the path only if this computer can see its namespace (/Users, /home).
        A path belonging to ANOTHER user is evaluable and must fail - that is how three skills
        kept pointing at the previous Mac with nothing flagging it."""
        nonlocal checked, cegos
        p = os.path.expanduser(raw.rstrip(".,;:"))
        ns = "/" + p.lstrip("/").split("/")[0]          # /Users, /home, /opt…
        if not Path(ns).is_dir():
            cegos += 1
            cegos_ns.add(ns)
            return
        checked += 1
        if not Path(p).exists() and (origem, p) not in vistos:
            vistos.add((origem, p))
            rep.fail("I2", f"{origem}: caminho declarado não existe — {p}", inc)

    for f in skill_files:
        for m in ABS_PATH.finditer(f.read_text(encoding="utf-8", errors="replace")):
            judge(m.group(1), f.parent.name)
    for key in ("setup", "runtime"):
        for m in re.finditer(r"(?<![\w-])(~?/[A-Za-z0-9._/-]{4,})", str(cfg.get("environment", {}).get(key, ""))):
            judge(m.group(1), f"contrato environment.{key}")

    msg = f"{checked} caminho(s) absoluto(s) verificado(s)"
    if cegos:
        msg += (f"; {cegos} em {', '.join(sorted(cegos_ns))} não avaliáveis nesta máquina"
                " — rode o doctor onde o projeto vive")
    rep.note("I2", msg)


def _wiki_targets(root):
    """Everything a [[wikilink]] may resolve to: concept page, declared alias, terms.md entry
    and ADR. Empty => wikilinks are not evaluable."""
    targets = set()
    conc = root / "docs" / "wiki"
    if conc.is_dir():
        # 14/09: the kernel copied by new_project.py lives in docs/wiki/harness/ and links to
        # itself ([[terms]], [[base-concept]]); those pages are part of this project's wiki.
        for f in (list(conc.glob("*.md")) + list((conc / "harness").glob("*.md"))
                  + list((conc / "kernel").glob("*.md"))):
            targets.add(f.stem.lower())
            al = frontmatter(f).get("aliases") or []
            if isinstance(al, str):
                al = re.split(r",\s*", al.strip("[] "))
            for a in al:
                a = str(a).strip().strip("'\"")
                if a:
                    targets.add(a.lower())
    dec = root / "docs" / "decisions"
    if dec.is_dir():
        for f in dec.glob("[0-9]*.md"):
            targets.add("adr-%s" % f.stem.split("-")[0])
    return targets


def i3_links(root, rep):
    inc = "a renomeação para mjrp-harness quebrou dois caminhos no visual-notes-hub sem que nada acusasse"
    inc_wiki = "a revisão de 07/09 tirou definições do VISION apontando para páginas de conceito que não existiam, e nada acusou"
    docs = [root / d for d in IDENTITY_DOCS] + sorted((root / "docs").rglob("*.md"))
    targets = _wiki_targets(root)
    n = nw = 0
    for doc in docs:
        if not doc.exists() or "_backups" in doc.parts or "_archive" in doc.parts:
            continue
        n += 1
        txt = doc.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\]\(([^)#\s]+?)(?:#[^)]*)?\)", txt):
            t = m.group(1)
            if t.startswith(("http://", "https://", "mailto:")):
                continue
            if not (doc.parent / t).exists():
                rep.fail("I3", f"{doc.relative_to(root)}: link para '{t}' não existe", inc)
        # wikilinks: [[target]] or [[target|text]]. Inside code it is an example, not a reference.
        sem_codigo = re.sub(r"```.*?```", "", txt, flags=re.S)
        sem_codigo = re.sub(r"`[^`\n]*`", "", sem_codigo)
        for m in re.finditer(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]", sem_codigo):
            target = m.group(1).strip().lower()
            nw += 1
            if targets and target not in targets:
                rep.fail("I3", f"{doc.relative_to(root)}: wikilink [[{m.group(1).strip()}]] não resolve "
                               f"(nem página em docs/wiki/, nem alias, nem ADR)", inc_wiki)
    rep.note("I3", f"{n} documentos conferidos · {nw} wikilink(s)")


def i4_agents(root, rep):
    inc = "dois projetos com CLAUDE.md, dois com GEMINI.md, nenhum com AGENTS.md: instrução divergente por ferramenta"
    if not (root / "AGENTS.md").exists():
        rep.fail("I4", "AGENTS.md não existe — é o canônico (ADR-0001)", inc)
        return
    for name in ("CLAUDE.md", "GEMINI.md"):
        f = root / name
        if f.exists() and "AGENTS.md" not in f.read_text(encoding="utf-8", errors="replace"):
            rep.fail("I4", f"{name} não aponta para AGENTS.md — vira segunda fonte de instruções", inc)
    rep.note("I4", "AGENTS.md canônico, ponteiros ok")


def i5_principles_inheritance(root, rep):
    # 14/09: um projeto novo, aberto direto no Gemini sem passar por onboarding/bootstrap, não
    # declarou a herança do PRINCIPLES.md em lugar nenhum — nem AGENTS.md nem constitution.md a
    # mencionavam. PRINCIPLES.md §III é claro: são exatamente três coisas que um constitution.md
    # faz, e a primeira é "declara a herança". Sem meio-termo, então é ERRO, não aviso.
    inc = ("14/09: projeto bootstrapado fora do Claude Code (Gemini, sem onboarding/bootstrap) "
           "não declarou a herança do PRINCIPLES.md em AGENTS.md nem em constitution.md")
    agents = root / "AGENTS.md"
    if not agents.exists():
        return  # I4 já cobre a ausência do arquivo; não duplicar o erro aqui
    agents_txt = agents.read_text(encoding="utf-8", errors="replace")
    if "PRINCIPLES.md" in agents_txt:
        rep.note("I5", "herança do PRINCIPLES.md declarada em AGENTS.md")
        return
    const = root / "docs" / "specs" / "constitution.md"
    if const.exists() and "PRINCIPLES.md" in const.read_text(encoding="utf-8", errors="replace"):
        rep.note("I5", "herança do PRINCIPLES.md declarada em constitution.md")
        return
    rep.fail("I5", "nem AGENTS.md nem docs/specs/constitution.md declaram a herança do "
                   "PRINCIPLES.md (PRINCIPLES.md §III: \"este projeto segue o PRINCIPLES.md do "
                   "MJRP Harness, versão X\") — herdar não é opcional", inc)


def w6_charter_not_migrated(root, rep):
    # mesmo incidente do I5: o Gemini criou um CHARTER.md cheio (não o stub de 5 linhas do
    # retrofit) sem nenhum docs/specs/prd.md — exatamente o padrão que a migração CHARTER→PRD
    # (BACKLOG #33/#44) deveria ter aposentado. Aviso, não erro: um brownfield em retrofit
    # legítimo também pode ter um CHARTER.md grande por um tempo, e o doctor não julga isso —
    # só torna visível.
    inc = ("14/09: CHARTER.md completo (não-stub) sem prd.md correspondente num projeto aberto "
           "fora do fluxo de bootstrap — parece charter novo, não retrofit em andamento")
    charter = root / "CHARTER.md"
    if not charter.exists():
        return
    linhas = len(charter.read_text(encoding="utf-8", errors="replace").splitlines())
    prd = root / "docs" / "specs" / "prd.md"
    if linhas > 10 and not prd.exists():
        rep.warn("W6", f"CHARTER.md tem {linhas} linhas (não é o stub de 5 linhas do retrofit) e "
                       f"não existe docs/specs/prd.md — CHARTER.md foi substituído pelo PRD "
                       f"(mjrp-project-bootstrap, PRD Writing Guide); se é retrofit em andamento, "
                       f"ignore", inc)


def now_section(text):
    """The lines of the ## Now section of MEMORY.md - the part that overwrites.
    Without the section, returns None: the file lost its active memory."""
    lines = text.splitlines()
    ini = None
    for i, l in enumerate(lines):
        if l.strip().lower() == "## now":
            ini = i + 1
            break
    if ini is None:
        return None
    body = []
    for l in lines[ini:]:
        if l.startswith("## ") or l.startswith("# "):
            break
        if l.strip() and not l.startswith(">") and not l.strip().startswith("*(") and l.strip() != "---":
            body.append(l)
    return body


NOW_BLOCKS = ("Where the Work Stopped", "Pending on Agent", "Pending on Human", "Do Not Forget")
PENDING_BLOCKS = ("Pending on Agent", "Pending on Human")
_PTR_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
_ISO_RE = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
_DM_RE = re.compile(r"\((\d{2})/(\d{2})\)")


def _today(cfg):
    tz = ((cfg or {}).get("locale") or {}).get("timezone", "America/Sao_Paulo")
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo(tz)).date()
    except Exception:
        return date.today()


def _latest_date(text, today):
    found = [date(int(y), int(m), int(d)) for y, m, d in _ISO_RE.findall(text)]
    found += [date(today.year, int(m), int(d)) for d, m in _DM_RE.findall(text)]
    return max(found) if found else None


def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def now_shape(root, text, cfg=None):
    """The FORM of ## Now (ADR-0008 §5, amended 10/09): four blocks, pointers instead of detail,
    pending items dated and fresh, nothing that AGENTS.md already says. Returns
    (fails, warns, notes). Line counts are notes - never a verdict: a line cap as an error made
    the agent cut exactly the Pending/Do-Not-Forget lines that keep the next session from erring."""
    cfg = cfg or {}
    mem = cfg.get("memory") or {}
    expiry = int(mem.get("pending_expiry_days", 7))
    budget = int(mem.get("layer0_budget_chars", 12000))
    fails, warns, notes = [], [], []
    body = now_section(text)
    if body is None:
        return ["MEMORY.md não tem seção '## Now' — a memória ativa sumiu (ADR-0006)"], warns, notes
    blocks, order, cur = {}, [], None
    for l in body:
        s = l.strip()
        hit = next((b for b in NOW_BLOCKS if s.startswith(f"**{b}")), None)
        if hit:
            cur = hit
            order.append(hit)
            blocks[cur] = [s]
        elif cur:
            blocks[cur].append(s)
    missing = [b for b in NOW_BLOCKS if b not in blocks]
    if missing:
        fails.append(f"## Now sem o(s) bloco(s) {', '.join(missing)} — os quatro são a forma (ADR-0008 §5)")
    if order != [b for b in NOW_BLOCKS if b in blocks]:
        warns.append("## Now com os blocos fora da ordem — a leitura é sempre a mesma: parou, meu, dele, não esquecer")
    names, aliases = set(), set()
    wiki = root / "docs" / "wiki"
    if wiki.exists():
        for p in wiki.rglob("*.md"):
            names.add(p.stem)
            m = re.search(r"^aliases:\s*\[(.*?)\]", p.read_text(encoding="utf-8", errors="replace")[:2000], re.M)
            if m:
                aliases.update(a.strip().strip("'\"") for a in m.group(1).split(","))
    today = _today(cfg)
    nptr = 0
    for b, ls in blocks.items():
        txt = " ".join(ls)
        ptrs = [p.strip() for p in _PTR_RE.findall(txt)]
        nptr += len(ptrs)
        for ptr in ptrs:
            if ptr not in names and ptr not in aliases:
                fails.append(f"## Now aponta para [[{ptr}]] e não existe docs/wiki/{ptr}.md (nem alias) — "
                             f"ponteiro que não resolve é detalhe perdido")
        n = len(ls)
        if b != "Do Not Forget" and n > 3 and not ptrs:
            fails.append(f"bloco '{b}' com {n} linhas e nenhum ponteiro — detalhe que mora no lugar errado; "
                         f"o que não cabe em duas linhas vira [[página]] ou data no log")
        if n > 6:
            warns.append(f"bloco '{b}' com {n} linhas — virou histórico?")
        if b in PENDING_BLOCKS and n > 1:
            latest = _latest_date(txt, today)
            if latest is None:
                warns.append(f"'{b}' sem data — não dá para saber se está parado")
            elif (today - latest).days > expiry:
                warns.append(f"'{b}' parado há {(today - latest).days} dias (limite {expiry}, "
                             f"memory.pending_expiry_days) — estado morto ou por reescrever")
    agents = root / "AGENTS.md"
    if agents.exists():
        ag = _norm(agents.read_text(encoding="utf-8", errors="replace"))
        for l in body:
            s = re.sub(r"^\*\*[^*]+\*\*\s*", "", l.strip())
            if len(s) >= 40 and _norm(s) in ag:
                warns.append(f"## Now repete o que o AGENTS.md já diz: \"{s[:60]}…\" — custo fixo sem informação")
    lines = text.splitlines()
    layer0 = 0
    keep = False
    for l in lines:
        if l.startswith("## "):
            keep = l.startswith("## Now") or l.startswith("## Ways of Working")
        if keep:
            layer0 += len(l) + 1
    idx = wiki / "index.md"
    if idx.exists():
        layer0 += len(idx.read_text(encoding="utf-8", errors="replace"))
    if layer0 > budget:
        warns.append(f"camada 0 (## Now + ## Ways of Working + wiki/index.md) com {layer0} chars — "
                     f"orçamento {budget} (memory.layer0_budget_chars); mover detalhe para página")
    notes.append(f"## Now: {len(body)} linhas, {len(blocks)}/4 blocos, {nptr} ponteiro(s) · "
                 f"camada 0: {layer0} chars (orçamento {budget})")
    return fails, warns, notes


KERNEL_STALE_DAYS = 30
# a fonte do kernel: a wiki do harness em que este doctor.py mora
HARNESS_WIKI = Path(__file__).resolve().parents[1] / "docs" / "wiki"   # same calendar logic as W5: a copy nobody refreshed in a month is suspect


def i5_kernel(root, cfg, rep):
    """The wiki kernel the project declares is really there, and its stamp is not stale.

    14/09: an agent inside fin-control had no way to know what log.md or ## Ways of Working
    are - the pages that define them live only in the harness. new_project.py now copies a
    stamped kernel into docs/wiki/harness/ and declares it in the contract; this is the check
    that the declaration and the disk agree (same shape as the PRINCIPLES.md inheritance).
    """
    inc = ("14/09: fin-control não tinha como saber o que log.md e ## Ways of Working são — os "
           "conceitos moravam só no harness, e a onboarding lê a wiki do projeto")
    if cfg.get("profile") == "meta":
        return   # the source does not carry a copy of itself
    k = cfg.get("kernel")
    if not k:
        rep.warn("I5", "contrato sem `kernel:` — o projeto não carrega os conceitos do harness; "
                       "rode `new_project.py --refresh-kernel <pasta>`", inc)
        return
    pages = k.get("pages") or []
    if isinstance(pages, str):
        pages = [x.strip() for x in pages.strip("[] ").split(",") if x.strip()]
    faltam = [pg for pg in pages if not (root / "docs" / "wiki" / "harness" / f"{pg}.md").exists()]
    if faltam:
        rep.fail("I5", f"kernel declarado no contrato mas {len(faltam)} página(s) ausente(s) em "
                       f"docs/wiki/harness/: {', '.join(faltam[:4])} — declaração sem disco é a "
                       f"herança de mentira que o I5 existe para pegar", inc)
    v = k.get("version")
    try:
        vd = v if isinstance(v, date) else datetime.strptime(str(v), "%Y-%m-%d").date()
        idade = (date.today() - vd).days
    except (TypeError, ValueError):
        rep.fail("I5", f"kernel.version inválido ({v!r}) — esperado AAAA-MM-DD", inc)
        return

    # 16/09: o carimbo media IDADE, nunca CONTEUDO. Os 4 projetos ficaram com 3 paginas
    # desatualizadas (terms, adr-practice, harness-concept) no mesmo dia em que foram
    # carimbados, e o check disse VERDE - carimbo novo, conteudo velho. Um kernel so esta em
    # dia se o texto bate com a fonte; a data e pista, nao prova.
    if idade > KERNEL_STALE_DAYS:
        rep.warn("I5", f"kernel carimbado há {idade} dias (versão {vd}) — mesmo que o texto "
                       f"confira, faz tempo que ninguém verifica; rode `--refresh-kernel`", inc)

    velhas = _kernel_divergentes(root, pages)
    if velhas is None:
        rep.note("I5", f"kernel: {len(pages)} página(s), versão {vd} — fonte não alcançável "
                       f"daqui, só a idade foi conferida")
    elif velhas:
        rep.fail("I5", f"kernel com {len(velhas)} página(s) DIVERGENTE(S) da fonte: "
                       f"{', '.join(velhas[:4])} — carimbo de {vd} mas o conteúdo envelheceu; "
                       f"rode `new_project.py --refresh-kernel <pasta>`",
                 "16/09: os 4 projetos foram carimbados e no mesmo dia 3 páginas do kernel "
                 "mudaram no harness; o I5 media só a idade e disse VERDE")
    else:
        rep.note("I5", f"kernel: {len(pages)} página(s) conferidas contra a fonte, versão {vd}, "
                       f"fonte {k.get('source', '?')}")

    # 18/09: PRINCIPLES.md e doctor.py entraram no kernel como `vendored` (arquivos fora da
    # wiki, mesmo carimbo) - mesma checagem de existencia+divergencia das paginas.
    inc_v = ("18/09: PRINCIPLES.md e doctor.py eram só referência (um caminho de texto quebrado, "
             "`<caminho-do-harness>`) até virarem cópia carimbada - sem eles no disco, ou "
             "desatualizados, o projeto não roda o próprio sensor nem sabe o que herdou")
    vendored = k.get("vendored") or []
    if isinstance(vendored, str):
        vendored = [x.strip() for x in vendored.strip("[] ").split(",") if x.strip()]
    if vendored:
        faltam_v = [ven for ven in vendored if not (root / ven).exists()]
        if faltam_v:
            rep.fail("I5", f"kernel declara {len(faltam_v)} arquivo(s) vendorizado(s) "
                           f"ausente(s): {', '.join(faltam_v)} — rode `new_project.py "
                           f"--refresh-kernel <pasta>`", inc_v)
        velhas_v = _vendored_divergentes(root, vendored)
        if velhas_v is None:
            rep.note("I5", f"vendorizados: {len(vendored)} arquivo(s), versão {vd} — fonte não "
                           f"alcançável daqui, só a idade foi conferida")
        elif velhas_v:
            rep.fail("I5", f"{len(velhas_v)} arquivo(s) vendorizado(s) DIVERGENTE(S) da fonte: "
                           f"{', '.join(velhas_v)} — rode `new_project.py --refresh-kernel "
                           f"<pasta>`", inc_v)
        elif not faltam_v:
            rep.note("I5", f"vendorizados: {len(vendored)} arquivo(s) conferidos contra a "
                           f"fonte, versão {vd}")


def _kernel_divergentes(root, pages):
    """Quais paginas do kernel do projeto divergem do que a fonte GERARIA hoje.

    Nao adivinha a transformacao: importa a mesma funcao que carimba
    (new_project.kernel_page_text) e compara o texto gerado com o que esta no disco do
    projeto, ignorando so a linha do banner - que carrega versao e hash, e muda por
    construcao. Uma fonte da verdade para o carimbo (II.9): se a regra de carimbar mudar,
    o check acompanha sozinho.

    Devolve None quando a fonte nao e alcancavel daqui - ai o check cai para so a idade.
    """
    try:
        import new_project as npj
    except Exception:
        return None
    # 18/09: HARNESS_WIKI é sempre parents[1]/docs/wiki de QUEM ESTÁ RODANDO - quando doctor.py
    # é a cópia vendorizada dentro de um projeto-filho, isso aponta pro docs/wiki DO FILHO (que
    # existe: tem harness/ e index.md), não pro harness de verdade. Sem exigir a subpasta
    # kernel/ (só a fonte tem), o loop abaixo só dava `continue` em toda página e devolvia lista
    # vazia - "0 divergente" por engano, não "não dá pra saber".
    if not (HARNESS_WIKI and (HARNESS_WIKI / "kernel").is_dir()):
        return None
    fora = []
    for pg in pages:
        cop = root / "docs" / "wiki" / "harness" / f"{pg}.md"
        if not cop.exists() or not (HARNESS_WIKI / "kernel" / f"{pg}.md").exists():
            continue
        try:
            esperado = npj.kernel_page_text(pg, "x", "x")
        except Exception:
            return None
        if _sem_banner(esperado) != _sem_banner(cop.read_text(encoding="utf-8", errors="replace")):
            fora.append(pg)
    return fora


def _sem_banner(texto):
    """O texto sem a linha do carimbo, que carrega versao e hash e difere por construcao."""
    return "\n".join(l for l in texto.splitlines()
                     if not l.startswith("<!-- kernel do MJRP Harness")
                     and not l.startswith("<!-- cópia carimbada do MJRP Harness")
                     and not l.startswith("# cópia carimbada do MJRP Harness")
                     and not l.startswith('  "_vendored": "cópia carimbada do MJRP Harness')).strip()


def _vendored_divergentes(root, vendored):
    """Mesma logica de _kernel_divergentes (18/09), pra PRINCIPLES.md e doctor.py - arquivos
    vendorizados fora da wiki, carimbados pelo mesmo new_project.py (vendored_file_text)."""
    try:
        import new_project as npj
    except Exception:
        return None
    if not npj.HARNESS_ROOT.is_dir():
        return None
    fora = []
    for dest_rel in vendored:
        cop = root / dest_rel
        src_rel = dest_rel   # VENDORED_FILES hoje mapeia 1:1 (mesmo caminho relativo)
        if not cop.exists() or not (npj.HARNESS_ROOT / src_rel).exists():
            continue
        try:
            esperado = npj.vendored_file_text(src_rel, "x", "x")
        except Exception:
            return None
        if _sem_banner(esperado) != _sem_banner(cop.read_text(encoding="utf-8", errors="replace")):
            fora.append(dest_rel)
    return fora


SPECKIT_MIRROR = Path(".specify") / "memory" / "constitution.md"
GENERATED_MARK = "GERADO de docs/specs/constitution.md"


def w7_kernel_downstream(root, cfg, rep):
    """Do lado da FONTE: mudei uma pagina do kernel - quem ficou defasado?

    16/09: o I5 passou a conferir o conteudo do kernel, mas so do lado do PROJETO - alguem
    tem que abrir o projeto para descobrir. Mudar `terms.md` aqui nao avisava nada, e foi
    assim que os 4 ficaram defasados no mesmo dia em que foram carimbados. Este e o espelho:
    rodando no harness, varre as pastas irmas e diz quem precisa de `--refresh-kernel`.

    E AVISO, nao erro: o harness nao e dono do ciclo de vida dos filhos, e um projeto pode
    estar legitimamente parado. Mas nao saber e o que nao pode continuar.
    """
    if cfg.get("profile") != "meta":
        return   # so a fonte olha para baixo
    inc = ("16/09: 3 paginas do kernel mudaram no harness e os 4 projetos seguiram com a copia "
           "velha; o I5 so acusa quando alguem abre o projeto, e ninguem abriu")
    vizinhos = sorted(d for d in root.parent.iterdir()
                      if d.is_dir() and d != root and (d / CONTRACT).exists())
    if not vizinhos:
        return
    defasados, conferidos = [], 0
    for d in vizinhos:
        try:
            raw = read_yaml((d / CONTRACT).read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        c = raw.get("mjrp_harness") or {}
        k = c.get("kernel")
        if not k:
            continue
        pages = k.get("pages") or []
        if isinstance(pages, str):
            pages = [x.strip() for x in pages.strip("[] ").split(",") if x.strip()]
        fora = _kernel_divergentes(d, pages)
        if fora is None:
            continue
        conferidos += 1
        if fora:
            defasados.append(f"{d.name} ({len(fora)}: {', '.join(fora[:3])})")
    if defasados:
        rep.warn("W7", f"{len(defasados)} projeto(s) com o kernel defasado desta fonte — "
                       f"{' · '.join(defasados)}. Rode `new_project.py <pasta> --refresh-kernel`", inc)
    elif conferidos:
        rep.note("W7", f"kernel: {conferidos} projeto(s) vizinho(s) em dia com esta fonte")


def i5_constitution_generated(root, cfg, rep):
    """The SpecKit copy of the constitution is GENERATED, never a second written one.

    PRINCIPLES.md Part III: a project keeps two copies of the constitution - docs/specs/ and
    .specify/memory/, where SpecKit expects it - and they must be "one written and one
    generated, never two written". The incident the rule was born from: in 2 of 5 projects they
    had already diverged. 14/09, MJRPpersonal: they diverged again, and nothing saw it.
    """
    inc = ("2 dos 5 projetos com constitution.md divergente entre docs/specs/ e .specify/memory/; "
           "14/09, no retrofit do MJRPpersonal, divergiam de novo e nada acusava")
    if cfg.get("profile") == "meta":
        return   # the harness has no constitution of its own
    fonte = root / "docs" / "specs" / "constitution.md"
    espelho = root / SPECKIT_MIRROR
    if not espelho.exists():
        return   # no SpecKit copy: nothing to diverge
    if not fonte.exists():
        rep.fail("I5", f"{SPECKIT_MIRROR} existe sem a fonte docs/specs/constitution.md — "
                       f"a cópia gerada virou a única, e ninguém sabe do que ela foi gerada", inc)
        return
    texto = espelho.read_text(encoding="utf-8", errors="replace")
    if GENERATED_MARK not in texto:
        rep.fail("I5", f"{SPECKIT_MIRROR} não se declara gerada — sem o marcador, é uma SEGUNDA "
                       f"ESCRITA, e duas escritas divergem (PRINCIPLES III)", inc)
        return
    corpo = texto.split("-->", 1)[-1].lstrip("\n")
    if corpo.strip() != fonte.read_text(encoding="utf-8", errors="replace").strip():
        rep.fail("I5", f"{SPECKIT_MIRROR} se declara gerada mas **divergiu** da fonte — "
                       f"regenere de docs/specs/constitution.md", inc)
    else:
        rep.note("I5", "constitution: a cópia do SpecKit é gerada e bate com a fonte")


def f1_memory(root, rep, cfg=None):
    inc = "o foco atual vivia enterrado na última entrada de um log.md de 400 linhas — lido por último, escrito por último"
    cur = root / "MEMORY.md"
    if not cur.exists():
        rep.fail("F1", "MEMORY.md não existe — memória ativa sem casa (ADR-0006)", inc)
        return
    # 08→09/09: em 36 horas o arquivo foi de 0 a 452 linhas e 8.558 tokens em TODA sessão, 42%
    # do custo fixo, porque decisão e aprendizado moravam nele. Nada acusava o crescimento.
    inc_08 = ("08→09/09: o MEMORY.md chegou a 452 linhas e 8.558 tokens em toda sessão — 42% do "
              "custo fixo — e nenhum sensor via o arquivo crescer")
    texto = cur.read_text(encoding="utf-8", errors="replace")
    linhas = texto.splitlines()
    # 10/09: the line caps (## Now <= 20, file <= 40) stopped being verdicts. As errors they made
    # the agent cut exactly the Pending/Do-Not-Forget lines that keep the next session from
    # erring - the sensor optimised the proxy, not the goal. What F1 verifies now is the FORM:
    # four blocks, pointers instead of detail, pending items dated and fresh (now_shape).
    fails, warns, _notes = now_shape(root, texto, cfg)
    for m in fails:
        rep.fail("F1", m, inc)
    for m in warns:
        rep.warn("F1", m, inc_08)
    for m in _notes:
        rep.note("F1", m)
    # A section that ADR-0008 ordered emptied coming back means the write half regressed: a
    # decision was filed here instead of on the subject's page.
    # 10/09: a ghost line "## Ways of Working`, `## History`…" left by a bad slice passed this
    # check because it compared by PREFIX. Titles are compared exactly - a section is its name.
    voltou = [t for t in linhas if t.startswith("## ")
              and t.strip() not in ("## Now", "## Ways of Working")]
    if voltou:
        rep.fail("F1", f"MEMORY.md tem seção que a ADR-0008 esvaziou: {', '.join(voltou)} — "
                       f"decisão mora na página do assunto, não aqui", inc_08)
    code, out = sh(["git", "log", "-1", "--format=%ct"], root)
    if code == 0 and out.isdigit() and os.path.getmtime(cur) < int(out) - 60:
        rep.fail("F1", "MEMORY.md é mais velho que o último commit — houve trabalho sem registrar", inc)
    rep.note("F1", f"MEMORY.md: {len(linhas)} linhas (contagem informativa — o veredito é a forma)")


# --- the episodic half of memory: docs/log.md and the growth of ## Ways of Working ------------
LOG_HEADER = "# log — o que aconteceu, em ordem"
LOG_ENTRY = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})( \d{2}:\d{2})?\] (session|decision|ingest|inventory|harness-feedback)\b.* — ")
LOG_TIME_REQUIRED_FROM = "2026-09-10"   # the hour became mandatory on this date (log.md header)
WOW_LINES_PER_DAY_WARN = 4              # corrections of conduct do not arrive in batches


def f1_log_shape(root, rep):
    """The episodic memory keeps its shape: canonical header, parseable dated entries.

    14/09: a child project (fin-control) had docs/log.md titled "Histórico de Decisões do
    Projeto" and MEMORY.md ## Ways of Working with 12 lines in one day, all delivery
    milestones. Nothing here looked at log.md at all, and F1 only measured Ways of Working by
    size. The root was in this repository: new_project.py wrote "uma linha datada por decisão"
    into every new log.md - the template taught the wrong frame.
    """
    inc = ("14/09: fin-control nasceu com log.md 'Histórico de Decisões' e 12 marcos de entrega em "
           "## Ways of Working num só dia — o template do new_project.py dizia 'linha por decisão'")
    log = root / "docs" / "log.md"
    if not log.exists():
        return   # F1/I3 already handle the missing file; legacy paths are the onboarding's job
    linhas = log.read_text(encoding="utf-8", errors="replace").splitlines()
    primeira = next((l.strip() for l in linhas if l.strip()), "")
    if primeira != LOG_HEADER:
        rep.fail("F1", f"docs/log.md abre com '{primeira[:60]}' — o cabeçalho canônico é "
                       f"'{LOG_HEADER}': o log é episódico (o QUANDO), decisão mora na wiki", inc)
    ruins, sem_hora = [], []
    for l in linhas:
        if not l.startswith("## "):
            continue
        m = LOG_ENTRY.match(l)
        if not m:
            ruins.append(l[:70])
        elif m.group(2) is None and m.group(1) >= LOG_TIME_REQUIRED_FROM:
            sem_hora.append(m.group(1))
    if ruins:
        rep.fail("F1", f"{len(ruins)} entrada(s) do log.md fora do formato "
                       f"'## [AAAA-MM-DD HH:MM] tipo — título' (ex.: {ruins[0]!r}) — sem o "
                       f"prefixo, o log deixa de responder por data e por grep", inc)
    if sem_hora:
        rep.warn("F1", f"{len(sem_hora)} entrada(s) do log.md sem hora depois de "
                       f"{LOG_TIME_REQUIRED_FROM} (a primeira: {sem_hora[0]}) — duas do mesmo dia "
                       f"perdem a ordem entre si", inc)


def f1_wow_growth(root, rep):
    """## Ways of Working grows one correction at a time; a batch is delivery history in disguise."""
    inc = ("14/09: fin-control acumulou 12 linhas em ## Ways of Working num só dia — "
           "'parametrizado', 'aprovado', 'gerada' — e o F1 só media o tamanho")
    cur = root / "MEMORY.md"
    if not cur.exists():
        return
    texto = cur.read_text(encoding="utf-8", errors="replace")
    i = texto.find("## Ways of Working")
    if i == -1:
        return
    hoje = date.today().isoformat()
    de_hoje = [l for l in texto[i:].splitlines() if l.startswith("- **" + hoje)]
    if len(de_hoje) > WOW_LINES_PER_DAY_WARN:
        rep.warn("F1", f"## Ways of Working ganhou {len(de_hoje)} linhas datadas de hoje (aviso a "
                       f"partir de {WOW_LINES_PER_DAY_WARN + 1}) — correção de conduta não vem em "
                       f"lote; marco de entrega mora no log.md, decisão mora na wiki", inc)


def f2_gates(cfg, rep):
    inc = "albumblender-v1 parado 166 dias exatamente num gate; visual-notes-hub, 184"
    sla = cfg.get("gate_sla_days", 14)
    abertos = cfg.get("gates_open") or []
    for g in abertos:
        if not isinstance(g, dict) or "since" not in g:
            rep.fail("F2", f"gate aberto sem data: {g}", inc)
            continue
        d = g["since"] if isinstance(g["since"], date) else datetime.strptime(str(g["since"]), "%Y-%m-%d").date()
        dias = (date.today() - d).days
        quem = g.get("owner", "sem dono")
        if dias > sla:
            rep.fail("F2", f"gate '{g.get('id','?')}' aberto há {dias} dias (SLA {sla}), com {quem}", inc)
    rep.note("F2", f"{len(abertos)} gate(s) aberto(s), SLA {sla} dias")


def f3_git(root, rep):
    inc = "careertransition, conteúdo de recolocação, sem git nenhum"
    top = git_toplevel(root)
    if top is None:
        rep.fail("F3", "o projeto não está sob git — não há histórico nem como voltar atrás", inc)
        return
    aninhado = top.resolve() != Path(root).resolve()
    if aninhado:
        # subprojeto aninhado: o repo é do pai. Push e edições não-commitadas são do doctor
        # DELE (W2/W4 rodam lá, sobre a árvore inteira) — reportar de novo aqui seria eco.
        rep.note("F3", f"sob git do repo pai ({top.name}) — subprojeto aninhado, sem repo próprio")
        return
    code, out = sh(["git", "status", "-sb"], root)
    m = re.search(r"ahead (\d+)", out or "")
    plog = root / ".mjrp" / "push.log"
    ultimo = "nunca registrado"
    if plog.exists():
        lines = [l for l in plog.read_text(encoding="utf-8").splitlines() if l.strip()]
        if lines:
            ultimo = lines[-1].split(" · ")[0] + (" (FALHOU)" if "FALHOU" in lines[-1] else "")
    if m:
        rep.warn("W2", f"{m.group(1)} commit(s) aguardando push · último push: {ultimo}",
                 "commits ficavam dias sem push e sem rastro — mjrp-scripts/push.py registra em .mjrp/push.log")
    rep.note("F3", f"sob git · último push: {ultimo}")


def repo_fingerprint(root):
    """What state of the repository a sensor result belongs to.

    A stored sensor result is a claim about CODE, and code changes. On 09/09 `.mjrp/sensors.json`
    held `code: 1` for the loop sensor while the loop selftest had already been fixed and passed:
    the record was true when written and false when read, and nothing in it said which. The
    fingerprint is what makes the difference visible.

    HEAD alone is not enough - most of the day the work is uncommitted. So: HEAD, plus the
    porcelain status with the derived paths filtered out, plus size and mtime of everything that
    status names. That covers the commit, the staging, and the edit that happened one second ago.
    Returns None when git cannot answer: a fingerprint that cannot be computed must not be
    invented, and a record without one reads as stale.
    """
    code, head = sh(["git", "rev-parse", "HEAD"], root)
    if code != 0:
        return None
    code, status = sh(["git", "status", "--porcelain", "-uall"], root)
    if code != 0:
        return None
    partes = [head.strip()]
    for linha in sorted(status.splitlines()):
        caminho = linha[3:].strip().strip('"')
        if any(d in f"/{caminho}" for d in DERIVED):
            continue
        partes.append(linha)
        try:
            st = (root / caminho).stat()
            partes.append(f"{st.st_size}:{st.st_mtime_ns}")
        except OSError:
            partes.append("ausente")
    return hashlib.sha1("\n".join(partes).encode("utf-8")).hexdigest()[:16]


def a1_sensors(root, cfg, rep, skip):
    inc = "o contrato declara {lint, test, build} e nada verifica que rodam; o Albums v0 tem 310 arquivos em produção sem que se saiba se o teste dele roda"
    inc_cache = ("09/09: o `.mjrp/sensors.json` guardava `code: 1` para o sensor do loop enquanto "
                 "o loop_selftest já estava consertado e passando — o registro era verdadeiro "
                 "quando foi escrito e falso quando foi lido, e nada nele dizia qual dos dois")
    sensors = cfg.get("sensors") or {}
    if not sensors:
        rep.fail("A1", "contrato sem sensores declarados — não há o que medir, só opinião", inc)
        return
    cache_file = root / SENSOR_CACHE
    cache = {}
    if cache_file.exists():
        try:
            cache = json.loads(cache_file.read_text())
        except Exception:
            cache = {}
    agora = repo_fingerprint(root)
    if skip:
        velhos, lidos = [], 0
        for name in sensors:
            r = cache.get(name)
            if not r:
                rep.fail("A1", f"sensor '{name}' nunca foi executado (sem registro)", inc)
            elif agora is None or r.get("fingerprint") != agora:
                velhos.append(name)
            elif r.get("code") != 0:
                rep.fail("A1", f"sensor '{name}' falhou na última execução ({r.get('when','?')})", inc)
            else:
                lidos += 1
        if velhos:
            # NÃO é aprovação e NÃO é reprovação: é não avaliável, o exit 2 do contrato do
            # harness. O registro descreve outro estado do repositório; dizer verde a partir
            # dele é o defeito, e dizer vermelho seria inventar uma falha que ninguém viu.
            rep.fail("A1", f"{len(velhos)} sensor(es) com registro de OUTRO estado do repositório "
                           f"({', '.join(sorted(velhos)[:4])}{'…' if len(velhos) > 4 else ''}) — "
                           f"não avaliável; rode o doctor sem --skip-sensors", inc_cache)
        if lidos:
            rep.note("A1", f"{lidos} sensor(es) lidos do registro, no estado atual (--skip-sensors)")
        return
    for name, cmd in sensors.items():
        code, out = sh(cmd, root, SENSOR_TIMEOUT)
        cache[name] = {"code": code, "when": datetime.now().isoformat(timespec="seconds"),
                       "fingerprint": agora, "v": SENSOR_CACHE_VERSION}
        if code == 127:
            rep.fail("A1", f"sensor '{name}' não executa: {out[:120]}", inc)
        elif code != 0:
            rep.fail("A1", f"sensor '{name}' reprovou (exit {code}): {out.splitlines()[-1][:120] if out else ''}", inc)
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(cache, indent=2, ensure_ascii=False))
    rep.note("A1", f"{len(sensors)} sensor(es) executados")


# Repository areas where an uncommitted edit matters to the agent right at session start:
# the human touched something, and the agent must know BEFORE acting over it.
WATCHED_AREAS = {
    "identidade": ("VISION.md", "MEMORY.md", "AGENTS.md", "CLAUDE.md", "PRINCIPLES.md", "docs/specs/prd.md", "ROADMAP.md",
                   "HOWTO.md", "README.md", ".mjrp-project.yml"),
    "wiki":       ("docs/wiki/",),
    "decisões":   ("docs/decisions/",),
    "skills":     ("mjrp-skills/",),
    "scripts":    ("mjrp-scripts/",),
    "arquivo":    ("_archive/",),
}


def w4_uncommitted_edits(root, rep):
    """W4 - the human edited on disk and did not commit. Warning, not error: being mid-edit is
    normal. The value is at session start: the agent finds out someone touched something, and
    where, before writing over it. It does not say WHAT changed - that is `git diff`."""
    inc = ("08/09: o Zé reestruturou o VISION.md à mão, no disco, e o agente só soube porque ele "
           "perguntou e o agente rodou git status — nada no harness avisava")
    top = git_toplevel(root)
    if top is None or top.resolve() != Path(root).resolve():
        return  # sem git, ou aninhado: o doctor do repo pai é quem vê as edições da árvore
    # sh() strips the whole output and would eat the status space of the porcelain's first line.
    # Aqui o formato importa: chama subprocess direto.
    try:
        pr = subprocess.run(["git", "status", "--porcelain", "--untracked-files=normal"],
                            cwd=root, text=True, capture_output=True, timeout=30)
    except Exception:
        return
    if pr.returncode != 0:
        return
    achados = {}
    for linha in pr.stdout.splitlines():
        if len(linha) < 4:
            continue
        state, path_str = linha[:2], linha[3:].strip()
        if path_str.startswith(("_backups/", ".mjrp/")):
            continue
        for area, prefixos in WATCHED_AREAS.items():
            if any(path_str == pfx or path_str.startswith(pfx) for pfx in prefixos):
                e = state.strip()
                tag = "novo" if e == "??" else ("removido" if "D" in e else "modificado")
                achados.setdefault(area, []).append((path_str, tag))
                break
    if not achados:
        rep.note("W4", "nenhuma edição sem commit nas áreas vigiadas")
        return
    total = sum(len(v) for v in achados.values())

    def summary(items):
        # ate 4 itens: lista; acima disso, agrupa por pasta de primeiro nivel e conta —
        # mover uma pasta inteira vira "48 removidos em _archive/", nao 48 linhas
        if len(items) <= 4:
            return ", ".join(f"{c} ({t})" for c, t in items)
        grupos = {}
        for c, t in items:
            topo = c.split("/")[0] + "/" if "/" in c else c
            grupos.setdefault((topo, t), 0)
            grupos[(topo, t)] += 1
        return ", ".join(f"{n} {t}{'s' if n > 1 else ''} em {topo}" for (topo, t), n in grupos.items())

    detalhe = " · ".join(f"{area}: {summary(v)}" for area, v in achados.items())
    rep.warn("W4", f"{total} arquivo(s) editado(s) sem commit — {detalhe}. Rode `git diff` antes de escrever por cima.", inc)


# The platform's HARD limit. Above it the upload is REFUSED - the skill simply does not
# install, and the message that says so appears in the tool, not here. This is not the same
# thing as W1: W1 is about cost (tokens in every session), this is about the skill existing
# at all. Two different failures, two different checks.
DESCRIPTION_HARD_LIMIT = 1024
DESCRIPTION_MARGIN = 950          # within 8% of the ceiling: one edit away from breaking

# There is NO per-skill target here, and that absence is the decision.
#
# It was 200, a number I invented and wrote into ADR-0002 as criterion. When the 53 skills were
# actually rewritten to meet it, the Zé looked at the result and said the opposite of what I had
# assumed: the build-framework skills are the ones he expects to APPEAR ON THEIR OWN, so they are
# where the trigger list earns its cost. I then proposed 650 - a number calibrated on the very
# cut he had just rejected. Two invented numbers in one day is enough.
#
# What is left are the two limits the PLATFORM gives, which nobody has to agree with:
#   · 1024 - above it the upload is refused and the skill does not install. Error.
#   · the margin below it - one edit away from that. Warning.
# And the SUM, which is the only cost that is actually paid: reported always, warned about only
# when it GROWS past where a deliberate decision left it. It measures drift, not taste.
DESCRIPTION_BUDGET = 33000


def w1_descriptions(rep, skill_files):
    inc = ("49 de 49 descriptions acima de 200 caracteres — cerca de 8.000 tokens em toda "
           "sessão; em 09/09, com a memória já enxuta, eram 67% de todo o custo fixo")
    inc_1024 = ("09/09: o upload da mjrp-onboarding foi RECUSADO — 'description must be at most "
                "1024 characters'. Outra ferramenta encurtou o arquivo no disco para conseguir "
                "subir, e ninguém soube por quê; o harness não media esse limite")
    estouradas, no_limite = [], []
    total = 0
    for f in skill_files:
        d = str(frontmatter(f).get("description", ""))
        n = len(d)
        total += n
        pass
        if n > DESCRIPTION_HARD_LIMIT:
            estouradas.append((f.parent.name, n))
        elif n > DESCRIPTION_MARGIN:
            no_limite.append((f.parent.name, n))
    # The hard limit is an ERROR: a skill that does not install is not a warning.
    for nome, n in sorted(estouradas, key=lambda x: -x[1]):
        rep.fail("W1", f"{nome}: description com {n} chars — acima do limite duro de "
                       f"{DESCRIPTION_HARD_LIMIT}; a skill NÃO instala", inc_1024)
    if no_limite:
        pior = max(no_limite, key=lambda x: x[1])
        rep.warn("W1", f"{len(no_limite)} skill(s) a menos de {DESCRIPTION_HARD_LIMIT - DESCRIPTION_MARGIN} "
                       f"chars do limite duro (pior: {pior[0]}, {pior[1]}/{DESCRIPTION_HARD_LIMIT}) — "
                       f"uma frase a mais e para de instalar", inc_1024)
    if total > DESCRIPTION_BUDGET:
        rep.warn("W1", f"as {len(skill_files)} descriptions somam {total} chars (~{total // 4} "
                       f"tokens em TODA sessão), acima de onde a decisão de 09/09 deixou "
                       f"({DESCRIPTION_BUDGET}) — cresceu; veja o que entrou", inc)
    else:
        rep.note("W1", f"descriptions: {total} chars (~{total // 4} tokens/sessão), "
                       f"dentro de {DESCRIPTION_BUDGET}")


# BACKLOG #42 / ADR-0009: skills de fronteira envelhecem caladas — rodam uma vez, no início,
# quando ninguém tem repertório para desconfiar; o custo de estarem erradas é pago espalhado por
# toda sessão seguinte, não na sessão em que rodaram. Incidente: 11/09, a mjrp-project-bootstrap
# estava 14 pontos atrasada (nem criava o .mjrp-project.yml) e ninguém tinha notado.
#
# Lista em código, não no contrato — mantém o critério da ADR-0002 §4 (determinístico, sem rede,
# sem julgamento). Proxy de "revisada" é a data do último commit do SKILL.md fonte, mesma lógica
# que F3/W2 já usam para git: não é prova de revisão substantiva, é o único sinal que já existe.
BOUNDARY_SKILLS = {"mjrp-onboarding", "mjrp-project-bootstrap"}
BOUNDARY_STALE_DAYS = 30


def w5_boundary_skills(root, rep, skill_files):
    inc = ("11/09: a mjrp-project-bootstrap estava atrasada em 14 pontos — nem criava o "
           ".mjrp-project.yml — e ninguém tinha notado; skill de fronteira envelhece calada")
    alvos = [f for f in skill_files if f.parent.name in BOUNDARY_SKILLS]
    stale = []
    for f in sorted(alvos, key=lambda f: f.parent.name):
        code, out = sh(["git", "log", "-1", "--format=%ct", "--", str(f)], root)
        if code != 0 or not out.strip().isdigit():
            rep.warn("W5", f"{f.parent.name}: sem histórico git para o SKILL.md — não dá para "
                           f"medir a janela de revisão", inc)
            continue
        dias = (time.time() - int(out.strip())) / 86400
        if dias > BOUNDARY_STALE_DAYS:
            stale.append((f.parent.name, int(dias)))
    for nome, dias in stale:
        rep.warn("W5", f"{nome}: sem revisão (sem commit no SKILL.md) há {dias} dias — passou "
                       f"da janela de {BOUNDARY_STALE_DAYS}; é skill de fronteira, revisar por "
                       f"calendário", inc)
    if alvos and not stale:
        rep.note("W5", f"{len(alvos)} skill(s) de fronteira dentro da janela de "
                       f"{BOUNDARY_STALE_DAYS} dias")


# BACKLOG #62/#63: nada roda sozinho hoje - nem de tempos em tempos, nem em gatilho automático
# (achado do MJRP, 17/09, ver conversa com outro agente registrada em MEMORY.md). O `#62` de
# verdade (verificar o que está DE FATO instalado no Cowork) só dá para rodar DE DENTRO de uma
# sessão Cowork ativa - ver `cowork_sync_check.py` e a scheduled task diária. Mas metade do gap
# não precisa do Cowork nenhum: o `skills_status.py` já sabe responder "o que mudou desde a
# última subida" (BACKLOG #63) usando só `git diff` contra o marcador - só que ninguém digitava o
# comando, e foi exatamente esse silêncio que deixou 53+ skills mudarem por 8 dias sem
# ninguém notar. W8 é essa MESMA lógica, rodando sozinha a cada SessionStart, de graça (sem
# device_bash, sem Cowork, só o git local) - não substitui o #62, avisa que HÁ trabalho pendente
# enquanto o #62 (a verificação de verdade, diária) ainda não rodou.
def w8_cowork_marker(root, cfg, rep):
    """W8 - drift do marcador de Cowork sem ninguém rodar skills_status.py à mão."""
    inc = ("17/09: o marcador de skills_status.py ficou 8 dias parado enquanto 53+ skills "
           "mudavam, e nada avisava - só apareceu porque o MJRP pediu verificação manual")
    if cfg.get("profile") != "meta":
        rep.note("W8", "n/a — só se aplica à fonte (profile: meta)")
        return
    try:
        import importlib
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import skills_status as ss
        importlib.reload(ss)
        ss.ROOT_DIR = root
        ss.MARKER = root / ".mjrp" / "cowork-install.json"
    except Exception as e:
        rep.warn("W8", f"skills_status.py não pôde ser importado ({e}) — drift de Cowork não avaliado", inc)
        return

    if not ss.MARKER.exists():
        rep.warn("W8", "nenhuma subida para o Cowork jamais registrada "
                       "(.mjrp/cowork-install.json não existe) — rode "
                       "`python3 mjrp-scripts/skills_status.py --marcar` depois de subir tudo", inc)
        return

    try:
        marco = json.loads(ss.MARKER.read_text(encoding="utf-8"))
        nomes, _novas = ss.changed(marco["commit"])
    except Exception as e:
        rep.warn("W8", f"marcador ilegível ou git falhou ({e}) — drift de Cowork não avaliado", inc)
        return

    idade_dias = int((time.time() - datetime.strptime(marco["quando"], "%Y-%m-%d %H:%M").timestamp()) / 86400)
    if nomes:
        listagem = ", ".join(sorted(nomes)) if len(nomes) <= 6 else f"{len(nomes)} skills"
        rep.warn("W8", f"{len(nomes)} skill(s) mudaram desde a última subida pro Cowork "
                       f"({marco['quando']}, {idade_dias}d atrás) e ainda não foram reempacotadas: "
                       f"{listagem}. `propose_skills` + git commit fecham isto "
                       f"(Ways of Working, MEMORY.md 17/09 21:46)", inc)
    else:
        rep.note("W8", f"nenhuma skill mudou desde a última subida pro Cowork "
                       f"({marco['quando']}, {idade_dias}d atrás)")


# ─────────────────────────────────────────────────────────────── main

# 26/09, ADR-0014 (EP-09): structure by nature. The rules live in structure_rules.json (vendored);
# the logic in structure_check.py (vendored). Warning, never error: healing is a `git mv` the human
# approves, and a red doctor for a folder name would get the doctor ignored. One warning per item,
# so the daily-checks ledger tracks each one opening and closing.
def w9_structure(root, rep):
    inc = ("2026-09-05: 28 arquivos mudaram de pasta e nenhum sensor acusou; 2026-09-26: o docs/ do "
           "fin-control com 16 entradas de quatro naturezas — cada skill escolhia o próprio destino")
    sys.dont_write_bytecode = True                  # the import runs in every child: no __pycache__ left behind
    try:
        import structure_check
    except ModuleNotFoundError:
        rep.note("W9", "structure_check.py ausente nesta instância — estrutura por natureza não avaliada "
                       "(chega com o kernel: `new_project.py --refresh-kernel`)")
        return
    try:
        profile, findings = structure_check.check(root)
    except Exception as e:                           # a broken rules file must not break the doctor
        rep.warn("W9", f"structure_check falhou ({e}) — estrutura não avaliada", inc)
        return
    if profile is None:
        rep.note("W9", "estrutura: perfil sem regra no structure_rules.json — não avaliada")
        return
    if not findings:
        rep.note("W9", f"estrutura por natureza: conforme ({profile})")
    for f in findings:
        rep.warn("W9", f"{f['path']} — {f['msg']}", inc)
    if profile == "meta":                           # the source also watches every child, like W7
        fora = []
        for child in structure_check.all_projects(root)[1:]:
            cprof, cf = structure_check.check(child)
            if cprof and cf:
                fora.append(f"{child.name} ({len(cf)})")
        if fora:
            rep.warn("W9", f"{len(fora)} projeto(s) com item fora da natureza: {', '.join(fora)} — "
                           f"`python3 mjrp-scripts/structure_check.py --all-projects` diz o quê e para onde", inc)
        else:
            rep.note("W9", "estrutura: todos os projetos vizinhos conformes")


def run(root, skip_sensors):
    rep = Report()
    cfile = root / CONTRACT
    if not cfile.exists():
        print(f"doctor: {root} não tem {CONTRACT} — instância não avaliável (exit 2)")
        print("        um projeto sem contrato não é verde nem vermelho: é desconhecido.")
        return None, 2
    raw = read_yaml(cfile.read_text(encoding="utf-8")) or {}
    cfg = raw.get("mjrp_harness") or {}
    if not cfg:
        print(f"doctor: {CONTRACT} sem bloco 'mjrp_harness:' (exit 2)")
        return None, 2

    src_root = root if cfg.get("profile") == "meta" else root
    skill_dirs = ["mjrp-skills"] if cfg.get("profile") == "meta" else INSTALLED_DIRS
    skill_files = [p for ps in find_skills(src_root, skill_dirs).values() for p in ps]

    c1_conformance(root, cfg, rep)
    i1_contract(cfg, rep)
    i2_paths(root, cfg, rep, skill_files)
    i3_links(root, rep)
    i4_agents(root, rep)
    i5_principles_inheritance(root, rep)
    i5_kernel(root, cfg, rep)
    w7_kernel_downstream(root, cfg, rep)
    i5_constitution_generated(root, cfg, rep)
    f1_memory(root, rep, cfg)
    f1_log_shape(root, rep)
    f1_wow_growth(root, rep)
    f2_gates(cfg, rep)
    f3_git(root, rep)
    a1_sensors(root, cfg, rep, skip_sensors)
    w1_descriptions(rep, skill_files)
    w4_uncommitted_edits(root, rep)
    w5_boundary_skills(root, rep, skill_files)
    w6_charter_not_migrated(root, rep)
    w8_cowork_marker(root, cfg, rep)
    w9_structure(root, rep)
    _daily_checks_ledger(root, cfg, rep)
    return rep, (1 if rep.errors else 0)


def _finding_identity(cid, msg):
    """cid sozinho nao basta -- o mesmo cid pode carregar mais de um achado distinto na MESMA
    rodada (ex.: dois avisos F1 diferentes juntos), e usar a mensagem inteira faz a identidade
    tremer a toa (contagem de arquivo, timestamp de push mudam sem o achado ter sido corrigido --
    foi exatamente o bug que duplicou linha em `daily-checks/` na primeira versao disto, 16/09).
    Meio-termo: cid + a mensagem com todo digito apagado, que preserva achados diferentes
    distintos e absorve so' o que varia de rodada pra rodada."""
    normalizado = re.sub(r"\d+", "#", msg)
    return f"{cid}:{normalizado}"


def _daily_checks_ledger(root, cfg, rep):
    """BACKLOG #60: o proprio doctor.py alimenta daily-checks/ com TODOS os seus achados, nao so'
    os do SDD_chain. Nunca falha o doctor -- e' so' rastro, roda por ultimo, de proposito."""
    try:
        import daily_checks
        when = _today(cfg).isoformat()
        avisos = [(_finding_identity(cid, msg), f"[{cid}] {msg}")
                  for cid, lvl, msg, _inc in rep.findings if lvl == AVISO]
        erros = [(_finding_identity(cid, msg), f"[{cid}] {msg}")
                 for cid, lvl, msg, _inc in rep.findings if lvl == ERRO]
        daily_checks.report(root, "doctor", "sensor-warnings.md", "doctor.py (avisos correntes)", avisos, when)
        daily_checks.report(root, "doctor", "sensor-errors.md", "doctor.py (erros correntes)", erros, when)
    except Exception as e:
        rep.note("F1", f"daily-checks/ nao pode ser escrito ({e}) -- rastro pulado, doctor segue normal")


def main():
    ap = argparse.ArgumentParser(description="sensor computacional do harness (ADR-0002)")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--skip-sensors", action="store_true", help="usa o último resultado registrado")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    root = Path(a.path).resolve()
    if not root.is_dir():
        print(f"doctor: {root} não existe (exit 2)")
        sys.exit(2)

    t0 = time.time()
    rep, code = run(root, a.skip_sensors)
    if rep is None:
        sys.exit(code)

    if a.json:
        print(json.dumps({
            "root": str(root), "exit": code,
            "erros": [{"id": i, "msg": m} for i, l, m, _ in rep.findings if l == ERRO],
            "avisos": [{"id": i, "msg": m} for i, l, m, _ in rep.findings if l == AVISO],
        }, indent=2, ensure_ascii=False))
        sys.exit(code)

    print(f"\n  doctor · {root.name}")
    for cid, msg in rep.notes:
        print(f"  · [{cid}] {msg}")
    for cid, level, msg, inc in rep.findings:
        tag = "ERRO " if level == ERRO else "aviso"
        print(f"\n  [{tag} {cid}] {msg}")
        print(f"          nasceu de: {inc}")
    veredito = "VERDE" if code == 0 else "VERMELHO"
    print(f"\n  {veredito} — {len(rep.errors)} erro(s), {len(rep.warnings_)} aviso(s) · {time.time()-t0:.1f}s")
    print(f"  critério: ADR-0002, emendada pela 0007 (docs/decisions/)\n")
    sys.exit(code)


if __name__ == "__main__":
    main()
