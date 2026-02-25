---
description: SDD — Planning Phase (plan.md)
---

# SDD: Planning Phase (`plan.md`)

**Goal**: Define HOW (Architecture, UI/UX, Component Strategy).

> **Parent workflow**: `sdd_protocol.md` — This is Stage 2 of 4.
> **Prerequisite**: `spec.md` must be APPROVED.

## Process

1. Agent creates/updates `docs/specs/<feature>/plan.md`.
2. Agent includes logic flows and **UI Mockups** (Critical for frontend features).
3. Agent researches project documentation: `docs/specs/arch.md`, `docs/specs/data-model.md`, `docs/specs/design-system.md` (if applicable). Agent follows `docs/specs/constitution.md` guidelines.
4. Agent informs the user which documents were consulted and what information was considered in the plan.
5. Agent requests User Review and if needed creates a new branch.
6. User validates strategy and visuals.
7. **Gate**: Cannot proceed to Task List until Plan is APPROVED.
8. **Commit**: `docs: complete plan stage for <feature>`

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
