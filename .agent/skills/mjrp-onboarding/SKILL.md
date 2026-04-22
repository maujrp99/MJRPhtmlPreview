---
name: mjrp-onboarding
description: >
  Carrega o contexto no INÍCIO de cada sessão — recuperação de sessão anterior, identidade do
  projeto e contexto técnico profundo por role. Use ao iniciar qualquer sessão, antes de
  refatorações complexas, ou quando solicitado para "entender" ou "auditar" um feature.
  Triggers: "retomar sessão", "onde paramos", "comece o trabalho", "carregue o contexto",
  "onboarding", "nova sessão", "qual o estado do projeto", "audit this feature", "deep reset",
  "first session", "o que temos até agora". É o DONO do início de sessão — para SALVAR ao
  final, use mjrp-save-context-handoff. Cobre: recuperação SESSION_HISTORY, leitura de
  VISION/CHARTER/ROADMAP/constitution, arch/story/spec/plan/tasks por role, e síntese com
  verificação de alinhamento SDD. Familiarizado com templates SDD: spec.md (WHAT+WHY, REQ-IDs,
  Success Criteria), plan.md (HOW, mockups, componentes), tasks.md (WHEN, checklist atômico).
---

# Skill: MJRP Onboarding — Context Loader

**Responsabilidade**: Carregar contexto no **INÍCIO** de sessões de trabalho.
**NÃO é responsabilidade deste skill**: Salvar contexto ao final — use `mjrp-save-context-handoff`.

**Divisão de responsabilidades**:
```
Início de sessão → mjrp-onboarding (este skill)
Fim de sessão    → mjrp-save-context-handoff (skill)
```

---

## SDD Derivation Chain (Internalize This)

Antes de qualquer trabalho, o agente deve ter este mapa mental:

```
CHARTER.md ──► ROADMAP.md ──► story.md (backlog) ──► spec.md ──► plan.md ──► tasks.md ──► src/
    │               │               │                    │           │           │
  Scope &       Phases &        O QUE          WHAT+WHY+REQ      HOW+mockups  WHEN+checklist
 Principles    Priorities      to build next   REQ-IDs, AC        components    atômico
```

**Regra fundamental**: nunca implementar o que não tem task aprovada. Nunca criar task sem plan
aprovado. Nunca criar plan sem spec aprovada. A chain é o contrato.

---

## SDD Artifact Templates (Reference)

### spec.md — WHAT and WHY
```markdown
# Feature: [Name]
**Status**: Draft | In Review | Approved | Implemented
**Date**: YYYY-MM-DD

## Problem Statement
[What problem? Why now?]

## User Stories
- As a [user], I want [action], so that [benefit].

## Requirements
### Functional
- [REQ-01] [Description — measurable]
- [REQ-02] [Description — testable]

### Non-Functional
- [NFR-01] [Performance/Security/Accessibility]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

## Out of Scope
- [What this feature does NOT include]

## Open Questions
- [Resolve ALL before proceeding to Plan]
```
**Rules**: No implementation details. WHAT and WHY only. UI features: user flow descriptions,
not mockups (mockups go in plan.md).

### plan.md — HOW
```markdown
# Plan: [Feature Name]
**Status**: Draft | In Review | Approved
**Spec Reference**: docs/specs/<feature>/spec.md

## Architecture Approach
[How does this fit the existing architecture? Which components/services are affected?]

## Technical Design
### Data Flow
[How data moves through the system]

### Components / Modules
- [Component 1]: [Responsibility]
- [File path]: [What changes]

### API / Interface Changes
[New endpoints, modified interfaces, schema changes]

## UI/UX Design (if applicable)
### Mockups (ASCII — mandatory for frontend)
[ASCII art of the screen layout]

### User Flow
[Step-by-step user interaction]

## Dependencies
- [Existing module this depends on]
- [New library — must align with constitution.md]

## Documents Consulted
- [Files read and key takeaways — proves agent did its homework]

## Risks & Considerations
- [Risk]: [Mitigation]
```
**Rules**: Every decision traces to a REQ-ID from spec.md. ASCII mockups are mandatory for UI.
New dependencies require ADR if they contradict constitution.md.

