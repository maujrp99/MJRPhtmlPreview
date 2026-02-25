---
description: Golden rules for AI-assisted development
---

# General Development Protocol

## 0. Onboarding
- If you were not onboarded, execute `onboarding_protocol.md` first.

## 1. Context & Planning
- [ ] Check for SDD files (`spec.md`, `plan.md`, `tasks.md`) in `docs/specs/<feature>/`.
- [ ] **Missing Docs?**: Ask the user: "Do we need an SDD for this?"
- [ ] Create/Update the plan if required.
- [ ] Read and follow `docs/specs/constitution.md`.

## 2. Execution (SDD)
- [ ] If new feature → Check `docs/specs/` for approved spec.
- [ ] Implement changes following defined architecture patterns and design system.
- [ ] Run build to verify.

## 3. Verification
- [ ] Run the project's test suite.
- [ ] Verify functionality (Evidence required).
- [ ] Run `regression_protocol.md` if applicable.

## 4. Documentation Sync
- [ ] Run `documentation_protocol.md` workflow.
- [ ] Update `docs/specs/tasks.md` to reflect completed work.

## 5. Completion
- [ ] Log in `docs/sessions/DEBUG_LOG.md` (if bug fix).
- [ ] Commit following Conventional Commits pattern.
- [ ] Request User Review.
