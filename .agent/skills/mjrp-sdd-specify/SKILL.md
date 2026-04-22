---
name: mjrp-sdd-specify
description: >
  MJRP SDD Stage 1 Specification Phase. Creates spec.md defining WHAT and WHY with problem statement and success criteria.
  Trigger: sdd specify, create spec.md, spec phase, write spec, SDD specification, fase de especificacao, criar spec.
---

# SDD: Specification Phase (`spec.md`)

**Goal**: Define WHAT, WHY, and Success Criteria. No implementation details.

> **Parent workflow**: `mjrp-sdd-protocol.md` — This is Stage 1 of 4.

## ✋ Pré-Gate: Verificar story.md antes de iniciar

Leia `docs/specs/story.md`. Verifique o **conteúdo**, não só a existência do arquivo:

- [ ] Há pelo menos um `US-XXX` com título definido
- [ ] Cada `US-XXX` tem pelo menos um Acceptance Criterion (AC) listado
- [ ] As stories cobrem o escopo que o usuário descreveu para esta feature

**Se qualquer item falhar → BLOQUEADO. Não inicie o Specify.**
Informe: *"story.md não tem US mapeadas com ACs. Use `mjrp-ba-sm` para escrever as stories antes de iniciar o Specify."*

---

## Process

0. If Agent does not have requirements, ask the requirements or idea from the human user.
1. Agent creates specification considering `docs/specs/constitution.md` and `docs/specs/arch.md`.
2. Agent creates/updates `docs/specs/<feature>/spec.md`.
3. **✋ Pós-Gate: Coverage Check** — antes de apresentar ao usuário, verifique internamente:
   - Cada `US-XXX` de story.md tem um `REQ-XXX` correspondente em spec.md?
   - Cada AC de cada US está refletido em `## Success Criteria`?
   - Itens "out of scope" de story.md aparecem em `## Out of Scope`?
   - **Se ❌ encontrado → corrigir spec.md antes de apresentar. O usuário não deve ver um spec que dropa itens de story.md.**
4. Agent requests User Review.
5. User validates or requests changes.
6. **Gate**: Cannot proceed to Plan until Spec is APPROVED.
7. **Commit**: `docs: complete specify stage for <feature>`

## Spec Template

```markdown
# Feature: [Name]

**Status**: Draft | In Review | Approved | Implemented
**Date**: YYYY-MM-DD
**Author**: [Name/Agent]

## Problem Statement
[What problem are we solving? Why now?]

## User Stories
- As a [user], I want [action], so that [benefit].

## Requirements
### Functional
- [REQ-01] [Description]
- [REQ-02] [Description]

### Non-Functional
- [NFR-01] [Performance/Security/Accessibility requirement]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

## Out of Scope
- [What this feature does NOT include]

## Open Questions
- [Questions to resolve before proceeding to Plan]
```

## Rules
- No implementation details (no "use library X" or "create component Y").
- Focus on the WHAT and WHY, not the HOW.
- If the feature has UI, include high-level user flow descriptions (not mockups — those go in Plan).
