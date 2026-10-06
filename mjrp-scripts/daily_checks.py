#!/usr/bin/env python3
# cópia carimbada do MJRP Harness · versão 2026-10-06 · fonte 7b92583 · não edite aqui — edite no harness e rode `new_project.py --refresh-kernel`
"""daily_checks.py -- rastro DATADO (aberto/resolvido) de aviso e erro, compartilhado por
sensores informativos (SDD_chain_artifacts_check.py) e pelo proprio doctor.py.

Por que existe: um aviso/erro que so aparece ao vivo no stdout de um hook e some do rastro no
segundo seguinte -- ninguem sabe desde quando esta aberto nem quando foi corrigido (achado do
MJRP, 16/09, no meio da implementacao do BACKLOG #58; generalizado no #60 pra cobrir TODO
aviso/erro do doctor.py, nao so o SDD_chain).

Cada "dono" (SDD_chain, doctor, ...) tem sua propria secao dentro do MESMO arquivo
(`daily-checks/sensor-warnings.md` ou `sensor-errors.md`), demarcada por
`<!-- sensor:<id>:start/end -->`, pra varios donos escreverem no mesmo arquivo sem se atropelar.
O estado (o que esta aberto desde quando) fica em `.mjrp/<id>_state.json` -- por isso
`daily-checks/` e `.mjrp/` ficam fora do `repo_fingerprint()` (ver DERIVED em doctor.py): o
proprio rastro nao pode invalidar o cache de sensor que ele mesmo atualiza.

IDENTIDADE != TEXTO. Cada item e' (identity, texto): identity decide se e' o MESMO item entre
rodadas (ex.: o `cid` do doctor.py, tipo "W4"; ou o texto inteiro do furo do SDD_chain, que nao
tem parte volatil). texto e' o que aparece no ledger, e PODE mudar sem trocar de identidade --
achado do MJRP, 16/09: usar o texto inteiro do doctor.py como identidade duplicava entradas a
cada rodada, porque a mensagem carrega contagem/timestamp ao vivo (ex.: "14 arquivos" vs "16
arquivos" no mesmo aviso W4, sem nada ter sido corrigido de verdade).
"""
import json
from pathlib import Path

RESOLVED_KEEP = 20

HEADER = {
    "warnings": (
        "# Avisos nao-bloqueantes\n\n"
        "> Cada dono (sensor informativo ou o proprio `doctor.py`) tem sua secao abaixo, "
        "demarcada por `<!-- sensor:<id>:start/end -->` -- gerada pelo proprio codigo, nao "
        "editar a mao dentro das marcas.\n"
    ),
    "errors": (
        "# Erros bloqueantes -- historico\n\n"
        "> O erro em si ja bloqueia o `doctor`/`stop_gate` ao vivo; este arquivo so registra "
        "QUANDO cada um apareceu e foi corrigido, pra dar pra ver o que fica se repetindo.\n"
    ),
}


def _state_key(owner_id, filename):
    """Achado do MJRP, 16/09: um mesmo owner_id (ex.: 'doctor') escreve em DOIS ledgers
    diferentes (sensor-warnings.md e sensor-errors.md) -- se os dois lessem/escrevessem o MESMO
    arquivo de estado, a chamada do segundo (com uma lista de itens diferente) apagava o que a
    primeira acabou de salvar. A chave do estado tem que amarrar owner_id AO arquivo, no' so' ao
    dono."""
    stem = Path(filename).stem.replace("-", "_")
    return f"{owner_id}__{stem}"


def _state_path(root, owner_id, filename):
    return Path(root) / ".mjrp" / f"{_state_key(owner_id, filename)}_state.json"


def load_state(root, owner_id, filename):
    p = _state_path(root, owner_id, filename)
    if not p.exists():
        return {"open": {}, "resolved": []}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        d.setdefault("open", {})
        d.setdefault("resolved", [])
        return d
    except Exception:
        return {"open": {}, "resolved": []}


def save_state(root, owner_id, filename, state):
    p = _state_path(root, owner_id, filename)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def update_state(state, current_items, when):
    """current_items: lista de (identity, texto). Retorna (state, abriu_ou_fechou) -- o texto
    de um item que continua aberto e' sempre atualizado pro mais recente, mas isso sozinho NAO
    conta como abriu_ou_fechou (senao a mensagem oscilando reimprimiria pra sempre, o mesmo
    problema que a identidade por texto causava)."""
    still_open = {}
    for ident, text in current_items:
        prev = state["open"].get(ident)
        since = prev["since"] if prev else when
        still_open[ident] = {"since": since, "text": text}
    newly_resolved = [ident for ident in state["open"] if ident not in still_open]
    for ident in newly_resolved:
        prev = state["open"][ident]
        state["resolved"].insert(0, {
            "text": prev["text"], "opened_at": prev["since"], "resolved_at": when,
        })
    changed = set(state["open"]) != set(still_open)
    state["open"] = still_open
    state["resolved"] = state["resolved"][:RESOLVED_KEEP]
    return state, changed


def render_section(owner_id, title, state):
    lines = [f"<!-- sensor:{owner_id}:start -->", f"### {title}", "", "**Abertos**", ""]
    if state["open"]:
        lines += ["| Desde | Item |", "|---|---|"]
        ordenado = sorted(state["open"].items(), key=lambda kv: kv[1]["since"])
        lines += [f"| {v['since']} | {v['text']} |" for _k, v in ordenado]
    else:
        lines.append("_nenhum aberto no momento._")
    lines += ["", f"**Resolvidos (ultimos {RESOLVED_KEEP})**", ""]
    if state["resolved"]:
        lines += ["| Aberto em | Resolvido em | Item |", "|---|---|---|"]
        lines += [f"| {r['opened_at']} | {r['resolved_at']} | {r['text']} |" for r in state["resolved"]]
    else:
        lines.append("_nenhum ainda._")
    lines.append(f"<!-- sensor:{owner_id}:end -->")
    return "\n".join(lines) + "\n"


def write_ledger(root, filename, owner_id, section_text):
    p = Path(root) / "daily-checks" / filename
    start, end = f"<!-- sensor:{owner_id}:start -->", f"<!-- sensor:{owner_id}:end -->"
    if p.exists():
        text = p.read_text(encoding="utf-8")
        if start in text and end in text:
            text = text.split(start)[0] + section_text + text.split(end)[1]
        else:
            text = text.rstrip("\n") + "\n\n" + section_text
    else:
        kind = "errors" if filename.startswith("sensor-errors") else "warnings"
        text = HEADER[kind] + "\n" + section_text
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text.rstrip("\n") + "\n", encoding="utf-8")  # nao deixa linha em branco acumular a cada rodada


def report(root, owner_id, filename, title, current_items, when):
    """current_items: lista de (identity, texto) -- ver update_state. Sempre reescreve o ledger
    (o texto de um item aberto pode ter mudado mesmo sem abrir/fechar nada), mas so' retorna
    changed=True quando algo abriu ou fechou de verdade -- e' isso que decide se vale falar no
    stdout do chamador."""
    state = load_state(root, owner_id, filename)
    state, changed = update_state(state, current_items, when)
    save_state(root, owner_id, filename, state)
    write_ledger(root, filename, owner_id, render_section(owner_id, title, state))
    return state, changed
