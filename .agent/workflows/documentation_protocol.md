---
description: Documentation protocol and post-implementation checklist
---

# Documentation Protocol & Post-Implementation Checklist

**Purpose**: Defines the Single Source of Truth for documentation and the mandatory checklist after coding.

## 1. The Documentation Map

We rely on a **Spec-Driven** documentation system aligned with the MJRP Vibe Coding Framework.

### **SpecKit (The Technical Truth)**
- **Location**: `docs/specs/`
- **Purpose**: Describes the *current* state of the system (constitution, architecture, data models, stories, specs, tasks, design system).
- **Rule**: If you change code, you **MUST** update the corresponding spec document.

### **Architecture Decision Records (The History)**
- **Location**: `docs/architecture/`
- **Purpose**: Explains *why* a decision was made.
- **Rule**: Never update old ADRs. Create new ones to supersede.

### **Session History (The Context)**
- **Location**: `docs/sessions/`
- **Purpose**: Preserves session context across AI tools and time.

---

## 2. Post-Implementation Checklist

> **Trigger**: Run this checklist after every feature implementation or significant bug fix.

### Immediate Actions
- [ ] **Check Specs**: Did I touch a feature covered in `docs/specs/`?
  - If YES: Update the relevant spec document (story.md, arch.md, data-model.md) to match the new code.
- [ ] **Check Constitution**: Did I introduce a new pattern or dependency?
  - If YES: Update `docs/specs/constitution.md`.
- [ ] **Check Design System**: Did I change UI patterns?
  - If YES: Update `docs/specs/design-system.md`.
- [ ] **Check Tasks**: Update `docs/specs/tasks.md` to mark completed items.

### For Bug Fixes
- [ ] **Debug Log**: Add entry to `docs/sessions/DEBUG_LOG.md`.
  - Format: `[Date] [IssueID] [Root Cause] [Fix]`.

### For Architecture Changes
- [ ] **ADR**: Did I change a core pattern?
  - If YES: Create a new ADR in `docs/architecture/`.

---

## 3. Maintenance

- **Periodic Audit**: Run `documentation_audit_protocol.md` monthly or when instructed.
- **Archive Policy**: Do not delete useful history; move it to `docs/archive/`.
