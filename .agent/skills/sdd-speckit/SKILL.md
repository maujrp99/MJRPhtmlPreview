---
name: SDD SpecKit Mastery
description: >
  Use when writing, reviewing, or improving any SpecKit artifact: spec.md,
  plan.md, tasks.md, constitution.md, arch.md, story.md, or data-model.md.
  Covers quality criteria, anti-patterns, templates, cross-artifact consistency,
  and the SpecKit lifecycle for Spec-Driven Development (SDD).
---

# Skill: SDD SpecKit Mastery

**Purpose**: Teach an AI agent how to produce high-quality SpecKit artifacts (spec.md, plan.md, tasks.md, constitution.md) following the MJRP Vibe Coding Framework.

**Related Workflows**: `sdd_protocol.md`, `sdd_specify_protocol.md`, `sdd_plan_protocol.md`, `sdd_task_protocol.md`, `architecture_decision_protocol.md`
**Related Templates**: `adr_template.md`

---

## Core Concept

SpecKit is the brain of the project — the set of documents in `docs/specs/` that AI agents consult before any action. The quality of SpecKit artifacts directly determines the quality of AI-generated code.

---

## Artifact Mastery

### 1. constitution.md — The Laws of Robotics

The most important file. Every agent reads this before every decision.

**Quality Criteria**:
- Lists the ACTUAL stack (not the ideal one)
- Specifies patterns to follow AND patterns to avoid
- Includes version numbers for key dependencies
- Has a "Legacy Notes" section (Brownfield) for known debt
- Is concise — agents have limited context windows

**Anti-patterns**:
- ❌ Vague: "Use modern best practices"
- ❌ Aspirational: "We plan to migrate to TypeScript" (unless flagged as future)
- ❌ Too long: 2000+ words makes agents lose focus
- ✅ Specific: "Frontend: Next.js 15 + TypeScript. Styling: Tailwind CSS. No CSS modules."
- ✅ Actionable: "All API calls go through src/lib/api.ts — never call fetch directly"

---

### 2. spec.md — The What and Why

Defines requirements without prescribing implementation.

**Quality Criteria**:
- Every requirement has an ID (REQ-01, REQ-02)
- User stories follow "As a [user], I want [action], so that [benefit]"
- Success criteria are measurable and testable
- "Out of Scope" section prevents scope creep
- "Open Questions" are resolved BEFORE moving to Plan

**Writing Tips**:
- Start with the problem, not the solution
- Use concrete examples: "User sees a grid of 12 book covers" not "User sees books"
- Quantify when possible: "Page loads in < 2s", "Supports 500+ items"
- Include edge cases: "What happens when library is empty?"

**Anti-patterns**:
- ❌ Implementation leaking: "Create a React component that..."
- ❌ Vague criteria: "The page should look good"
- ❌ Missing scope: No "Out of Scope" section leads to infinite features
- ✅ Clean: "REQ-03: Book cards display cover, title, author, and garden status emoji"

---

### 3. plan.md — The How

Translates spec into technical architecture.

**Quality Criteria**:
- References specific requirements from spec.md (REQ-01, REQ-02)
- Includes data flow description (even if simple text, no diagram tool needed)
- For UI features: includes mockups (ASCII art, Stitch reference, or textual description)
- Lists components/modules with clear responsibilities
- Documents which existing files are affected
- Lists new dependencies with justification (must align with constitution.md)
- "Documents Consulted" section shows the agent did its homework

**Writing Tips**:
- Start with the data flow — how does information move through the system?
- Be explicit about file paths: "Create src/components/BookCard.tsx" not "Create a book card component"
- For each component, state: what it receives, what it renders, what it emits
- Include ASCII mockups for UI — they're surprisingly effective for AI agents:

```
┌─────────────────────────────────┐
│  [Logo]  Home | Books | About   │
├─────────────────────────────────┤
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐      │
│  │ 📖│ │ 📖│ │ 📖│ │ 📖│      │
│  │   │ │   │ │   │ │   │      │
│  └───┘ └───┘ └───┘ └───┘      │
│  Title  Title  Title  Title     │
│  Author Author Author Author    │
│  🌳     🌱     🌿     🌲       │
├─────────────────────────────────┤
│  [Filters: Category | Status]   │
└─────────────────────────────────┘
```

**Anti-patterns**:
- ❌ No traceability: Plan doesn't reference spec requirements
- ❌ Vague architecture: "We'll use components" (which ones? where?)
- ❌ Missing UI: "The page will display books" (how? grid? list? cards?)

---

### 4. tasks.md — The When

Decomposes the plan into atomic, verifiable work units.

**Quality Criteria**:
- Each task is completable in one focused session (< 1 hour of agent work)
- Each task has a clear "done" signal (file created, test passes, UI renders)
- Tasks are ordered by dependency
- Includes verification tasks (test, build, manual check)
- Includes documentation tasks (update specs, session history)

