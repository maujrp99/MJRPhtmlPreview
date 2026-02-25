---
name: QA Engineer
description: >
  Use when planning WHAT to test, deriving test cases from spec.md, writing
  acceptance criteria, discovering edge cases, planning regression strategy,
  writing bug reports, or defining "definition of done". This skill owns test
  STRATEGY and PLANNING — not the implementation of tests (see Frontend Developer
  or Backend Developer skills for how to write tests in code).
---

# Skill: QA Engineer

**Purpose**: Teach an AI agent how to approach quality assurance — not just writing tests, but thinking about quality holistically: what to test, how to test, when to test, and what "done" really means.

**Related Workflows**: `regression_protocol.md`, `test_suite_audit_protocol.md`, `code_quality_assessment_protocol.md`
**Related Templates**: `onboarding_qa.md`, `technical_debt.md` (Category 3: Missing Tests)

---

## 1. Test Strategy

### The Test Pyramid

```
            ╱╲
           ╱ E2E ╲           Few: 5-10 critical user journeys
          ╱────────╲
         ╱Integration╲       Some: API + DB + service interactions
        ╱──────────────╲
       ╱  Component/UI   ╲   Moderate: Rendered components with states
      ╱────────────────────╲
     ╱    Unit Tests         ╲  Many: Pure logic, utils, validators
    ╱__________________________╲
```

### Cost-Benefit by Layer

| Layer | Speed | Maintenance | Confidence | Write When |
|-------|-------|-------------|------------|------------|
| **Unit** | ⚡ Fast | 🟢 Low | Per function | Business logic, validators, transformers |
| **Component** | ⚡ Fast | 🟡 Medium | Per component | UI states, props, events |
| **Integration** | 🔄 Medium | 🟡 Medium | Per feature | API routes, DB queries, service chains |
| **E2E** | 🐢 Slow | 🔴 High | Per journey | Login, checkout, onboarding, critical paths |

### The "Ice Cream Cone" Anti-pattern (avoid)
```
❌ Too many E2E, few unit tests → Slow suite, flaky, expensive to maintain
✅ Many unit/component, few E2E → Fast feedback, stable, focused E2E on critical paths
```

---

## 2. Deriving Tests from spec.md

### From Requirements to Test Cases

Every requirement in spec.md (REQ-01, REQ-02...) should generate test cases:

```markdown
## REQ-03: Book cards display cover, title, author, and garden status emoji

### Test Cases:
- TC-03.1: Book card renders all 4 elements when data is complete
- TC-03.2: Book card shows placeholder when cover image is missing
- TC-03.3: Book card shows "Unknown Author" when author field is empty
- TC-03.4: Garden status emoji maps correctly (🌱=seedling, 🌿=growing, 🌳=evergreen)
- TC-03.5: Book card is keyboard-accessible and screen-reader friendly
```

### Traceability Matrix

| Requirement | Test Cases | Automated? | Status |
|-------------|-----------|------------|--------|
| REQ-01 | TC-01.1, TC-01.2, TC-01.3 | ✅ | Passing |
| REQ-02 | TC-02.1, TC-02.2 | ✅ | Passing |
| REQ-03 | TC-03.1 - TC-03.5 | TC-03.5 manual | Mixed |
| REQ-04 | *(missing)* | ❌ | **Gap** |

---

## 3. Acceptance Criteria

### Writing Good Acceptance Criteria

**Use Given-When-Then format**:
```markdown
**Given** the user is on the bookshelf page with 50 books
**When** the user types "Design" in the search bar
**Then** only books with "Design" in the title or author are displayed
**And** the result count updates to show "3 of 50 books"
**And** the filter happens in < 200ms (no visible delay)
```

### Criteria Checklist
Every acceptance criterion should be:
- [ ] **Specific**: No ambiguity (quantify where possible)
- [ ] **Testable**: Can be verified by automated test or clear manual step
- [ ] **Independent**: Doesn't depend on external state that's hard to reproduce
- [ ] **Complete**: Covers happy path, error path, and edge cases

