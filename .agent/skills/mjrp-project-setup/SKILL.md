---
name: mjrp-project-setup
description: >
  Initialize and bootstrap new software projects using the MJRP Vibe Coding
  Framework. Use this skill whenever the user wants to: start a new project,
  set up a project from scratch (Greenfield), organize an existing project
  (Brownfield), create the SpecKit folder structure, bootstrap AI agent
  configurations, or apply the MJRP framework to a codebase. Trigger on phrases
  like "new project", "start a project", "initialize project", "project setup",
  "bootstrap project", "set up framework", "criar projeto", "novo projeto",
  "inicializar projeto", "setup do projeto", "aplicar framework", or any request
  involving creating project scaffolding with docs/specs, VISION.md, CHARTER.md,
  constitution.md, or multi-AI orchestration setup. Also trigger when the user
  mentions "Greenfield", "Brownfield", or "SpecKit setup" in the context of
  starting work on a project.
---

# Skill: MJRP Project Setup

**Purpose**: Guide the initialization of a new software project (or the organization of an existing one) following the MJRP Vibe Coding Framework — creating the full folder structure, SpecKit artifacts, AI tool configurations, and governance setup.

**Framework source**: The MJRP Proj Setup Framework lives at the user's local path. Ask the user for the framework path if not provided. The default location is `/Users/mpedroso/0.MyPetProjects/MJRPprojSetupFramework`.

---

## Step 0: Determine the Mode

Before anything else, figure out which scenario applies:

**Greenfield** — The project doesn't exist yet. You're starting from zero.
- Flow: Vision → Directory & Git → Folder Structure → Baseline Docs → SpecKit → Design System → AI Config → **Discovery → Design → SDD Dev Loop**

**Brownfield** — The project already has code, data, or history.
- Flow: Audit & Inventory → Gap Analysis → Extract/Create Artifacts → Retrofit SpecKit → AI Config → **Discovery → Design → SDD Dev Loop**
- Guiding principle: "Add without breaking." Reflect reality before idealizing.

Ask the user which mode applies. If they describe an existing project with code, default to Brownfield. If they say "new idea" or "starting fresh," default to Greenfield.

---

## Greenfield Flow

### Step 1: Vision & Charter

Collaborate with the user to define the project's identity. Create two files in the project root:

**VISION.md** — The soul of the project:
```markdown
# [Project Name]

## Core Objective
[One sentence that defines success]

## The Vibe
[Aesthetic direction — e.g., "Organic Blueprint — cream, forest green, serif typography"]

## User Empathy
[What pain are we relieving?]

## Design DNA
[Visual reference — screenshot, Stitch link, or description]
```

**CHARTER.md** — The boundaries:
```markdown
# [Project Name] — Charter

## Title and Description
[Name and high-level overview]

## Justification (Business Case)
[The problem or opportunity]

## Main Goals and Success Metrics
[Measurable outcomes]

## High-Level Scope
[What's in / what's out]

## Main Stakeholders
[Sponsor, PM, interested parties]

## Roadmap (Milestones)
[Key dates and deliverables]

## Risks and Constraints
[Potential problems and limitations]

## AI Tooling
[Which AI tools and their roles — see AI Orchestration section]
```

### Step 2: Directory & Git

Create the project directory and initialize version control:

```bash
mkdir -p [project-name]
cd [project-name]
git init
```

Set up the branching model:
- **main**: Stable, deploy-ready code
- **dev**: Integration of new features
- **feat/[name]-[timestamp]**: Short-lived feature branches

Create a `.gitignore` appropriate for the tech stack.

First commit: `chore: project scaffold`

### Step 3: Folder Structure

Apply the standard structure that makes the project readable by AI agents:

```
/project-name
├── .github/              # CI/CD workflows (GitHub Actions)
├── .claudeprompt         # Persistent system prompt for Claude Code
├── .gemini/              # Antigravity config (GEMINI.md)
├── docs/
│   ├── specs/            # SpecKit — the project's brain
│   │   ├── constitution.md
│   │   ├── story.md
│   │   ├── arch.md
│   │   ├── data-model.md
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   └── design-system.md
│   ├── architecture/     # Diagrams and ADRs
│   └── sessions/
│       └── SESSION_HISTORY.md
├── src/                  # Source code
├── tests/                # Tests
├── VISION.md
├── CHARTER.md
├── README.md
└── .gitignore
```

Create all directories:
```bash
mkdir -p docs/specs docs/sessions docs/architecture src tests
```

### Step 4: Baseline Docs

