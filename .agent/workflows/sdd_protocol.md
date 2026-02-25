---
description: Specification Defined Development (SDD) Protocol — Full Flow
---

# Specification Defined Development (SDD) Protocol

**Purpose**: To ensure alignment, reduce rework, and guarantee that what is built matches the user's vision.

> **Reference**: This workflow implements the SpecKit stages defined in the MJRP Vibe Coding Framework (Section 5).

## The Flow

### 1. Specification Phase (`spec.md`)
**Goal**: Define WHAT, WHY, and Success Criteria. No implementation details.

0. If Agent does not have requirements, ask the requirements or idea from the human user.
1. Agent creates specification considering `docs/specs/constitution.md` and `docs/specs/arch.md`.
2. Agent creates/updates `docs/specs/<feature>/spec.md`.
3. Agent requests User Review.
4. User validates or requests changes.
5. **Gate**: Cannot proceed to Plan until Spec is APPROVED.
6. **Commit**: `docs: complete specify stage for <feature>`

### 2. Planning Phase (`plan.md`)
**Goal**: Define HOW (Architecture, UI/UX, Component Strategy).

1. Agent creates/updates `docs/specs/<feature>/plan.md`.
2. Agent includes logic flows and **UI Mockups** (Critical for frontend).
3. Agent researches project documentation starting by `docs/specs/arch.md`, `docs/specs/data-model.md`, and `docs/specs/design-system.md` (if applicable). Agent follows `docs/specs/constitution.md` guidelines.
4. Agent informs the user which documents were consulted and what information were considered in the plan.
5. Agent requests User Review and if needed creates a new branch.
6. User validates strategy and visuals.
7. **Gate**: Cannot proceed to Task List until Plan is APPROVED.
8. **Commit**: `docs: complete plan stage for <feature>`

### 3. Tasking Phase (`tasks.md`)
**Goal**: Define WHEN and Order of Operations.

1. Agent creates/updates `docs/specs/<feature>/tasks.md`.
2. Checklist items must be granular, reflecting exactly what was added to the plan.md, and verifiable.
3. Add tasks for running the project's test suite and build commands after the implementation.
4. Agent requests User Review.
5. **Gate**: Start Execution only after Tasks are APPROVED.
6. **Commit**: `docs: generate tasks for <feature>`

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