### Common Missing Criteria
- ❌ No empty state: "What happens when there are zero results?"
- ❌ No loading state: "What does the user see while data loads?"
- ❌ No error state: "What happens when the API fails?"
- ❌ No boundary: "What happens with 10,000 items?"
- ❌ No accessibility: "Can a screen reader user complete this flow?"

---

## 4. Edge Case Discovery

### Systematic Edge Case Categories

**Data edges**:
- Empty/null/undefined values
- Maximum length strings (title with 500 characters)
- Special characters (emojis, HTML entities, Unicode, RTL text)
- Minimum and maximum numeric values (0, -1, MAX_INT)
- Dates: leap years, timezone boundaries, epoch, far future

**State edges**:
- First-time user (no data, no preferences)
- Power user (1000+ items, complex filters)
- Interrupted actions (close app mid-save, network loss mid-upload)
- Concurrent modifications (two tabs editing same item)
- Session expiry during interaction

**Network edges**:
- Slow connection (3G simulation)
- Timeout (server takes > 30s)
- Partial response (connection drops mid-download)
- Offline → Online transition
- Duplicate requests (user double-clicks submit)

**Device edges**:
- Smallest supported screen (320px)
- Largest screen (4K)
- Low memory device
- Accessibility: zoom 200%, high contrast, screen reader
- Different browsers/OS versions

### The "Evil User" Exercise
Think: "If I were trying to break this, what would I do?"
- Submit the form 100 times in 1 second
- Paste a 10MB string into the search bar
- Navigate using only keyboard
- Open 3 tabs and edit the same item simultaneously
- Set device clock to year 2050

---

## 5. Regression Testing

### When to Run Regressions

| Trigger | Scope | Speed Target |
|---------|-------|-------------|
| Every commit (CI) | Unit + Component | < 5 minutes |
| Every PR | Unit + Component + Integration | < 15 minutes |
| Before release | Full suite including E2E | < 30 minutes |
| After hotfix | Targeted regression + smoke test | < 10 minutes |

### Regression Risk Levels

| Change Type | Risk | Regression Scope |
|-------------|------|-----------------|
| Bug fix in isolated function | 🟢 Low | Unit tests of that function + direct callers |
| New feature (additive) | 🟡 Medium | New tests + existing feature tests nearby |
| Refactor (behavior preserved) | 🟠 High | Full test suite for affected module |
| Dependency upgrade | 🔴 Critical | Full test suite + E2E |
| Data model change | 🔴 Critical | Full suite + migration tests + API contract tests |

### Smoke Test Suite
A minimal set of tests that verify "the app is not completely broken":
```
[ ] App starts without crash
[ ] Home page renders
[ ] User can log in
[ ] Core feature (e.g., book list) loads
[ ] API responds (at least one endpoint)
[ ] Navigation works (can reach 3+ screens)
```

---

## 6. Performance Testing

### What to Measure

| Metric | How | Target |
|--------|-----|--------|
| **Response time** | API endpoint benchmarks | p50 < 200ms, p99 < 1s |
| **Throughput** | Requests per second under load | Depends on expected traffic |
| **Page load** | Lighthouse, WebPageTest | LCP < 2.5s, INP < 200ms |
| **Memory** | Profiler, DevTools | No leaks over time, stable baseline |
| **Bundle size** | Bundler analyzer | < 200KB initial JS (web) |

### Load Testing Levels

| Level | Users | Purpose |
|-------|-------|---------|
| **Baseline** | 1 | Establish response times without load |
| **Normal load** | Expected daily active | Verify performance under typical conditions |
| **Peak load** | 2-3x normal | Verify behavior at anticipated peaks |
| **Stress test** | Until failure | Find breaking point, verify graceful degradation |

### Tools
- **API**: k6, Artillery, Apache Bench
- **Frontend**: Lighthouse CI, WebPageTest, Playwright with performance APIs
- **Profiling**: Chrome DevTools, React Profiler, Xcode Instruments

