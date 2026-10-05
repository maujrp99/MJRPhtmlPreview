---
name: Code Quality & Architecture Assessment
description: >
  Use when EVALUATING existing code architecture: detect layer violations,
  measure modularity and componentization, assess maintainability, check
  constitution.md compliance, and produce assessment reports with remediation
  plans. This skill is for structural analysis of code — not for test planning
  (see QA Engineer) or writing new code (see Frontend/Backend Developer).
---

# Skill: Code Quality & Architecture Assessment

**Purpose**: Teach an AI agent how to evaluate code quality, detect architecture violations, and produce actionable assessment reports.

**Related Workflows**: `code_quality_assessment_protocol.md`, `regression_protocol.md`, `architecture_decision_protocol.md`
**Related Templates**: `technical_debt.md`, `adr_template.md`

---

## Quality Dimensions

### 1. Separation of Concerns (SoC)

**The Principle**: Each layer/module has ONE job. UI renders, Logic computes, Data persists.

**How to Test**:
- Pick a random component/controller → Does it contain business logic? (Bad)
- Pick a random view → Does it import from the data layer directly? (Bad)
- Pick a random service → Does it manipulate DOM? (Bad)

**Layer Compliance Matrix** (adapt to your architecture):

| Layer | CAN access | CANNOT access |
|-------|-----------|---------------|
| Views/Components | Controllers, Props, Design tokens | Repositories, DB, APIs directly |
| Controllers/Services | Stores, other Services | DOM, window, document |
| Stores/State | APIs, persistence | DOM, Views |
| API/Routes | Services, Libraries | DOM, Views, State |

### 2. Modularization

**The Principle**: Features are isolated. Deleting one feature shouldn't break another.

**How to Test**:
- **The Isolation Test**: Can you delete Feature A's folder and still build Feature B?
- **The Import Test**: Does Feature A import from Feature B's internals? (Bad — should use shared/core)

**Coupling Score**: Count cross-feature imports. Target: **0**.

### 3. Componentization

**The Principle**: UI is built from small, reusable, "dumb" components composed together.

**Metrics**:
- **Atomic Density**: Dumb components / Total components → Target: > 70%
- **Prop Depth**: Max levels of prop drilling → Target: < 3
- **God Components**: Components > 300 LOC → Target: 0

### 4. Maintainability

**Red Flags**:
- Files > 400 LOC (God Files)
- Functions > 50 LOC (should be decomposed)
- Deeply nested conditionals (> 3 levels)
- Duplicated code blocks (DRY violations)
- Magic numbers/strings (should be constants)

---

## Assessment Process

### 1. Automated Checks
```bash
# Find large files
find src/ -name "*.ts" -o -name "*.tsx" -o -name "*.js" | xargs wc -l | sort -rn | head -20

# Find cross-feature imports (adapt paths)
grep -r "from.*features/other-feature" src/features/my-feature/

# Find TODO/FIXME/HACK
grep -rn "TODO\|FIXME\|HACK\|XXX" src/
```

### 2. Manual Stress Tests

Run these 3 tests and log results:

**A. Controller Diet Test**
- Pick 3 random controllers/services
- Check: Do they compute or just orchestrate?
- Score: PASS (orchestrate) / FAIL (compute)

**B. Feature Wall Test**
- Pick 2 features
- Check: Are they independent?
- Score: PASS (independent) / FAIL (coupled)

**C. Composition Test**
- Trace a piece of data through the component tree
- Check: How many levels does it pass through without being used?
- Score: PASS (< 3) / FAIL (>= 3)

### 3. Constitution Compliance

Compare actual code patterns against `docs/specs/constitution.md`:
- Stack matches? (correct framework versions, libraries)
- Patterns followed? (naming, file structure, imports)
- Anti-patterns avoided? (things constitution says NOT to do)

---

## Report Template

```markdown
# Quality Assessment: [Date]

**Assessor**: [Name/Agent]
**Scope**: [Full project / Specific feature]

## Scorecard

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Atomic Density | X% | > 70% | ✅/❌ |
| Prop Depth | X | < 3 | ✅/❌ |
| Feature Coupling | X imports | 0 | ✅/❌ |
| Layer Violations | X | 0 | ✅/❌ |
| God Files | X files | 0 | ✅/❌ |

## Stress Test Results
- **Controller Diet**: [PASS/FAIL] — [details]
- **Feature Wall**: [PASS/FAIL] — [details]
- **Composition**: [PASS/FAIL] — [details]

## Constitution Compliance
- [✅/❌] Stack matches constitution.md
- [✅/❌] Patterns followed
- [✅/❌] No anti-patterns detected

## Top Issues (by severity)
1. [CRITICAL] [Description] — [File] — [Suggested fix]
2. [HIGH] [Description] — [File] — [Suggested fix]
3. [MEDIUM] [Description] — [File] — [Suggested fix]

## Remediation Plan
- [ ] [Task 1 — add to tasks.md]
- [ ] [Task 2]
```

---

## Scope & Boundaries

This skill evaluates **code structure and architecture** — not functional correctness:

```
"Is the codebase well-organized?"           → Code Quality (this skill)
"Does the feature work correctly?"          → QA Engineer (test strategy)
"Are there layer violations?"               → Code Quality (this skill)
"What tests should we write?"               → QA Engineer
"How do I refactor this component?"         → Frontend Developer or Backend Developer
"Does the UI meet accessibility standards?" → UX/UI Designer
```

### Decision Tree

```
Assessing overall code health or architecture?
  └─ YES → Code Quality & Architecture Assessment
Planning what to test or writing acceptance criteria?
  └─ YES → QA Engineer
Checking if constitution.md rules are followed?
  └─ YES → Code Quality & Architecture Assessment
Writing or refactoring actual code?
  └─ Frontend? → Frontend Developer
  └─ Backend? → Backend Developer
```

---

## When to Run

- End of every sprint
- After major refactors
- Before major new features (baseline)
- When the human asks for it
- After onboarding to a new codebase (initial assessment)
