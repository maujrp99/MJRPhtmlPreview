---
description: SDD — Tasking Phase (tasks.md)
---

# SDD: Tasking Phase (`tasks.md`)

**Goal**: Define WHEN and Order of Operations. Decompose the plan into atomic, verifiable units of work.

> **Parent workflow**: `sdd_protocol.md` — This is Stage 3 of 4.
> **Prerequisite**: `plan.md` must be APPROVED.

## Process

1. Agent creates/updates `docs/specs/<feature>/tasks.md`.
2. Checklist items must be granular, reflecting exactly what was defined in plan.md, and verifiable.
3. Add tasks for running the project's test suite after implementation.
4. Add a final task for running the build.
5. Agent requests User Review.
6. **Gate**: Start Execution only after Tasks are APPROVED.
7. **Commit**: `docs: generate tasks for <feature>`

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
