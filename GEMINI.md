# Instruções do Projeto MJRPhtmlPreview

## Contexto Obrigatório
Antes de qualquer trabalho, leia:
- VISION.md (propósito e direção estética)
- CHARTER.md (escopo, milestones, restrições)
- docs/specs/constitution.md (regras técnicas e stack)
- docs/specs/design-system.md (tokens visuais Minimal Dark)
- docs/specs/tasks.md (backlog atual)

## Sobre o Projeto
MJRPhtmlPreview é um visualizador de HTML client-side com save para Google Drive e download local (Obsidian vault). Arquitetura: single HTML file SPA, sem backend, vanilla JS.

## Workflows Disponíveis
Quando executar tarefas, siga os workflows em .agent/workflows/:
- sdd_protocol.md — Fluxo SDD completo (Specify → Plan → Tasks → Implement)
- debug_protocol.md — Protocolo de debug
- onboarding_protocol.md — Carregamento de contexto

## Regras
- Siga Conventional Commits (feat, fix, docs, refactor, vibe, chore)
- Nunca implemente sem task em docs/specs/tasks.md
- Consulte constitution.md antes de sugerir dependências
- Filosofia vanilla-first: sem dependências externas salvo necessidade absoluta
- Arquitetura single HTML file para MVP (CSS + JS inline)
- Nunca commite secrets (.env, API keys, OAuth credentials)
- Respeite o fluxo SDD: Specify -> Plan -> Tasks -> Implement
- Atualize SESSION_HISTORY.md ao final de cada sessão