Create `README.md` with a project overview that references the VISION and CHARTER.

### Step 5: SpecKit Setup

Create the SpecKit artifacts in `docs/specs/`. Start with `constitution.md` — the most important file. Every AI agent reads this before every decision.

**constitution.md template**:
```markdown
# Project Constitution

## 1. Technical Stack
- Frontend: [e.g., Next.js 15 + TypeScript]
- Styling: [e.g., Tailwind CSS — Vibe: Organic Blueprint]
- Backend: [e.g., Firebase / Supabase]

## 2. Development Methodology (SDD)
- Flow: Specify -> Plan -> Tasks -> Implement
- No implementation without a defined Task in tasks.md
- Iteration via [Scrum sprints / Kanban features]

## 3. SCM & Governance
- Branching: main (stable), dev (integration)
- Commits: Conventional Commits (feat, fix, docs, refactor, vibe, chore)
- Review: Every implementation validated against story.md

## 4. AI Orchestration
- [Rules per tool — see AI Orchestration section]
- Always check this file before suggesting packages/patterns

## 5. Design System Reference
- Consult design-system.md for visual decisions
- Never deviate from the defined palette/typography
```

Create placeholder files for the remaining SpecKit artifacts (story.md, spec.md, arch.md, data-model.md, plan.md, tasks.md). Each starts with a header and a note that it will be populated during the Specify stage.

### Step 6: Design System (if applicable)

If the project has a visual interface, create `docs/specs/design-system.md` with tokens for colors, typography, spacing, and key components. Collaborate with the user on the "Vibe" — the aesthetic identity.

### Step 7: AI Tool Configuration

Configure each AI tool the user plans to use:

**Claude Code (.claudeprompt)**:
```
You are a developer working on [Project Name].

Before any implementation, read:
- VISION.md (purpose)
- CHARTER.md (scope and limits)
- docs/specs/constitution.md (technical rules)
- docs/specs/design-system.md (visual standards)
- docs/specs/tasks.md (current backlog)

Rules:
- Follow Conventional Commits
- Never implement without a task in tasks.md
- Consult constitution.md before suggesting dependencies
```

**Antigravity (GEMINI.md)** — same structure adapted for Antigravity's format.

**Skills & Workflows**: Copy from the framework repository into the project. The framework includes 12 skills, 14 workflows, and 10 templates. See `references/setup-guide.md` for exact copy commands.

### Step 8: First Commit Sequence

Follow the checklist:

| # | Phase | Action | Commit |
|---|-------|--------|--------|
| 1 | Setup | Create VISION.md and CHARTER.md | `docs: initial vision and charter` |
| 2 | Setup | git init + .gitignore + first commit | `chore: project scaffold` |
| 3 | Setup | Create full folder structure | `chore: folder structure` |
| 4 | Setup | Create constitution.md | `docs: project constitution` |
| 5 | Setup | Configure .claudeprompt and GEMINI.md | `chore: AI config` |
| 6 | Discovery | Run discovery_protocol.md | `docs: discovery [feature]` |
| 7 | Design | Run design_protocol.md + architecture_review | `docs: design [feature]` |
| 8 | Design | Create design-system.md (if applicable) | `docs: design system` |
| 9 | SDD | Complete Specify for first feature | `docs: specify [feature]` |
| 10 | SDD | Complete Plan | `docs: plan [feature]` |
| 11 | SDD | Generate Tasks | `docs: tasks [feature]` |
| 12 | SDD | Start Implement | `feat: [feature]` |

---

## Brownfield Flow

### Step 0: Audit & Bootstrap

Before anything else, map what already exists:

**0.1 Artifact Inventory** — Check for:
- Code: languages, frameworks, folder structure
- Data: schemas, models, existing content
- Git: branches, commits, history
- Documentation: specs, docs, READMEs
- AI tools: configs, histories, prompts
- Design: prototypes, wireframes, existing UI
- Previous sessions: AI session context

**0.2 Gap Analysis** — For each framework artifact (VISION.md, CHARTER.md, constitution.md, story.md, spec.md, arch.md, data-model.md, design-system.md, tasks.md, SESSION_HISTORY.md, .claudeprompt), determine: Does it exist? Is it partial? What action is needed (Create / Extract / Adapt)?

**0.3 Bootstrap Decision** — For each missing artifact:
- **Extract** when equivalent content exists in another format (spec in Google Docs, stack defined in package.json)
- **Create** when no equivalent material exists
- **Adapt** when the artifact exists but is incomplete or differently formatted