### tasks.md — WHEN
```markdown
# Tasks: [Feature Name]
**Status**: Draft | In Review | Approved | In Progress | Complete
**Plan Reference**: docs/specs/<feature>/plan.md

## Pre-Implementation
- [ ] Create branch: feat/<feature-name>-<timestamp>
- [ ] Confirm spec.md and plan.md are APPROVED

## Implementation
- [ ] [Task 1 — atomic: one file, one function, one clear done-signal]
- [ ] [Task 2 — atomic]
- [ ] ...

## Verification
- [ ] Run test suite
- [ ] Run build
- [ ] Manual verification of happy path
- [ ] Regression check on affected areas

## Documentation
- [ ] Update relevant spec documents
- [ ] Commit: feat: implement <feature> (ref task-N)
```
**Rules**: Each task = one focused agent session (<1h). Ordered by dependency: data → logic →
UI → polish → verify. Every task traces to plan.md which traces to spec.md REQ-IDs.

---

## Phase 0: Session Recovery (Always First)

> Antes de qualquer coisa, verificar se há contexto anterior para carregar.

**Step 1 — Ler SESSION_HISTORY.md**:
- Tentar `docs/SESSION_HISTORY.md` primeiro.
- Fallback: `docs/sessions/SESSION_HISTORY.md` (path legado).
- Se o usuário enviou um arquivo `.md` de `claude_cowork_sessions/`, priorizá-lo — é mais
  detalhado que o SESSION_HISTORY.md.
- Se existir: carregar entrada mais recente, focar em:
  - **Resumo Executivo** — o que foi feito
  - **Decisões Tomadas** — restringem trabalho atual
  - **Pendências** — ponto de partida desta sessão
  - **Dados-Chave** — métricas e versões importantes
- Se não existir: primeira sessão — prosseguir para Phase 1.

**Step 2 — Checar DEBUG_LOG**: Ler `docs/sessions/DEBUG_LOG.md` se existir. Issues ativos?

**Step 3 — Checar Git** (se projeto tem Git):
```bash
git status
git log --oneline -5
```
Se não houver Git (projeto Cowork-only): pular, notar que é projeto sem versionamento.

**Step 4 — Confirmar ao usuário**:
> "Carreguei o contexto da sessão de [data]. Última sessão: [resumo em 1 frase].
> Pendências: [top 3]. Branch atual: [branch ou 'sem Git']. Vou começar por [item 1]. Bora?"

---

## Phase 1: Project Identity

> Pular se Phase 0 forneceu contexto suficiente para continuar o trabalho.
> Rodar se: primeira sessão, deep reset, mudança de escopo, ou contexto insufiiciente.

**Ler nesta ordem**:
1. `VISION.md` — filosofia, goals, aesthetic vibe do projeto
2. `CHARTER.md` — escopo, stakeholders, milestones iniciais, constraints
3. `ROADMAP.md` — fase atual, prioridades ativas, próximos milestones (deriva do CHARTER)
4. `docs/specs/constitution.md` — stack, padrões a seguir, padrões a evitar, versões

**Ler AI config do projeto** (se existir):
- `.claudeprompt` — instruções específicas para Claude Code/Cowork neste projeto
- `.gemini/GEMINI.md` — instruções específicas para Antigravity neste projeto
- Essas configs podem sobrescrever comportamentos padrão — sempre lê-las antes de qualquer ação.

---

## Phase 2: Technical Context

> Ler sempre, mesmo que Phase 0 trouxe contexto — specs mudam entre sessões.

5. `docs/specs/arch.md` — arquitetura do sistema, mapa de componentes, data flow
6. `docs/specs/story.md` — **backlog de produto**: stories INVEST-ready por fase. É o WHAT to
   build next. Alimenta spec.md mas não é spec.md.
