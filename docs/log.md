# log — o que aconteceu, em ordem

> **Append-only.** Uma entrada por bloco de trabalho, mais recente no topo, com prefixo parseável: `## [AAAA-MM-DD HH:MM] <tipo> — título`. Tipos: `session`, `decision` (o conteúdo mora na página do assunto em `docs/wiki/`, seção `## History`), `ingest`, `inventory`. Hora de Brasília, sempre. Ninguém lê este arquivo inteiro — consulta-se por data ou `grep`. Aqui fica só o **quando**; o que é verdade mora na wiki, o estado no `MEMORY.md`.

## [2026-10-09 21:43] session — requisitos com o título no nome do arquivo (<ID>-<slug>.md)

> Participantes: MJRP + Claude (Claude Code) · Branch: main
> Session: https://claude.ai/code/session_014Njz6sPfb4eXwKy8bvGxqq

Revisão geral do harness de 9/10, aplicada aqui: os 16 arquivos de requisito passam a `<ID>-<slug>.md` (o slug é o título em inglês, encurtado por julgamento quando passa de 50 caracteres), com `aliases: [<ID>]`; os links e embeds do PRD e das specs usam o nome inteiro com o ID como texto (`[[S-07-…|S-07]]`). Feito por `req_file_names.py --map --apply` do harness; backup em `_backups/req-file-names-20261009-2143/`. Grafo sem achado novo. O kernel foi atualizado antes, no mesmo dia.

## [2026-10-05 18:53] session — cópias antigas de skills arquivadas; o GEMINI.md aponta para as skills do harness

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01UFhRr8vY3DcgNwoXzoEzLx

- Decisão do MJRP (2026-10-05 18:5x, "arquivar e apontar"): as cópias antigas de skills, workflows e rules que viviam no projeto (`.agent/`, e `skills/` quando havia) foram para `_archive/2026-10-05-legacy-agent/` com `git mv` — um agente que abria o projeto lia nomes aposentados dali. O `GEMINI.md` agora aponta para as skills do MJRP Harness instaladas na AI Platform.

## [2026-10-05 18:48] session — `.mjrp/` sai do índice do git (correção)

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01UFhRr8vY3DcgNwoXzoEzLx

- A entrada de 16:47 disse que o `.mjrp/` (cache dos sensores) tinha saído do índice; não saiu — o commit por caminho levou o arquivo do disco de volta. Agora sai de fato (`git rm --cached`); o arquivo fica no disco e o `.gitignore` já o ignora.

## [2026-10-05 16:58] session — estado e links depois do grafo de requisitos (harness, S-77/S-79)

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01UFhRr8vY3DcgNwoXzoEzLx

- Depois do trabalho do harness de hoje: `## Now` atualizado com o estado (grafo de requisitos, SDD_chain aposentado); links que apontavam para `story.md`/`spec.md`/`tasks.md` planos corrigidos para os nós e a pasta da feature.

## [2026-10-05 16:47] session — rastro dos sensores e backup do refresh no git (S-77 do harness)

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01UFhRr8vY3DcgNwoXzoEzLx

- Depois do refresh do kernel de hoje (S-77 do harness): o rastro dos sensores em `daily-checks/` entra no git, como no harness; o backup do `.claude/settings.json` que o refresh fez em `_backups/` também; `.mjrp/` (cache dos sensores) saiu do índice — o `.gitignore` já o ignora, o arquivo continua no disco.

## [2026-10-05 16:32] session — grafo de requisitos: backlog virou nós, spec/plan/tasks viraram feature (S-79 do harness)

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01UFhRr8vY3DcgNwoXzoEzLx

- Pedido do MJRP no harness (2026-10-05 13:2x: "endereça tudo o que for necessário pra não ficar pendência"): este projeto passou para o grafo de requisitos, como o harness. O `story.md` virou nós em `docs/specs/requirements/<pasta do épico>/`, em pt-BR e em inglês; o `spec.md`/`plan.md`/`tasks.md` planos foram para `docs/specs/features/F01-…/` (e outras pastas, se havia); o PRD ganhou a seção `## Requisitos por épico` e o ROADMAP, as âncoras `^OUT-NN`. Status de cada nó pela evidência (commit que entregou, aceite registrado); sensor do grafo VERDE. O mapa velho→novo, os status e as perguntas em aberto estão em `reports/audits/2026-10-05-graph-migration-report.md`. O `story.md` original está em `_archive/2026-10-05-story-md/`.

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

