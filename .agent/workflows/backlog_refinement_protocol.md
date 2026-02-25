---
description: Backlog Refinement Protocol — Structured session to assess, prioritize, and rewrite backlog items using the ba-scrum-master skill. Run before sprint planning, milestone kickoff, or when stories are not ready for execution.
---

# Backlog Refinement Protocol

**Purpose**: Ensure the product backlog is clean, prioritized, and actionable before work begins. Uses the `ba-scrum-master` skill to assess story quality (INVEST), reframe solution-shaped items as user needs, split oversized stories, and update the relevant SpecKit artifacts.

## 1. When to Trigger

Run this protocol when:
- **Milestone kickoff**: Before SDD Specify phase for a new milestone — confirm stories are ready to be specced.
- **Sprint planning prep**: Top backlog items must be "ready" before a sprint starts.
- **Story not passing gate**: A story in `story.md` lacks acceptance criteria, is too large (13+ points), or is solution-shaped.
- **Backlog drift**: `story.md` or `product_backlog.md` hasn't been reviewed in 2+ milestones.
- **New requirements arrived**: Stakeholder input, user feedback, or post-milestone learnings need to be triaged into the backlog.
- **Before onboarding a new agent**: Builder agents need clean, ready stories to execute against.

## 2. Context to Load

Before starting the session, load in this order:

1. `docs/specs/story.md` — Epic map and all user stories with current status
2. `docs/specs/product_backlog.md` — Prioritized backlog (if separate from story.md)
3. `docs/ROADMAP.md` — Milestone sequencing and exit criteria (for priority context)
4. Active milestone `docs/specs/milestones/<active>/spec.md` — What's in scope right now
5. `CHARTER.md` — MVP scope and boundaries (to catch out-of-scope items)
6. `docs/specs/constitution.md` — Technical constraints that affect feasibility

## 3. Refinement Session Flow

### Phase 1 — Assess (Read before touching anything)

For each story in scope:
- Is it framed as a user need or a solution/task?
- Does it have acceptance criteria (Given/When/Then)?
- Does it pass **INVEST**? (Independent, Negotiable, Valuable, Estimable, Small, Testable)
- Is the estimate ≤ 8 points? If 13+, it must be split.
- Are dependencies mapped and resolved?

Produce a triage table before making any changes:

```
| Story | Issue | Action |
|-------|-------|--------|
| E1-S2 | No AC, too large | Split + rewrite |
| E3-S1 | Solution-shaped | Reframe as user need |
```

### Phase 2 — Diagnose and Reframe

Apply the `ba-scrum-master` skill's anti-pattern detector:
- **Task disguised as story** → reframe or move to tech debt track
- **Solution baked in** → ask "What decision is the user making?" and rewrite
- **Missing "so that"** → surface the business value
- **Epic posing as story** → decompose using story splitting techniques

Show original vs. rewritten version side by side for each changed story. Explain which INVEST criterion drove the change.

### Phase 3 — Prioritize

Apply value-based triage from the `ba-scrum-master` skill:

| Priority | Criteria |
|----------|----------|
| P0 — Critical | Blocks users, revenue, or current milestone exit criteria |
| P1 — High | Core user journey, retention, key integrations |
| P2 — Medium | Business enablers, secondary flows |
| P3 — Low | Nice-to-have, cosmetic, tech debt without measurable impact |

Reorder the backlog by value, not by who requested the item or when it was added. Recommend deferral or archival for P3 items older than 2 milestones.

### Phase 4 — Update Artifacts

After the session, update:

| Artifact | What to update |
|----------|---------------|
| `docs/specs/story.md` | Rewritten stories, updated AC, new status |
| `docs/specs/product_backlog.md` | Priority order, P-labels, deferred/archived items |
| Active milestone `tasks.md` | Add any new tasks for stories entering the next sprint |
| `docs/ROADMAP.md` | Update milestone stories table if scope changed |

**Commit**: `docs: backlog refinement — [milestone or sprint] [date]`

## 4. Definition of "Ready"

A story is ready for SDD Specify when:
- [ ] Framed as a user need (not a solution or task)
- [ ] Has at least 2 Given/When/Then acceptance criteria
- [ ] Passes all 6 INVEST criteria
- [ ] Estimated ≤ 8 story points (or explicitly split if larger)
- [ ] Dependencies identified and resolved or explicitly accepted
- [ ] Fits within CHARTER MVP scope or has explicit approval to extend

If a story fails any criterion, it is **Not Ready** and must not enter the SDD Specify phase.

## 5. Charter Check

During Phase 3 (Prioritize), if any of the following are detected, flag for CHARTER update before proceeding:

- A story being added is **outside current CHARTER MVP scope**
- A story being deferred reveals that a **CHARTER goal is no longer being pursued**
- **Stakeholder input** introduced new requirements that change the project's direction

**Action**: Surface the drift to the human. If confirmed, update `CHARTER.md` (human approval required), then cascade:
1. `docs/ROADMAP.md` — realign milestone targets
2. `docs/specs/story.md` — mark out-of-scope stories as `🚫 Deferred`

Do not silently absorb scope changes into the backlog without surfacing them to the CHARTER level.

---

## 6. Related

- **Story structure and INVEST**: `ba-scrum-master` skill
- **SDD Specify phase**: `sdd_specify_protocol.md` (run after stories are Ready)
- **Full SDD flow**: `sdd_protocol.md`
- **Doc sync after refinement**: `documentation_protocol.md`