---

## 7. Bug Reports

### Template

```markdown
## Bug: [Short descriptive title]

**Severity**: Critical / High / Medium / Low
**Environment**: [OS, Browser/Device, App version]
**Reproducibility**: Always / Sometimes / Rare

### Steps to Reproduce
1. [Exact step 1]
2. [Exact step 2]
3. [Exact step 3]

### Expected Result
[What should happen]

### Actual Result
[What actually happens]

### Evidence
- Screenshot/Video: [link]
- Console errors: [paste]
- Network tab: [relevant request/response]

### Impact
[Who is affected? How many users? Is there a workaround?]

### Possible Cause (if known)
[Technical hypothesis]
```

### Severity Guide

| Severity | Definition | SLA |
|----------|-----------|-----|
| **Critical** | App crash, data loss, security breach, complete feature failure | Fix immediately |
| **High** | Major feature broken, no workaround, affects many users | Fix within 24h |
| **Medium** | Feature partially broken, workaround exists | Fix in current sprint |
| **Low** | Cosmetic, minor inconvenience, edge case | Backlog |

---

## 8. Definition of Done

### Feature-Level Done

A feature is "done" when ALL of these are true:

```
Code:
[ ] Implementation matches all acceptance criteria from spec.md
[ ] Code reviewed (by human or AI peer review)
[ ] No console errors or warnings
[ ] No TypeScript/lint errors

Tests:
[ ] Unit tests for business logic (≥ 80% coverage for new code)
[ ] Component tests for UI states (happy + error + empty + loading)
[ ] Integration test for the main flow
[ ] E2E test if it's a critical path
[ ] All existing tests still pass (no regressions)

Quality:
[ ] Accessible (keyboard navigation, screen reader, contrast)
[ ] Responsive (tested on mobile + tablet + desktop)
[ ] Performance within budget (no new Lighthouse regressions)
[ ] Error states handled gracefully

Documentation:
[ ] spec.md updated if requirements evolved during implementation
[ ] constitution.md updated if new patterns were introduced
[ ] design-system.md updated if new components were created
[ ] SESSION_HISTORY.md entry written

Deployment:
[ ] Build passes in CI
[ ] Feature flag configured (if applicable)
[ ] Monitoring/alerting set up for new endpoints
```

### Sprint-Level Done
```
[ ] All committed features meet Feature-Level Done
[ ] Regression suite passes
[ ] Performance baseline maintained or improved
[ ] Tech debt tracked (new issues created for any shortcuts taken)
[ ] SESSION_HISTORY.md reflects all work done
```

---

---

## Scope & Boundaries

This skill owns test **strategy, planning, and quality governance**. Other skills own test **implementation**:

```
"What should we test?"           → QA Engineer (this skill)
"How do I write this test?"      → Frontend Developer or Backend Developer
"Is the architecture healthy?"   → Code Quality & Architecture Assessment
"Does the UI meet standards?"    → UX/UI Designer (accessibility, usability)
```

### Decision Tree

```
Need to plan a test strategy?
  └─ YES → QA Engineer
Need to write acceptance criteria from spec.md?
  └─ YES → QA Engineer
Need to write actual test code (unit/integration/E2E)?
  └─ Frontend test? → Frontend Developer
  └─ Backend test? → Backend Developer
Need to assess code architecture quality?
  └─ YES → Code Quality & Architecture Assessment
Need to validate UI accessibility or usability?
  └─ YES → UX/UI Designer
```

---

## When to Apply This Skill

- During **Specify** phase: Write acceptance criteria, identify edge cases early
- During **Plan** phase: Define test strategy, map requirements to test types
- During **Tasks** phase: Include test tasks in tasks.md (not as afterthought)
- During **Implementation**: Write tests alongside code (TDD or test-with)
- During **Review**: Validate traceability, run full regression, check definition of done
- **Continuously**: Monitor test health, update flaky tests, expand coverage gaps