**Task Sizing Guide**:
- ✅ "Create BookCard component with props: title, author, coverUrl, gardenStatus" — atomic, clear
- ❌ "Implement the bookshelf page" — too large, not atomic
- ✅ "Add filter dropdown for category_mjrp with values from schema" — atomic, specific
- ❌ "Add filters" — too vague

**Ordering Pattern**:
1. Data layer first (models, schemas, API)
2. Core logic second (services, stores)
3. UI components third (building blocks)
4. Page composition fourth (assembling components)
5. Polish fifth (animations, edge cases)
6. Verification last (tests, build, regression)

---

## Cross-Artifact Consistency Rules

1. **Traceability Chain**: spec.md requirements → plan.md components → tasks.md items. Every task should trace back to a requirement.
2. **Vocabulary Consistency**: If spec says "garden_status", plan and tasks must use "garden_status" — not "growth stage" or "plant status".
3. **Constitution Alignment**: Plan must not propose dependencies or patterns that contradict constitution.md. If it needs to, create an ADR first (see `architecture_decision_protocol.md` and `3.MJRP-Templates/adr_template.md`).
4. **Gate Enforcement**: Never generate Plan content while writing Spec. Never generate Tasks while writing Plan. One stage at a time.

---

## SpecKit Lifecycle

```
[New Feature Request]
       │
       ▼
   SPECIFY ──→ spec.md (WHAT/WHY)
       │         commit: docs: complete specify stage for <feature>
       ▼
     PLAN ──→ plan.md (HOW)
       │         commit: docs: complete plan stage for <feature>
       ▼
    TASKS ──→ tasks.md (WHEN)
       │         commit: docs: generate tasks for <feature>
       ▼
  IMPLEMENT ──→ code (DO)
                 commit: feat: implement <description>
```

Each arrow is a **Gate** requiring human approval.

---

## Additional SpecKit Artifacts

### 5. arch.md — The Blueprint

Documents the system's high-level architecture: components, layers, data flow, and deployment model.

**Quality Criteria**:
- Describes the ACTUAL architecture (not the ideal/aspirational one)
- Lists all major components and their responsibilities
- Shows how components communicate (APIs, events, shared state)
- Includes a data flow diagram (even ASCII is fine)
- Stays in sync with constitution.md (if arch changes, constitution may need updating)

**Template**:
```markdown
# Architecture: [Project Name]

## System Overview
[1-2 paragraphs describing the system at a high level]

## Component Map
| Component | Responsibility | Technology |
|-----------|---------------|------------|
| [Name] | [What it does] | [Stack] |

## Data Flow
[Description or ASCII diagram of how data moves through the system]

## Infrastructure
- Hosting: [where it runs]
- Database: [what and where]
- CDN/Assets: [if applicable]

## Constraints
- [Performance constraint]
- [Security constraint]
- [Scale constraint]
```

---

### 6. story.md — The Narrative

Documents key user stories, algorithms, and business logic in human-readable form. The "how things work" document.

**Quality Criteria**:
- Explains business logic that ISN'T obvious from code
- Covers key algorithms with plain-language descriptions
- Includes decision rationale ("we do X because Y")
- Useful for a new developer/agent trying to understand WHY the code does what it does

**Template**:
```markdown
# Story: [Feature/System Name]

## How [Feature] Works
[Plain-language explanation of the business logic]

## Key Algorithms
### [Algorithm Name]
- **Input**: [what it receives]
- **Process**: [step by step]
- **Output**: [what it produces]
- **Why this approach**: [rationale]

## Edge Cases
- [Case 1]: [How the system handles it]
- [Case 2]: [How the system handles it]
```

---

### 7. data-model.md — The Schema

Documents the data layer: entities, relationships, schemas, and persistence strategy.

**Quality Criteria**:
- Lists ALL entities with their attributes and types
- Shows relationships (one-to-many, many-to-many)
- Specifies where data lives (DB tables, local storage, API)
- Includes migration strategy (if applicable)
- Stays in sync with arch.md

**Template**:
```markdown
# Data Model: [Project Name]

## Entities

### [Entity Name]
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | UUID | ✅ | Primary key |
| [field] | [type] | [✅/❌] | [description] |
| created_at | DateTime | ✅ | Auto-generated |
| updated_at | DateTime | ✅ | Auto-updated |

## Relationships
- [Entity A] → has many → [Entity B]
- [Entity B] → belongs to → [Entity A]

## Persistence
- Primary: [Database/storage technology]
- Cache: [If applicable]
- Sync: [If offline-first, how data syncs]

## Migration Notes
- [Any pending or recent schema changes]
```
