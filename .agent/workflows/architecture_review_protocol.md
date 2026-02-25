---
description: Architecture Review Protocol — Full system review using system-architect skill before major milestones, after significant implementation, or when architectural drift is suspected.
---

# Architecture Review Protocol

**Purpose**: Trigger a structured architecture review using the `system-architect` skill to catch layer violations, dependency drift, and technical debt before they compound. Distinct from the ADR protocol (which records a decision already made) — this protocol runs *before* decisions, to surface issues and inform them.

## 1. When to Trigger

Run this protocol when:
- **Milestone gate**: Before starting a new milestone (e.g., M2 → M3 transition).
- **Significant implementation landed**: After a Builder agent completes a milestone or major feature.
- **Architectural drift suspected**: Code deviates from `constitution.md` patterns (new layers, unexpected dependencies, growing files).
- **New agent onboarding**: When a new Builder joins and must be trusted to respect existing architecture.
- **Tech stack change proposed**: Any new dependency or framework being considered.
- **Audit file exists**: When `docs/temp/architecture_audit.md` or similar is present and unreviewed.

Do **not** run this protocol for every feature. Reserve it for milestone-level moments.

## 2. Context to Load

Before starting the review, load in this order:

1. `VISION.md` — system purpose (does architecture serve it?)
2. `CHARTER.md` — scope and constraints
3. `docs/specs/constitution.md` — technical rules and layer boundaries
4. `docs/specs/arch.md` — documented layer map and ADRs
5. `docs/specs/data-model.md` — entity contracts
6. `src/` folder structure — actual code (use `find src/ -type f | sort`)
7. Any `docs/temp/architecture_audit.md` if present

## 3. Review Workflow (7 Steps)

Follow the `system-architect` skill's review sequence:

**Step 1 — Understand the Purpose**
Read VISION + CHARTER. Ask: *"Does the current architecture scream this project's domain?"*

**Step 2 — Map the Layers**
Identify what lives in each Clean Architecture layer. Compare against `arch.md`. Flag anything in the wrong ring.

**Step 3 — Check the Dependency Rule**
Trace dependencies between components. Any inner layer importing outer-layer code is a violation. List each one with severity.

**Step 4 — Evaluate Technology Choices**
For each major tech: is it isolated behind an interface, or has it leaked into business logic?

**Step 5 — Apply SOLID**
For each major module boundary: SRP, OCP, ISP, DIP. Note which principles are under pressure.

**Step 6 — Identify Pattern Opportunities**
Look for recurring conditionals, complex subsystems, third-party coupling — suggest GoF patterns where applicable.

**Step 7 — Flag Technical Debt**
Classify debt items: Fix Now / Fix Before MVP / Monitor. Apply Broken Windows lens — which debt lowers the bar if left unchecked?

## 4. Output: Architecture Audit Report

Save to `docs/temp/architecture_audit.md`:

```markdown
# Architecture Audit — [Date]

## Verdict
[One sentence: sound / minor concerns / significant risks]

## Layer Analysis
[Map components to layers; flag violations]

## Dependency Direction
[Violations table: component → wrongly depends on → severity]

## SOLID Assessment
[Principles upheld / under pressure]

## Technology Isolation
[Each major tech: properly isolated? leaked?]

## Pattern Opportunities
[Recommended patterns with rationale]

## Technical Debt Register
| Item | Severity | Priority | Action |
|------|----------|----------|--------|
| ... | Fix Now / Before MVP / Monitor | ... | ... |

## Recommendations
[Fix Now / Monitor / Defer — with rationale]
```

## 5. After the Review

Based on findings, trigger the appropriate follow-on protocol:

| Finding | Action |
|---------|--------|
| Layer violation or SOLID breach | Fix inline, update `constitution.md` and `arch.md` |
| New architectural decision needed | → `architecture_decision_protocol.md` (ADR) |
| Docs out of sync with code | → `documentation_audit_protocol.md` |
| Debt items flagged Fix Now | Add tasks to active milestone `tasks.md` |

**Commit**: `docs: architecture audit — [scope] [date]`

## 6. Related

- **ADR (post-decision record)**: `architecture_decision_protocol.md`
- **Doc-code sync**: `documentation_audit_protocol.md`
- **Code quality scan**: `code_quality_assessment_protocol.md`
- **SDD integration**: Run before `sdd_specify_protocol.md` when starting a new milestone