### Brownfield Steps 1-8

1. **Execute Audit & Bootstrap** → Document in BOOTSTRAP_REPORT.md
2. **Extract/Create Vision** → Generate VISION.md and CHARTER.md from existing material
3. **Portray Current State** → Create constitution.md reflecting the ACTUAL stack and patterns (not idealized)
4. **Adapt Folder Structure** → Only reorganize where needed to add `docs/specs/`. Don't move working code.
5. **Retrofit SpecKit** → Document existing features in story.md and spec.md
6. **Consolidate Design System** → If UI exists, extract visual tokens into design-system.md
7. **Activate Multi-AI Environment** → Configure tools with newly created artifacts
8. **Migrate Context** → Consolidate previous sessions into SESSION_HISTORY.md

Guiding principles:
- constitution.md must reflect REALITY, not the IDEAL
- Don't reorganize everything at once — prioritize constitution.md and VISION.md
- Use a single commit for the bootstrap: `docs: bootstrap MJRP Framework v1.2`
- Create a tag: `git tag -a v0-framework-bootstrap -m "Start of MJRP Framework"`

---

## Full Development Lifecycle (Both Modes)

After the project setup is complete, the development lifecycle has three phases that flow sequentially. Discovery and Design happen before SDD coding begins — this ensures you build the right thing before building it right.

### Phase 1: Discovery (`discovery_protocol.md`)

Purpose: Understand the problem space, users, and opportunities before jumping into solutions.

Activities include: user research, competitive analysis, problem framing, opportunity mapping, stakeholder interviews, and defining success metrics. The output is a validated understanding of what's worth building.

This phase feeds into VISION.md and CHARTER.md refinement, and directly informs the Design phase.

### Phase 2: Design (`design_protocol.md` + `architecture_review_protocol.md`)

Purpose: Design the solution — both the user experience and the technical architecture — before committing to implementation.

Activities include: user flows, wireframing, prototyping (Stitch/Figma), design system creation, architecture decisions (ADRs), and technical feasibility assessment. The `architecture_review_protocol.md` ensures architectural decisions are reviewed and documented.

Outputs feed into design-system.md, arch.md, and inform the Specify stage.

### Phase 3: SDD — Spec-Driven Development

The iterative build cycle with 4 stages:

1. **SPECIFY** (What & Why) → story.md + spec.md
2. **PLAN** (How) → arch.md + data-model.md + plan.md
3. **TASKS** (Decompose) → tasks.md
4. **IMPLEMENT** (Execute) → code in src/, tests in tests/

**Approval Gates**: Each transition requires explicit human approval. The agent cannot advance without validation. No stage can be skipped or combined.

**Flow Interruption**: If requirements change during any stage that impact a previous stage, the flow must go back to the appropriate stage. If scope changes fundamentally, you may need to loop back to Discovery or Design.

---

## Commit Convention (Conventional Commits)

- **feat**: New functionality
- **fix**: Bug fix
- **docs**: Documentation/specs changes
- **refactor**: Code change without behavior change
- **vibe**: UI/UX adjustments based on aesthetic feedback
- **chore**: Maintenance tasks (deps, configs)

Each SpecKit stage transition generates a docs commit:
- Specify done → `docs: complete specify stage for [feature]`
- Plan done → `docs: complete plan stage for [feature]`
- Tasks generated → `docs: generate tasks for [feature]`
- Implement done → `feat: implement [feature]`

---

## Multi-AI Orchestration

Each tool has a defined role. Context flows between them through SpecKit artifacts (in Git) and SESSION_HISTORY.md:

| Tool | Role | When to Use |
|------|------|-------------|
| Claude Cowork | Brainstorming, analysis, planning | Pairing sessions, spec creation, data analysis |
| Claude Code | Terminal coding | Implementation, refactoring, tests, git ops |
| Antigravity | Builder: Coding + Git | Implementation, code review, Git ops |
| Stitch | AI Design | Prototyping, UI/UX, visual design system |

Git is the central hub. All tools read and write to the same repository.

---

## Context Handoff

At the end of each work session, update `docs/sessions/SESSION_HISTORY.md`:

```markdown
# [Project] — Session History

> Date: [date]
> Participants: [human] + [AI tool]
> Branch: [active branch]

## Executive Summary
[2-3 sentences of what was done]

## Decisions Made
[List of decisions with context]

## Artifacts Generated/Modified
[Table: file | description | version]

## Pending for Next Session
[Priority-ordered list]

## Key Data for Reference
[Metrics, counts, important values]
```
