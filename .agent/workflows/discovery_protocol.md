---
description: Discovery Protocol — Product discovery and backlog definition using product-designer and ba-scrum-master skills.
---

# Discovery Protocol

**Purpose**: To ensure we are building the *right* thing before we figure out *how* to build it or *how it looks*. It shifts from "ticket-taking" to empowered product discovery.

## 1. When to Trigger
- At the start of a completely new initiative or Epic.
- When the user proposes a vague idea or "cool feature".
- When product direction lacks clarity or value proposition.
- When reorganizing the high-level roadmap (`ROADMAP.md`).

## 2. Participating Skills
- **`product-designer`**: Challenges assumptions, focuses on user value, viability, and usability constraints (Marty Cagan's methodology).
- **`ba-scrum-master`**: Translates the validated idea into actionable, INVEST-compliant user stories in the backlog.

## 3. Workflow Steps

### Phase 1: Empathize & Ideate (`product-designer`)
1. **Understand the User**: Who is this for? What is the core problem being solved? (Consult `VISION.md` and `CHARTER.md`).
2. **Challenge Assumptions**: Ask "Why?" to the user. Is this the most valuable thing to build right now? 
3. **Define Success**: What does success look like? What metrics or qualitative changes are expected?

### Phase 2: Refine & Document (`ba-scrum-master`)
1. **Translate to Epics/Stories**: Take the validated product direction and break it down into Epics and Stories.
2. **Apply INVEST**: Ensure stories are Independent, Negotiable, Valuable, Estimable, Small, and Testable.
3. **Update Records**: Add or update stories in `docs/specs/story.md`. Set status to `Not Started` or `Backlog`.
4. **Milestone Mapping**: Add the new scope to the appropriate milestone in `ROADMAP.md`.

## 4. Exit Criteria
- Feature/Idea is validated for value and viability.
- `docs/specs/story.md` is updated with clear, BDD-formatted Acceptance Criteria.
- Scope is placed accurately within the project Roadmap.
- The flow proceeds to `.agent/workflows/design_protocol.md`.
