---
description: Architecture Decision Record (ADR) Protocol
---

# Architecture Decision Protocol (ADR)

Architecture Decision Records (ADR) provide a historical log of significant design choices, separating "Why we did it" (History) from "How it works" (Specs/Architecture docs).

## 1. When to Write an ADR

Create an ADR when a decision:
- Introduces a new framework, language, or storage engine.
- Changes a core architectural pattern.
- Has significant trade-offs (e.g., "Performance vs. Maintainability").
- Is difficult to reverse.

## 2. File Convention

- **Location**: `docs/architecture/`
- **Format**: `NNNN-short-title-kebab-case.md` (e.g., `0001-use-firebase-firestore.md`)
- **Numbering**: Sequential (0001, 0002, ...).

## 3. Workflow

1. **Draft**: Create the file, effectively proposing the change.
2. **Review**: Discuss with the team/user.
3. **Decision**: Mark as `Accepted` or `Rejected`.
4. **Merge**: Commit to the repository (`docs: ADR <number> — <title>`).
5. **Sync Specs**: **CRITICAL**. Once accepted, you MUST update `docs/specs/arch.md` and `docs/specs/constitution.md` to reflect the *new* truth. The ADR explains *why*, the spec explains *what is*.

## 4. ADR Template

Use the full template from `3.MJRP-Templates/adr_template.md`. Minimum fields:

```markdown
# ADR-NNNN: [Short Title]

**Status**: Accepted | Proposed | Rejected | Deprecated
**Date**: YYYY-MM-DD
**Deciders**: [List names]

## Context
[What is the issue? What constraints are we facing?]

## Options Considered
[At least 2 options with pros/cons]

## Decision
[We decided on Option X because...]

## Consequences
- **Positive**: [Benefit 1]
- **Negative**: [Trade-off 1]
- **Risks**: [Risk 1]

## Files Impacted
[Table of files that need updating after this decision]
```

## 5. Related

- **Full ADR template**: `3.MJRP-Templates/adr_template.md`
- **Debug triggers ADR**: `debug_protocol.md` §2 (fix requires Core Pattern change → ADR first)
- **Architecture compliance**: `code_quality_assessment_protocol.md`
- **Post-ADR doc sync**: `documentation_audit_protocol.md`
