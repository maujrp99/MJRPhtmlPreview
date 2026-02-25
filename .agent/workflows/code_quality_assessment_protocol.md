---
description: Code and Architecture Quality Assessment
---

# Code Quality Assessment Protocol v3.0

Execute this protocol at the end of every sprint or major architectural milestone, or whenever the human user requests it.

## 1. Preparation

1. **Identify Scope**: Determine if the assessment covers the entire project or specific components.
2. **Environment Check**: Ensure tests pass (run project test suite).
3. **Baseline**: Check `docs/archive/` for previous assessments.

## 2. Quantitative Metrics (The Hard Numbers)

| Metric Group | Specific Metric | Formula/Definition | Target |
| :--- | :--- | :--- | :--- |
| **Componentization** | **Atomic Density** | "Dumb" Components / Total Components | > 70% |
| **Componentization** | **Prop Depth** | Max depth of prop passing chain | < 3 |
| **Modularization** | **Feature Coupling** | Cross-feature internal imports | **0** |
| **SoC** | **Layer Violations** | View → Repository or Controller → DOM imports | **0** |
| **Maintainability** | **God Files** | Files > 400 LOC | 0 |
| **Backend Health** | **Route Thinness** | Routes > 50 LOC (Should delegate to Service/Lib) | 0 |

> **Note**: Adapt metrics to your project's stack. The above are examples for component-based frontend + API backend architectures.

## 3. Structural Stress Tests (The "Real Quality" Checks)

### A. Separation of Concerns (The "Controller Diet")
- **The Controller Test**: Pick a random Controller/Service.
  - *Fail*: If it loops through data to "calculate" totals (Business Logic leakage).
  - *Pass*: If it delegates to a Service/Store and just passes the result.
- **The View Test**: Pick a random View/Component.
  - *Fail*: If it has complex business logic inside the render.
  - *Pass*: If it renders pre-computed data (Logic derived elsewhere).

### B. Modularization (The "Feature Wall")
- **The Isolation Test**: Can you delete one feature module and still build the others?
  - *Fail*: If features import each other's internals.
  - *Pass*: If they rely only on shared/core modules.

### C. Componentization (The "Composition" Check)
- **The Prop Drill**: Trace a piece of data through the component tree.
  - *Fail*: Data passes through 4+ levels without being used.
  - *Pass*: Components connect to stores/context directly, or composition is used.

## 4. Deep Architecture Audit

Verify compliance against the project's defined architecture (`docs/specs/arch.md` and `docs/specs/constitution.md`):

### A. Layer Compliance
- Verify that each architectural layer respects its boundaries as defined in the architecture document.
- Check for unauthorized cross-layer imports.

### B. Backend Integrity
- Routes/API endpoints should be thin wrappers delegating to services/libraries.

## 5. Technical Debt Update

After the assessment, update `docs/TECHNICAL_DEBT.md` (use template from `3.MJRP-Templates/technical_debt.md`):

1. **God Files**: Add any files > 400 LOC found in §2
2. **Coupling**: Add any cross-feature imports found in §3.B
3. **Pattern Violations**: Add any constitution violations found in §4
4. **Missing Tests**: Cross-reference with `test_suite_audit_protocol.md` results
5. **Remediation Plan**: Prioritize items and create tasks in `docs/specs/tasks.md`

## 6. Report Generation

Create a **Snapshot Report** in `docs/archive/quality_assessment_YYYY-MM-DD.md`.

### Template
```markdown
# Quality Assessment: [Date]
**Assessor**: [Name/Agent]

## 1. Scorecard
[Insert Metrics Table from §2]

## 2. Stress Test Results
- **Controller Diet**: [Pass/Fail] - [Details]
- **Feature Wall**: [Pass/Fail] - [Details]
- **Composition**: [Pass/Fail] - [Details]

## 3. Constitution Compliance
- [✅/❌] Stack matches constitution.md
- [✅/❌] Patterns followed
- [✅/❌] No anti-patterns detected

## 4. Violations & Remediation Plan
- [ ] [Violation 1] — [Proposed fix] — [Priority]
- [ ] [Violation 2] — [Proposed fix] — [Priority]

## 5. Technical Debt Delta
- New items added to TECHNICAL_DEBT.md: [count]
- Items resolved since last assessment: [count]
```

## 7. Related

- **Technical Debt template**: `3.MJRP-Templates/technical_debt.md`
- **Test coverage gaps**: `test_suite_audit_protocol.md`
- **ADRs for pattern changes**: `architecture_decision_protocol.md`