7. `docs/specs/spec.md` (feature ativa, se conhecida) — requisitos detalhados, REQ-IDs,
   success criteria, acceptance criteria. Ver template acima.
8. `docs/specs/plan.md` (sprint ativo, se em implementação) — design técnico da feature
   atual, mockups, componentes. Crítico se a fase for Implement. Ver template acima.
9. `docs/specs/tasks.md` — checklist de implementação atual e progresso. Ver template acima.

---

## Phase 3: Deep Context by Role

> Selecionar as áreas relevantes para a task atual. Ler "tudo" somente em onboarding completo.

### Developer (Implementation)
*Ler*: `docs/specs/constitution.md`, `docs/specs/arch.md`, `docs/specs/data-model.md`,
`docs/specs/plan.md` (feature ativa), `docs/specs/tasks.md`
*Goal*: Entender stack, padrões, onde o código vai, o que fazer hoje.
*SDD check*: Há spec e plan aprovados? Se não → não implementar. Ir para Specify ou Plan primeiro.

### Designer / UX-UI
*Ler*: `docs/specs/design-system.md`, `docs/specs/spec.md` (user stories + user flow),
`docs/specs/plan.md` (mockups existentes)
*Goal*: Entender visual system, componentes, o que está especificado visualmente.
*Tool*: Verificar referência Stitch/Figma se task é UI.

### QA / Testing
*Ler*: `docs/specs/spec.md` (success criteria + acceptance criteria), `docs/specs/tasks.md`
(verification tasks), README (test commands)
*Goal*: Entender o que deve ser testado, o que já existe, e gaps de cobertura.

### Architect / Code Review
*Ler*: `docs/specs/constitution.md`, `docs/specs/arch.md`, `docs/specs/data-model.md`,
`docs/architecture/*.md` (ADRs)
*Goal*: Entender decisões passadas, constraints, e o porquê das escolhas atuais.

---

## Phase 4: Synthesis & Verification

1. **Constraints**: Quais padrões DEVEM ser seguidos? (de constitution.md)
2. **Dependencies**: Quais serviços/componentes interagem com o que vai ser modificado?
3. **ROADMAP alignment**: O que vai ser feito bate com a fase atual no ROADMAP.md?
4. **SDD gate check**: Existe spec + plan + tasks aprovados para esta feature?
   - Sim → pronto para implementar
   - Só spec → ir para Plan first
   - Nada → ir para Specify first
5. **Confirmar ao usuário**:
   > "Contexto carregado: [arquivos lidos]. Padrões chave: [2-3 bullets de constitution].
   > SDD status: [spec/plan/tasks aprovados ou pendentes]. Pronto para [próxima ação]."

---

## Session End: Handoff (Mandatory)

> AO FINAL de toda sessão, invocar **`mjrp-save-context-handoff`** para:
> - Gerar arquivo em `claude_cowork_sessions/YYYY-MM-DD_Projeto.md`
> - Atualizar `docs/SESSION_HISTORY.md` no repo
> - Commitar e pushar se trocar de ferramenta (cross-tool bridge)

Nunca encerrar sessão sem salvar — a próxima sessão (ou próxima ferramenta) começa cega.

---

## Tool Detection Notes

Comportamento mínimo por ferramenta ao iniciar:

| Ferramenta | Phase 0 | .claudeprompt | .gemini/GEMINI.md | Git |
|------------|---------|---------------|-------------------|-----|
| **Cowork** | ✅ | ✅ lê se existe | ❌ não aplica | Se disponível |
| **Claude Code** | ✅ | ✅ lê sempre | ❌ não aplica | ✅ sempre |
| **Antigravity** | ✅ | ❌ não aplica | ✅ lê sempre | ✅ sempre |

Se não souber qual ferramenta está rodando, ler ambos os config files e aplicar o relevante.
