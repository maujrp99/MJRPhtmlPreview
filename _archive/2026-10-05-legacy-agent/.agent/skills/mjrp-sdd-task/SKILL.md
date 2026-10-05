---
name: mjrp-sdd-task
description: >
  MJRP SDD Stage 3 Tasking Phase. Creates tasks.md decomposing the plan into atomic verifiable units of work.
  Trigger: sdd task, create tasks.md, tasking phase, write tasks, SDD tasks, fase de tarefas, criar tasks.
---

# SDD: Tasking Phase (`tasks.md`)

**Goal**: Define WHEN and Order of Operations. Decompose the plan into atomic, verifiable units of work.

> **Parent workflow**: `mjrp-sdd-protocol.md` — This is Stage 3 of 4.
> **Prerequisite**: `plan.md` must be APPROVED.

## ✋ Pré-Gate: Verificar plan.md antes de iniciar

Leia `docs/specs/<feature>/plan.md`. Verifique o **conteúdo**:

- [ ] Status é `Approved`
- [ ] Há componentes/módulos explicitamente definidos em `## Components / Modules`
- [ ] Para features com UI: mockups ou wireframes existem em `## UI/UX Design`

**Se qualquer item falhar → BLOQUEADO. Não inicie o Tasking.**
Informe: *"plan.md não está aprovado ou não tem componentes definidos. Conclua o Plan primeiro."*

---

## Process

1. Agent creates/updates `docs/specs/<feature>/tasks.md`.
2. Checklist items must be granular, reflecting exactly what was defined in plan.md, and verifiable.
3. Add tasks for running the project's test suite after implementation.
4. Add a final task for running the build.
5. **✋ Pós-Gate: Coverage Check** — antes de apresentar ao usuário, verifique internamente:
   - Cada componente/módulo de plan.md tem ≥1 task de implementação?
   - Cada `REQ-XXX` de spec.md tem ≥1 task que o endereça?
   - Cada `US-XXX` de story.md aparece como tag `[US-XXX]` em pelo menos uma task?
   - Success criteria de spec.md têm tasks de verificação correspondentes?
   - **Se ❌ encontrado → adicionar as tasks faltantes antes de apresentar.**
6. Agent requests User Review.
7. **Gate**: Start Execution only after Tasks are APPROVED.
8. **Commit**: `docs: generate tasks for <feature>`

## Tasks Template

```markdown
# Tasks: [Feature Name]

**Status**: Draft | In Review | Approved | In Progress | Complete
**Date**: YYYY-MM-DD
**Plan Reference**: docs/specs/<feature>/plan.md

## Pre-Implementation
- [ ] Create feature branch: `feat/<feature-name>-<timestamp>`
- [ ] Verify spec and plan are APPROVED

## Implementation
- [ ] [Task 1 — atomic, verifiable action]
- [ ] [Task 2 — atomic, verifiable action]
- [ ] [Task 3 — atomic, verifiable action]
- [ ] ...

## Verification
- [ ] Run test suite
- [ ] Run build
- [ ] Manual verification of happy path
- [ ] Regression check on affected areas

## Documentation
- [ ] Update relevant spec documents
- [ ] Update tasks.md with completion status
- [ ] Commit: `feat: implement <feature>`
```

## Rules for Good Tasks
- **Atomic**: Each task should be completable in one focused coding session.
- **Verifiable**: Each task must have a clear "done" criteria.
- **Ordered**: Tasks should be sequenced respecting dependencies.
- **Traceable**: Each task should map to something in plan.md.
- **No token overflow**: Tasks should be small enough that an AI agent can complete one without exceeding its context window.
- **Workflow Interruption**: If architecture changes → go back to Plan.
