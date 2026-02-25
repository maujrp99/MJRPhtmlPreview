---
description: SDD — Specification Phase (spec.md)
---

# SDD: Specification Phase (`spec.md`)

**Goal**: Define WHAT, WHY, and Success Criteria. No implementation details.

> **Parent workflow**: `sdd_protocol.md` — This is Stage 1 of 4.

## Process

0. If Agent does not have requirements, ask the requirements or idea from the human user.
1. Agent creates specification considering `docs/specs/constitution.md` and `docs/specs/arch.md`.
2. Agent creates/updates `docs/specs/<feature>/spec.md`.
3. Agent requests User Review.
4. User validates or requests changes.
5. **Gate**: Cannot proceed to Plan until Spec is APPROVED.
6. **Commit**: `docs: complete specify stage for <feature>`

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
