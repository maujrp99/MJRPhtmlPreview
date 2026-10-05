# Instruções do Projeto MJRPhtmlPreview

> **A fonte canônica de instruções deste projeto é o [`AGENTS.md`](AGENTS.md).**
> Leia-o primeiro; o que está abaixo acrescenta só o que é específico desta AI Platform.

## Contexto Obrigatório
Antes de qualquer trabalho, leia:
- VISION.md (propósito e direção estética)
- docs/specs/prd.md (escopo, milestones, restrições)
- docs/specs/constitution.md (regras técnicas e stack)
- docs/specs/design-system.md (tokens visuais Minimal Dark)
- docs/specs/requirements/ (backlog, um nó por requisito) e docs/specs/features/<F-ID>/tasks.md (tarefas)

## Sobre o Projeto
MJRPhtmlPreview é um visualizador de HTML client-side com save para Google Drive e download local (Obsidian vault). Arquitetura: single HTML file SPA, sem backend, vanilla JS.

## Skills do harness
As cópias antigas de skills e workflows que viviam em `.agent/` foram arquivadas em `_archive/2026-10-05-legacy-agent/` (2026-10-05). Use as skills do MJRP Harness instaladas na AI Platform:
- `mjrp-pdlc-onboarding` — carregamento de contexto no início da sessão
- `mjrp-specifying-sdd-artifacts` e `mjrp-implementing-tasks` — fluxo SDD (spec → plan → tasks → implement); `mjrp-ensuring-sdd` confere os gates
- `mjrp-debugging` — protocolo de debug
- `mjrp-saving-context` — fechamento da sessão

## Regras
- Siga Conventional Commits (feat, fix, docs, refactor, vibe, chore)
- Nunca implemente sem task num docs/specs/features/<F-ID>/tasks.md
- Consulte constitution.md antes de sugerir dependências
- Filosofia vanilla-first: sem dependências externas salvo necessidade absoluta
- Arquitetura single HTML file para MVP (CSS + JS inline)
- Nunca commite secrets (.env, API keys, OAuth credentials)
- Respeite o fluxo SDD: Specify -> Plan -> Tasks -> Implement
- Atualize SESSION_HISTORY.md ao final de cada sessão
