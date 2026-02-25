---
description: Protocol for auditing and maintaining test suite health
---

# Test Suite Audit Protocol

Use this protocol when:
- Starting a "Test Revamp" sprint.
- After major architectural refactors (to ensure tests align).
- Periodically to catch regression/deprecation drift.

## Phase 1: Context & Architecture Alignment

**Goal**: Ensure the test strategy matches the current system architecture.

1. **Review System Architecture**:
   - Read `docs/specs/arch.md`.
   - Identify major recent changes (e.g., architectural refactors, new patterns).
2. **Verify Test Layering**:
   - Check if **Unit Tests** mock dependencies correctly.
   - Check if **Integration/E2E Tests** cover critical user flows without excessive implementation coupling.

## Phase 2: Gap Analysis

**Goal**: Identify code files that have no corresponding tests.

1. **Source Inventory**: List all source files (excluding libs/vendors).
2. **Test Inventory**: List all test files.
3. **Mapping**: Match Source → Test.
   - Generate a list of **Untested Components**.
4. **Criticality Assessment**: Mark untested components as High/Medium/Low priority based on usage.

## Phase 3: Pattern & Deprecation Audit

**Goal**: Remove legacy patterns and ensure best practices.

1. **Deprecation Scan**: Search for deprecated API usage or legacy test patterns.
2. **Mocking Consistency**: Ensure consistent mocking library/approach usage.
3. **Selector Health (E2E)**: Review if selectors use stable attributes (ids, data-attributes) or brittle paths.

## Phase 4: Integrity Check

**Goal**: Verify that the suite actually runs and passes cleanly.

1. **Run Full Suite**: Execute both unit and E2E tests.
2. **Flakiness Detection**: Run the suite 3 times. Note any inconsistent failures.
3. **Performance Check**: Identify tests that are abnormally slow. Mark for optimization.

## Phase 5: Regression Checklist Sync

**Goal**: Ensure the regression checklist reflects the current feature set.

1. **Review Regression Checklist**: Read `docs/specs/regression_checklist.md` (or `docs/manual/regression_checklist.md`).
2. **Tag Coverage**: Verify each major feature has a `[TAG]` section.
3. **New Tags**: Add tags for features that were added since last audit.
4. **Remove Tags**: Remove or archive tags for features that were removed.

## Phase 6: Reporting & Remediation

**Goal**: Document findings and plan fixes.

1. **Generate Report**: Create `docs/archive/test_audit_YYYY-MM-DD.md`.
   - Include: Coverage Summary, Flaky Tests List, Deprecation Count, Gap Analysis Table.
2. **Update Technical Debt**: Add "Missing Test Coverage" items to `docs/TECHNICAL_DEBT.md` (Category 3).
3. **Create Remediation Rules**: Update testing guidelines if new patterns are established.
4. **Task Creation**: Create tasks in `docs/specs/tasks.md` for fixing identified gaps.

---

## Related

- **Technical Debt template**: `3.MJRP-Templates/technical_debt.md`
- **Regression Checklist (modular)**: `regression_protocol.md`
- **QA Strategy**: QA Engineer skill
- **Code Quality**: `code_quality_assessment_protocol.md`

---

**Prompt for AI Agent**:
"Run the Test Suite Audit Protocol. Start by reading the architecture docs, then list current test files and perform a gap analysis. Check for deprecated patterns. Sync the regression checklist tags. Finally, generate a report."
