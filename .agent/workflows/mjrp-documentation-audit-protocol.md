---
description: Audit protocol to keep documentation aligned with code
---

# Documentation Audit Protocol

**Purpose**: Systematic process for verifying that **Spec documents** match the **Code**.

## 1. Identify Changes

Assess which functional areas have been modified since the last audit.

## 2. Map to Spec Documents

Consult this map to find the relevant SpecKit artifacts:

### System & Architecture
- **Architecture & Patterns**: `docs/specs/arch.md`
- **Technical Stack & Rules**: `docs/specs/constitution.md`
- **Data Models**: `docs/specs/data-model.md`

### Features & Requirements
- **User Stories**: `docs/specs/story.md`
- **Specifications**: `docs/specs/spec.md`
- **Task Backlog**: `docs/specs/tasks.md`

### Design & UI
- **Visual System**: `docs/specs/design-system.md`

### Governance
- **ADRs**: `docs/architecture/` (Verify alignment with constitution.md)
- **Workflows**: Workflow files (Verify alignment with actual agent behavior)
- **Session History**: `docs/sessions/SESSION_HISTORY.md`

### Reference & Operational
- **Reference Guide Index**: `docs/manual/00_INDEX.md` (Verify all manual docs are indexed)
- **Technical Debt**: `docs/TECHNICAL_DEBT.md` (Update with newly discovered debt)
- **Regression Checklist**: `docs/specs/regression_checklist.md` (Verify tags match current features)
- **Debug Log**: `docs/sessions/DEBUG_LOG.md` (Verify issue numbering is sequential)

### Project Definition
- **Vision**: `VISION.md`
- **Charter**: `CHARTER.md` — Verify scope, goals, and success metrics still reflect reality. Update when:
  - A milestone is completed and metrics need refreshing
  - Scope expanded or contracted (in/out of MVP)
  - Stakeholders or success criteria changed
  - **After any scope update**: cascade to `ROADMAP.md` (milestone alignment) and `story.md` (mark out-of-scope stories as `🚫 Deferred`). CHARTER changes require explicit human approval before commit.
- **README**: `README.md`

## 3. Update Documentation

1. **Read** the relevant spec file.
2. **Update** the file to reflect the new code reality.
   - *Rule*: Documentation must match Code. If Code changes, Docs MUST change.

## 4. Changelog

1. If the project maintains a `CHANGELOG.md`, add a concise entry under the [Unreleased] section.

## 5. The Snapshot Protocol (Optional)

For larger projects, maintain periodic snapshots:
1. **Inspect**: Check if a significant milestone has been reached.
2. **Decide**: If major features have shipped since last snapshot:
   - **Archive**: Move the old snapshot to `docs/archive/`.
   - **Regenerate**: Create a new snapshot reflecting the current state.
