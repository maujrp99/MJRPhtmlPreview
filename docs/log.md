# log — o que aconteceu, em ordem

> **Append-only.** Uma entrada por bloco de trabalho, mais recente no topo, com prefixo parseável: `## [AAAA-MM-DD HH:MM] <tipo> — título`. Tipos: `session`, `decision` (o conteúdo mora na página do assunto em `docs/wiki/`, seção `## History`), `ingest`, `inventory`. Hora de Brasília, sempre. Ninguém lê este arquivo inteiro — consulta-se por data ou `grep`. Aqui fica só o **quando**; o que é verdade mora na wiki, o estado no `MEMORY.md`.

## [2026-09-27 00:05] decision — estrutura por natureza aplicada (EP-09 do harness)

> Participantes: MJRP + Claude (Cowork, sessão do harness) · Branch: main
> Session: https://claude.ai/code/session_01QmaqjvQpirivrfpMzMbKvm

- Kernel refrescado (sensor da estrutura, pre-commit, hook). `docs/sessions/` → `_archive/…/docs-sessions/`; o debug log antigo tinha 1 item aberto (Export to PNG, adiado) — virou `UAT-001` no `docs/specs/uat.md` (criado agora), e o arquivo foi para `_archive/`.

