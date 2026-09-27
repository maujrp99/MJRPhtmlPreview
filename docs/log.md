# log — o que aconteceu, em ordem

> **Append-only.** Uma entrada por bloco de trabalho, mais recente no topo, com prefixo parseável: `## [AAAA-MM-DD HH:MM] <tipo> — título`. Tipos: `session`, `decision` (o conteúdo mora na página do assunto em `docs/wiki/`, seção `## History`), `ingest`, `inventory`. Hora de Brasília, sempre. Ninguém lê este arquivo inteiro — consulta-se por data ou `grep`. Aqui fica só o **quando**; o que é verdade mora na wiki, o estado no `MEMORY.md`.

## [2026-09-27 11:21] decision — kernel do harness atualizado: MP-01 no design-canon e `data/canonical/`

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01QmaqjvQpirivrfpMzMbKvm

- `design-canon` (`docs/wiki/harness/`) ganhou a disciplina **MP · Método de produção**, com o **MP-01 — divergir antes de
  convergir**: onde a decisão de design tem latitude, a skill entrega três opções (Consolidar / Elevar / Transformar)
  sobre um eixo nomeado antes do checklist.
- A estrutura por natureza passou a aceitar `data/canonical/` (dado já normalizado para ingestão).

## [2026-09-27 10:45] decision — kernel do harness atualizado: PRINCIPLES I.14 e engineering-canon ampliado

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01QmaqjvQpirivrfpMzMbKvm

- `PRINCIPLES.md` ganhou o **I.14 — segredo nunca no código** (o teste: o repositório pode ficar público
  amanhã sem trocar nenhuma credencial). O `engineering-canon` (`docs/wiki/harness/`) ganhou *Quando
  extrair*, OCP, a escada de isolamento, *Fluxo de dados e estado*, *Desempenho e custo* e *Sinais e
  anti-padrões*; o *Refactoring* (Fowler) virou a quarta fonte. Decisão do MJRP no harness, 27/09.
- A `constitution.md` deste projeto não muda sozinha: o template novo do harness sugere as seções
  Tipagem, Tamanho de arquivo, Nomes, Padrões com endereço e Proibições — preencher quando ela for revisada.

## [2026-09-27 00:05] decision — estrutura por natureza aplicada (EP-09 do harness)

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01QmaqjvQpirivrfpMzMbKvm

- Kernel refrescado (sensor da estrutura, pre-commit, hook). `docs/sessions/` → `_archive/…/docs-sessions/`; o debug log antigo tinha 1 item aberto (Export to PNG, adiado) — virou `UAT-001` no `docs/specs/uat.md` (criado agora), e o arquivo foi para `_archive/`.

