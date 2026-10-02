#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-02 · fonte 64f0cf9 · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""SDD_chain_artifacts_check.py -- rastreabilidade de IDs na cadeia SDD (prd -> story -> spec ->
plan -> tasks).

NUNCA e sensor do A1 (nao entra em `sensors:` do .mjrp-project.yml -- A1 trata qualquer saida
!= 0 como FAIL, e este aviso e por natureza informativo, BACKLOG #58). Chamado a mao ou pelo
hook Stop do PROJETO-FILHO (nao deste harness, que nao tem cadeia SDD propria) -- sempre sai 0.

Origem: docs/wiki/feedback-from-other-projects/spec-chain-consistency-check.md (achado do
mjrp-fin-control-2026-27, 2026-09-16) -- EP-11/EP-12 avancaram ate plan.md/tasks.md sem o
prd.md ser atualizado, e nada acusou.

Achado da PRIMEIRA rodada real (16/09, no proprio mjrp-fin-control-2026-27): checar TODO padrao
de ID entre TODO par adjacente da cadeia gera ruido, nao sinal -- 366 avisos, quase todos falso-
positivo. `REQ-`/`SC-` nascem em spec.md e nunca precisam voltar pra story.md; `TASK-` nasce em
plan/tasks e nunca precisa aparecer em spec.md. Cada TIPO de ID tem seu proprio trecho da cadeia
onde faz sentido ser rastreado -- por isso `id_patterns` virou um dict com o intervalo [de, ate],
nao uma lista solta. So' o intervalo declarado e' checado (par a par, dentro dele); um padrao sem
intervalo configurado nao e' checado.

Contrato (.mjrp-project.yml, campo novo, opcional -- projeto sem ele sai 0 e nao avisa nada):

  mjrp_harness:
    sdd_chain:
      chain: [prd, story, spec, plan, tasks]        # ordem da cadeia
      globs:                                        # cada elo pode ter varios arquivos (specs/**/*.md)
        prd:   ['docs/specs/prd.md']
        story: ['docs/specs/story.md']
        spec:  ['docs/specs/spec.md']
        plan:  ['docs/specs/plan.md']
        tasks: ['docs/specs/tasks.md']
      id_patterns:                                  # padrao -> [elo onde nasce, ate onde deveria refletir]
        'EP-\d+': [prd, story]                       # so' isto reproduz o incidente original --
                                                       # nao declare REQ-/SC-/TASK- sem um incidente
                                                       # real que peca por eles (achado acima)

Rastreio dos avisos abertos: usa `mjrp-scripts/daily_checks.py` -- cada furo detectado e' gravado
com a data em que apareceu pela primeira vez em `daily-checks/sensor-warnings.md` (secao
"sdd_chain"), pra dar pra ver o que continua aberto e o que foi resolvido.

Inventario do prototipo (02/10/2026, EP-07 -- mapeamento reverso): quando
`docs/specs/info-arch.md` tem a secao `## Inventário do protótipo`, cada item precisa terminar num
destino -- coberto/evoluido com um REQ que exista no spec.md, ou cortado com motivo escrito.
"Pendente" so' e' aviso depois que o spec.md esta' aprovado. Independe do `sdd_chain:` do contrato:
o inventario existe, ele e' conferido. O prototipo e' baseline, nao molde -- o que se cobra e'
destino, nunca igualdade.

Uso:
  python3 mjrp-scripts/SDD_chain_artifacts_check.py [root]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from doctor import read_yaml, _today  # reusa parser + relogio do doctor -- nao duplica
import daily_checks

SENSOR_ID = "sdd_chain"
LEDGER = "sensor-warnings.md"


def _read_all(paths):
    parts = []
    for p in paths:
        try:
            parts.append(p.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
    return "\n".join(parts)


def find_orphans(root, chain, globs, id_patterns):
    root = Path(root)
    index = {name: i for i, name in enumerate(chain)}
    texts, missing = {}, []
    for elo in chain:
        paths = [p for g in (globs.get(elo) or []) for p in root.glob(g)]
        if not paths:
            missing.append(elo)
            texts[elo] = None
            continue
        texts[elo] = _read_all(paths)

    warnings = []
    for pattern, span in (id_patterns or {}).items():
        if not (isinstance(span, (list, tuple)) and len(span) == 2):
            warnings.append(f"id_pattern '{pattern}': intervalo mal configurado (esperado [de, ate]) -- pulado")
            continue
        de, ate = span
        if de not in index or ate not in index or index[de] >= index[ate]:
            warnings.append(f"id_pattern '{pattern}': intervalo '{de}'->'{ate}' invalido pra esta chain -- pulado")
            continue
        for i in range(index[de], index[ate]):
            up, down = chain[i], chain[i + 1]
            if texts.get(up) is None or texts.get(down) is None:
                continue
            up_ids = set(re.findall(pattern, texts[up]))
            down_ids = set(re.findall(pattern, texts[down]))
            for oid in sorted(down_ids - up_ids):
                warnings.append(f"orfao downstream: {oid} aparece em '{down}' mas nao em '{up}'")
            for oid in sorted(up_ids - down_ids):
                warnings.append(f"orfao upstream: {oid} prometido em '{up}' mas nunca citado em '{down}'")
    return warnings, missing


INVENTORY_FILE = Path("docs") / "specs" / "info-arch.md"
INVENTORY_HEADING = re.compile(r"^##\s+Invent[aá]rio do prot[oó]tipo\s*$", re.I | re.M)
SPEC_APPROVED = re.compile(r"(?i)status\W{0,4}\s*(approved|aprovad[oa])")
STATES = {"pendente": "pendente", "coberto": "coberto", "evoluido": "evoluido", "evoluído": "evoluido",
          "cortado": "cortado"}


def _inventory_rows(text):
    """Rows of the table under '## Inventário do protótipo': [id, function, where, kind, state, req]."""
    m = INVENTORY_HEADING.search(text)
    if not m:
        return None
    body = text[m.end():]
    nxt = re.search(r"^##\s", body, re.M)
    body = body[:nxt.start()] if nxt else body
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells or not re.match(r"^[A-Z]{1,4}-\d+$", cells[0]):
            continue                                    # header and separator rows
        rows.append((cells + [""] * 6)[:6])
    return rows


def inventory_gaps(root):
    """Warnings for prototype-inventory items with no destination. None = no inventory to check."""
    root = Path(root)
    ia = root / INVENTORY_FILE
    if not ia.exists():
        return None
    rows = _inventory_rows(ia.read_text(encoding="utf-8", errors="replace"))
    if rows is None:
        return None
    spec = root / "docs" / "specs" / "spec.md"
    spec_text = spec.read_text(encoding="utf-8", errors="replace") if spec.exists() else ""
    spec_reqs = set(re.findall(r"REQ-\d+", spec_text))
    approved = bool(SPEC_APPROVED.search(spec_text))
    out, seen = [], set()
    for iid, _fn, _where, _kind, state, dest in rows:
        if iid in seen:
            out.append(f"inventario: {iid} repetido -- ID de item e' unico e estavel")
        seen.add(iid)
        st = STATES.get(state.lower().strip("* "))
        reqs = re.findall(r"REQ-\d+", dest)
        has_text = bool(re.sub(r"[\s\-—–]|motivo:?", "", dest, flags=re.I))
        if st is None:
            out.append(f"inventario: {iid} com estado '{state}' -- use pendente, coberto, evoluido ou cortado")
        elif st == "cortado":
            if not has_text:
                out.append(f"inventario: {iid} cortado sem motivo escrito")
        elif st in ("coberto", "evoluido"):
            if not reqs:
                out.append(f"inventario: {iid} {st} sem REQ -- em que requisito ele vive?")
            elif spec_text:
                for r in reqs:
                    if r not in spec_reqs:
                        out.append(f"inventario: {iid} aponta {r}, que nao existe no spec.md")
        elif st == "pendente" and approved:
            out.append(f"inventario: {iid} ainda pendente com o spec.md aprovado -- vira REQ ou e' cortado com motivo")
    return out


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    cfg_path = root / ".mjrp-project.yml"
    if not cfg_path.exists():
        return 0
    raw = read_yaml(cfg_path.read_text(encoding="utf-8"))
    cfg = raw.get("mjrp_harness") or {}
    chain_cfg = cfg.get("sdd_chain")
    inventory = inventory_gaps(root)              # None = sem inventario do prototipo
    if not chain_cfg and inventory is None:
        return 0  # nada configurado e nada a conferir -- nunca obrigatorio

    warnings = []
    if chain_cfg:
        chain = chain_cfg.get("chain") or []
        globs = chain_cfg.get("globs") or {}
        id_patterns = chain_cfg.get("id_patterns") or {}
        if len(chain) < 2 or not id_patterns:
            print("[SDD_chain] sdd_chain configurado mas incompleto (precisa chain com >=2 elos e "
                  "id_patterns) -- pulando a cadeia")
            if inventory is None:
                return 0
        else:
            warnings, missing = find_orphans(root, chain, globs, id_patterns)
            if missing:
                print(f"[SDD_chain] elo(s) sem nenhum arquivo encontrado (nao avaliados): {', '.join(missing)}")
    warnings += inventory or []

    when = _today(cfg).isoformat()
    _state, changed = daily_checks.report(
        root, SENSOR_ID, LEDGER, "SDD_chain (rastreabilidade PRD/Story/Spec/Plan/Tasks)",
        [(w, w) for w in warnings], when,
    )

    # So' fala quando o estado MUDOU (abriu ou fechou algo) -- repetir o mesmo texto a cada Stop
    # e' exatamente o barulho que este desenho existe pra evitar; o estado atual sempre da' pra
    # conferir em `daily-checks/sensor-warnings.md`.
    if changed and warnings:
        print(f"[SDD_chain] {len(warnings)} furo(s) de rastreabilidade na cadeia SDD "
              f"(ver daily-checks/{LEDGER}):")
        for w in warnings:
            print(f"  - {w}")
        print("  (aviso informativo -- nunca bloqueia o stop_gate)")
    elif changed and not warnings:
        print(f"[SDD_chain] furo(s) anterior(es) resolvido(s) -- ver daily-checks/{LEDGER}")

    return 0  # sempre informativo


if __name__ == "__main__":
    sys.exit(main())
