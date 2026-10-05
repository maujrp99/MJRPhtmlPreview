---
name: mjrp-sdd
description: >
  MJRP Specification Defined Development full flow: Specify, Plan, Task, Implement with mandatory human approval gates.
  Trigger: SDD, spec driven development, start SDD, full SDD flow, iniciar SDD, desenvolvimento orientado a spec.
---


# Specification Defined Development (SDD) Protocol

**Purpose**: To ensure alignment, reduce rework, and guarantee that what is built matches the user's vision.

> **Reference**: This workflow implements the SpecKit stages defined in the MJRP Vibe Coding Framework (Section 5).

## The Flow

### 1. Specification Phase (`spec.md`)
**Goal**: Define WHAT, WHY, and Success Criteria. No implementation details.

0. If Agent does not have requirements, ask the requirements or idea from the human user.
1. **✋ Pré-Gate**: story.md tem `US-XXX` com ACs? Se não → BLOQUEADO, use `mjrp-ba-sm` primeiro.
2. Agent creates specification considering `docs/specs/constitution.md` and `docs/specs/arch.md`.
3. Agent creates/updates `docs/specs/<feature>/spec.md`.
4. **✋ Pós-Gate**: cada US-XXX tem REQ correspondente? cada AC refletido em Success Criteria? Se ❌ → corrigir antes de apresentar.
5. Agent requests User Review.
6. User validates or requests changes.
7. **Gate**: Cannot proceed to Plan until Spec is APPROVED.
8. **Commit**: `docs: complete specify stage for <feature>`

### 2. Planning Phase (`plan.md`)
**Goal**: Define HOW (Architecture, UI/UX, Component Strategy).

1. **✋ Pré-Gate**: spec.md tem REQ-IDs e status Approved? Se não → BLOQUEADO.
2. Agent creates/updates `docs/specs/<feature>/plan.md`.
3. Agent includes logic flows and **UI Mockups** (Critical for frontend).
4. Agent researches project documentation starting by `docs/specs/arch.md`, `docs/specs/data-model.md`, and `docs/specs/design-system.md` (if applicable). Agent follows `docs/specs/constitution.md` guidelines.
5. Agent informs the user which documents were consulted and what information were considered in the plan.
6. **✋ Pós-Gate**: cada REQ-XXX de spec.md tem componente no plan? cada US-XXX de story.md endereçada? Se ❌ → corrigir antes de apresentar.
7. Agent requests User Review and if needed creates a new branch.
8. User validates strategy and visuals.
9. **Gate**: Cannot proceed to Task List until Plan is APPROVED.
10. **Commit**: `docs: complete plan stage for <feature>`

### 3. Tasking Phase (`tasks.md`)
**Goal**: Define WHEN and Order of Operations.

1. **✋ Pré-Gate**: plan.md tem componentes definidos e status Approved? Se não → BLOQUEADO.
2. Agent creates/updates `docs/specs/<feature>/tasks.md`.
3. Checklist items must be granular, reflecting exactly what was added to the plan.md, and verifiable.
4. Add tasks for running the project's test suite and build commands after the implementation.
5. **✋ Pós-Gate**: cada componente do plan tem ≥1 task? cada REQ-XXX tem ≥1 task? cada US-XXX tagueada [US-XXX] em ≥1 task? Se ❌ → adicionar tasks antes de apresentar.
6. Agent requests User Review.
7. **Gate**: Start Execution only after Tasks are APPROVED.
8. **Commit**: `docs: generate tasks for <feature>`

### 4. Implementation Phase
**Goal**: Execute task by task, producing code that adheres to the spec and constitution.

1. Agent picks tasks one at a time from `tasks.md`.
2. Agent implements following `docs/specs/constitution.md` patterns and architecture.
3. Agent runs tests and build to verify.
4. Agent marks tasks as complete in `tasks.md`.
5. **Commit**: `feat: implement <description>` (ref task)

## Rules
- **One Stage at a Time**: Do not create all docs at once.
- **Gates are Mandatory**: Agent MUST request human approval between every stage. Cannot advance without explicit APPROVED.
- **Visuals First**: For UI changes, visuals (or ASCII mocks) must be in the Plan or Spec depending on complexity.
- **Workflow Interruption**: If User changes requirements during Plan → go back to Spec. If architecture changes during Tasks → go back to Plan. If scope changes during Implement → go back to appropriate stage. Rollback generates commit: `docs: revise <stage> for <feature> — requirement change`

## Definition of "APPROVED"

Approval is an **explicit message from the human in the chat** confirming the stage is accepted. Examples:
- "Aprovado, pode avançar"
- "LGTM, proceed to Plan"
- "Approved" / "Go ahead"

**The agent MUST NOT**:
- Auto-approve any stage transition
- Interpret silence as approval
- Proceed based on lack of objection

If the human says "looks good but change X", that is NOT approval — it's a revision request. Apply the change first, then request approval again.
