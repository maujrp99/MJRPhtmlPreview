---
name: mjrp-sdd-plan
description: >
  MJRP SDD Stage 2 Planning Phase. Creates plan.md defining HOW with architecture approach and UI mockups.
  Trigger: sdd plan, create plan.md, planning phase, write plan, SDD planning, plano SDD, fase de planejamento.
---

# SDD: Planning Phase (`plan.md`)

**Goal**: Define HOW (Architecture, UI/UX, Component Strategy).

> **Parent workflow**: `mjrp-sdd-protocol.md` — This is Stage 2 of 4.
> **Prerequisite**: `spec.md` must be APPROVED.

## ✋ Pré-Gate: Verificar spec.md antes de iniciar

Leia `docs/specs/<feature>/spec.md`. Verifique o **conteúdo**:

- [ ] Status é `Approved` (não Draft ou In Review)
- [ ] Há pelo menos um `REQ-XXX` definido — spec sem REQ-IDs não é spec, é rascunho
- [ ] `## Success Criteria` existe e tem itens mensuráveis

**Se qualquer item falhar → BLOQUEADO. Não inicie o Plan.**
Informe: *"spec.md não está aprovada ou não tem REQ-IDs. Conclua o Specify primeiro."*

---

## Process

1. Agent creates/updates `docs/specs/<feature>/plan.md`.
2. Agent includes logic flows and **UI Mockups** (Critical for frontend features).
3. Agent researches project documentation: `docs/specs/arch.md`, `docs/specs/data-model.md`, `docs/specs/design-system.md` (if applicable). Agent follows `docs/specs/constitution.md` guidelines.
4. Agent informs the user which documents were consulted and what information was considered in the plan.
5. **✋ Pós-Gate: Coverage Check** — antes de apresentar ao usuário, verifique internamente:
   - Cada `REQ-XXX` de spec.md tem componente/seção correspondente no plan.md?
   - Cada `US-XXX` de story.md tem pelo menos um componente ou fluxo que a enderessa?
   - Constraints (performance, segurança, a11y) de spec.md aparecem no plan — não foram suavizados?
   - **Se ❌ encontrado → corrigir plan.md antes de apresentar.**
6. Agent requests User Review and if needed creates a new branch.
7. User validates strategy and visuals.
8. **Gate**: Cannot proceed to Task List until Plan is APPROVED.
9. **Commit**: `docs: complete plan stage for <feature>`

## Plan Template

```markdown
# Plan: [Feature Name]

**Status**: Draft | In Review | Approved
**Date**: YYYY-MM-DD
**Spec Reference**: docs/specs/<feature>/spec.md

## Architecture Approach
[How does this feature fit into the existing architecture?]
[Which components/services are affected?]

## Technical Design
### Data Flow
[Describe or diagram the data flow]

### Components / Modules
- [Component 1]: [Responsibility]
- [Component 2]: [Responsibility]

### API / Interface Changes
[New endpoints, modified interfaces, schema changes]

## UI/UX Design (if applicable)
### Mockups
[ASCII mockups, Stitch references, or visual descriptions]

### User Flow
[Step-by-step user interaction flow]

## Dependencies
- [Existing module/service this depends on]
- [New library needed — must align with constitution.md]

## Documents Consulted
- [List of spec/arch files read and key takeaways]

## Risks & Considerations
- [Risk 1]: [Mitigation]
```

## Rules
- **Visuals First**: For UI changes, mockups (ASCII, Stitch, or descriptions) are mandatory.
- Must reference and align with `docs/specs/constitution.md` for tech choices.
- If the plan requires a new dependency or pattern change → flag for ADR consideration.
- **Workflow Interruption**: If User changes requirements → go back to Specify.
