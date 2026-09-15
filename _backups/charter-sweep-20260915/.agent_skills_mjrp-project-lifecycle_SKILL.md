---
name: mjrp-project-lifecycle
description: >
  Master lifecycle orchestrator for the MJRP Vibe Coding Framework (v1.2 Greenfield / v1.3 Brownfield).
  Use this skill whenever the user wants to: start a new project from scratch, adopt the MJRP framework
  on an existing codebase, understand the full development flow, or orchestrate the complete lifecycle
  from project setup through discovery, architecture, design, SDD specification, implementation, and testing.
  Trigger on: "start a new project", "setup project", "bootstrap project", "novo projeto",
  "começar projeto", "adotar o framework", "por onde começo", "where do I start", "full project setup",
  "greenfield", "brownfield", "apply framework to existing project", "setup do zero", or any request
  to go through the complete development lifecycle. Also trigger when the user is starting a new sprint
  and needs a reminder of the full flow, or when they ask "qual o próximo passo?" in a project context.
---

# MJRP Project Lifecycle — Master Orchestrator

You are the **master orchestrator** of the MJRP Vibe Coding Framework. Your job is to guide the user
through the complete development lifecycle — ensuring every phase invokes the right skill, produces the
right artifacts, and has human approval before advancing to the next stage.

**Framework references** (read if you need depth on any step):
- `mjrpSetup/MJRP_Proj_Setup_Framework_v1.1_Greenfield.md` — new projects
- `mjrpSetup/MJRP_Proj_Setup_Framework_v1.2_Brownfield.md` — existing projects

---

## Artifact Derivation Chain

Every MJRP artifact derives from a parent artifact. This chain is the backbone of the framework —
understanding it prevents gaps, duplication, and drift between documents.

```
┌──────────────────┐
│   CHARTER.md     │  Project identity, principles, initial milestones (root truth)
└────────┬─────────┘
         │ derives strategic plan
         ▼
┌──────────────────┐
│   ROADMAP.md     │  Living tactical plan — phases, epics, priorities, status
└────────┬─────────┘
         │ breaks down into stories
         ▼
┌──────────────────┐
│   story.md       │  Product backlog — INVEST-ready user stories, prioritized by phase
└────────┬─────────┘
         │ informa o domínio
         ▼
┌──────────────────┐     ARQUITETURA: estrutura técnica do sistema e modelo de dados.
│   arch.md        │     Layers, components, routes, data flows, infra decisions.
│   data-model.md  │     Entidades, relacionamentos, schema de DB, seed data.
│  (FASE 1 output) │     ── produzidos ao final de Discovery, antes do Design ──
└────────┬─────────┘
         │ informa o design
         ▼
┌──────────────────┐     ESTRUTURA DO PRODUTO: sitemap, nav hierarchy, page templates,
│   info-arch.md   │     content zones, user flows por persona.
│  (FASE 2 output) │     ── produzido antes do design-system.md ──
└────────┬─────────┘
         │ informa os tokens visuais
         ▼
┌──────────────────┐
│ design-system.md │  Visual tokens (colors, typography, spacing), component specs,
│  (FASE 2 output) │  do's and don'ts. Referencia info-arch.md para page templates.
└────────┬─────────┘
         │ one story at a time enters the SDD cycle
         ▼
┌──────────────────┐     WHAT + WHY: elaborates the story entry into full requirements.
│   spec.md        │     Adds: problem statement, REQ-IDs, success criteria,
│  (SDD: Specify)  │     out-of-scope, open questions, edge cases.
└────────┬─────────┘     ── spec.md ≠ story.md duplicate: it ELABORATES the story ──
         │ derives architecture
         ▼
┌──────────────────┐     HOW: translates spec requirements into technical design.
│   plan.md        │     References REQ-IDs from spec.md. Includes data model,
│  (SDD: Plan)     │     component design, UI mockups, file structure.
└────────┬─────────┘
         │ decomposes into tasks
         ▼
┌──────────────────┐     WHEN: atomic, verifiable implementation checklist.
│   tasks.md       │     Each task traces back to plan.md which traces to spec.md.
│  (SDD: Tasks)    │     Ordered by dependency. Each task = one focused session.
└────────┬─────────┘
         │ executes
         ▼
   src/ + tests/        Code committed per task. Every commit refs its task.
```

### story.md vs spec.md — Complementary, Not Redundant

These two artifacts are often confused. They operate at different levels of abstraction:

```
story.md entry (backlog level — the WHAT we want to build):
  "As a listener, I want a balanced playlist generated automatically
   so I can discover new music without effort.
   Points: 8 | Priority: P1 | AC: playlist ready in < 2s"

                    │
                    │ feeds SDD Specify
                    ▼

spec.md (requirement level — the WHAT IN DETAIL + how we know it's done):
  User Stories:     [imports the story above, adds REQ traceability]
  Problem:          Users abandon the app when manually curating takes too long.
  REQ-01:           System generates a playlist within 2 seconds of request.
  REQ-02:           Playlist must include ≥ 30% tracks not in user's recent history.
  REQ-03:           User triggers generation with a single tap from the home screen.
  Out of Scope:     Manual track reordering (Phase 2).
  Open Questions:   Max playlist length? Default 20 or configurable? (resolve before Plan)
```

**Rule**: story.md tells you WHAT to build next. spec.md tells you EXACTLY what "done" means for it.
The "User Stories" section of spec.md imports from story.md — it never invents new stories.

---

## Step 0 — Identify the Mode

Before anything else, ask the user:

> "Este projeto é **Greenfield** (começando do zero) ou **Brownfield** (projeto existente com código, dados ou histórico)?"

This single answer determines the entire entry path. Do not proceed without it.

---

## PATH A — Greenfield (New Project)
*Framework v1.1 — project starts from zero.*

### FASE 0 — Setup & Bootstrap

**Why this comes first**: Nothing can be built reliably without version control, a clear project identity, and a constitution that tells AI agents what rules to follow. This phase creates the skeleton before any feature work.

**Workflows**:
- `mjrp-environment-setup-protocol.md` → git init, branches (main/dev), .gitignore, folder structure, CI/CD scaffold
- `mjrp-project-bootstrap` (skill) → VISION.md, CHARTER.md, constitution.md, docs/specs/ structure, .claudeprompt, .gemini/GEMINI.md

**Outputs**:
- Git repo with main + dev branches
- `VISION.md` and `CHARTER.md` at root
- `ROADMAP.md` at root — created from CHARTER milestones (use `mjrp-templates/roadmap.md` as base)
- `docs/specs/constitution.md` (stack, methodology, governance, design reference)
- `docs/sessions/SESSION_HISTORY.md` initialized
- `.claudeprompt` and `.gemini/GEMINI.md` configured

**Commits**:
```
chore: project scaffold
docs: initial vision and charter
docs: initial roadmap from charter milestones
docs: project constitution
chore: folder structure
chore: AI config
```

⛔ **GATE — FOUNDATION APPROVAL**: Ask the user to review VISION.md, CHARTER.md, ROADMAP.md, and constitution.md.
Do not advance until they confirm these are correct. These files are what every AI agent reads
before making any decision — getting them right now prevents expensive rework later.

---

### FASE 1 — Discovery & Vision Refinement

**Why this matters**: Specifying features without deeply understanding the problem leads to building
the wrong thing. This phase ensures the Specify stage has solid, validated inputs.

**Workflows / Skills**:
- `mjrp-discovery` → empathize with users, ideate solutions, refine scope, document findings
- `mjrp-product-designer` (skill) → challenge assumptions, validate the opportunity (Cagan lens)
- `mjrp-it-executive` (skill) → executive / business viability perspective *(optional)*

**Outputs**:
- Validated problem statement + prioritized opportunity areas
- `docs/specs/story.md` initialized — first INVEST-ready user stories added from discovery findings
- `ROADMAP.md` updated — phases refined based on discovery insights
- `docs/specs/arch.md` skeleton — Clean Architecture layers, component map, routing, infra decisions (TBD)
- `docs/specs/data-model.md` skeleton — domain entities, relationships, DB schema first draft

> **Por que arch.md e data-model.md aqui?** O Design (FASE 2) precisa saber quais entidades existem
> e como o sistema é estruturado antes de criar a IA e o design system. Produzir esses artefatos
> durante o Design gera dependência circular — você não pode desenhar páginas sem saber que dados
> elas vão exibir. Skeletons produzidos aqui são refinados durante cada SDD Plan.

**Skills para arch.md + data-model.md**:
- `mjrp-system-architect` (skill) → Clean Architecture layers, component boundaries, routing
- `sdd-speckit` (skill) → garantir que arch.md e data-model.md seguem o template SpecKit

**Commits**:
```
docs: initial arch skeleton — layers, components, routing
docs: initial data model — domain entities and relationships
```

⚠️ **Nota**: arch.md e data-model.md neste ponto são **skeletons** — suficientes para informar o Design.
Eles são refinados e completados durante cada SDD Plan (onde detalhes de implementação emergem).

> Skip this phase only if the product vision is already locked and well-understood by both the user
> and the team. When in doubt, run it — it's cheap and prevents expensive spec rewrites.

---

### FASE 2 — Design

**Why this matters**: Design inputs — information architecture, wireframes, Stitch prototypes, visual
tokens — become the inputs for the Specify and Plan stages. Doing design after spec creates expensive
rework cycles. Design CONSUMES arch.md and data-model.md (produced in FASE 1) — não os produz.

**Pré-condição obrigatória**: `arch.md` e `data-model.md` (skeletons) devem existir antes de iniciar
esta fase. O design de IA e de componentes depende de saber quais entidades e rotas o sistema terá.

**FASE 2 tem três etapas em sequência:**

#### FASE 2a — Information Architecture (`ux-ui-designer`)
Estrutura do produto do ponto de vista do usuário. Precede o design visual — você não pode
estilizar páginas que ainda não definiu.

**Skills**: `mjrp-ux-ui-designer`
**Inputs**: `story.md` + `arch.md` + `data-model.md`
**Output**: `docs/specs/info-arch.md` com:
- Sitemap completo (todas as rotas do ponto de vista do usuário)
- Hierarquia de navegação (primária, secundária, terciária)
- Page templates com ASCII wireframes e zonas de conteúdo
- Fluxos de entrada por persona
- Mapeamento template → épico SDD

**Commit**: `docs: information architecture — sitemap, nav, page templates`

⛔ **GATE**: Aprovar info-arch.md antes de avançar para o design visual. Mudanças na estrutura
após o design-system estar feito são muito mais caras.

#### FASE 2b — Visual Design System (`aesthetic-designer` + `design-system`)
Tokens visuais, linguagem visual e especificação de componentes. Consumes info-arch.md para
saber quantos tipos de página e componentes o sistema precisa.

**Skills**: `mjrp-aesthetic-designer` + `mjrp-design-system`
**Inputs**: `info-arch.md` (page templates) + VISION.md (vibe)
**Output**: `docs/design/design-system.md` com tokens, componentes e specs visuais

**Commit**: `docs: design system — tokens, components, visual specs`

#### FASE 2c — High-Fidelity Prototyping (Stitch / opcional)
Mockups de alta fidelidade para aprovação visual antes do SDD.

**Skills**: `StitchMCP`
**Inputs**: `design-system.md` + `info-arch.md`
**Output**: Protótipos aprovados + referências em `design/inception/`

> Discovery (FASE 1) e a parte de skeleton de arch/data-model podem rodar em paralelo com
> FASE 2a para times experientes. FASE 2b exige FASE 2a completa.

---

### FASE 3 — SDD Cycle *(Iterative — repeat per sprint or feature)*

This is the engine of the framework. Every sprint or feature goes through all 4 stages in sequence.
**No stage can be skipped or combined.**

**Entry point**: A sprint-ready story from `story.md` (INVEST-compliant, acceptance criteria defined).
Run `mjrp-backlog-refine` first if stories are not sprint-ready.

**Exit point**: Committed, tested code in `src/` + updated `docs/specs/`.

**Derivation chain within each SDD cycle**:
```
story.md entry → [Specify] → spec.md → [Plan] → plan.md → [Tasks] → tasks.md → [Implement] → src/
```
Each artifact derives from the previous one. Each gate requires human approval before advancing.

> **Alternative entry point**: `mjrp-sdd` is the original simplified SDD workflow
> covering all 4 stages in one document. Use for lightweight features or quick reference.
> The granular protocols below are recommended for complex features or multi-agent teams.

---

#### SPECIFY — What and Why

**Input**: A sprint-ready story entry from `story.md` (the story provides the seed for spec.md).

**Workflow**: `mjrp-sdd-specify` → orchestrates `mjrp-sdd-speckit` + `mjrp-ba-sm` + `mjrp-qa-engineer`

**Pre-condition**: Run `mjrp-backlog-refine` first if stories in `story.md` are not
sprint-ready (not INVEST-compliant, too large, solution-shaped, or lacking acceptance criteria).

**How story.md feeds spec.md**:
The story entry from `story.md` becomes the "User Stories" section of `spec.md`. The Specify stage
then elaborates it — never invents new stories. The spec adds: Problem Statement, Functional
Requirements (REQ-IDs), Success Criteria, Out of Scope, Open Questions, Edge Cases.

**Outputs**: `docs/specs/story.md` (status updated) + `docs/specs/<feature>/spec.md` created with:
- User stories (imported from story.md, annotated with REQ traceability)
- Problem statement and business context
- Functional requirements (REQ-01, REQ-02...) — measurable and testable
- Acceptance criteria and edge cases
- Out of scope (critical for preventing scope creep)
- Open questions (ALL must be resolved before advancing to Plan)

**Commit**: `docs: complete specify stage for [feature]`

⛔ **GATE — SPEC APPROVAL**: Present spec.md to the user. Do not advance to Plan until they
explicitly approve and all Open Questions are resolved. This gate exists because changing requirements
after Plan has been written wastes significant effort.

> **Flow interruption rule**: If the user changes requirements during Plan that affect the spec,
> return here. Commit: `docs: revise specify for [feature] — requirement change`

---

#### PLAN — How

**Input**: Approved `spec.md` — every decision in plan.md must trace back to a REQ-ID.

**Workflow**: `mjrp-sdd-plan` → orchestrates `mjrp-system-architect` + `mjrp-architecture-review-protocol.md`
(if architectural decision is needed) + `mjrp-adr` (to formally document each decision)

**Outputs**: `docs/specs/<feature>/plan.md` created. Também **atualizar** (não criar):
- `docs/specs/arch.md` — adicionar detalhes de implementação específicos da feature
- `docs/specs/data-model.md` — refinar schema conforme decisões de implementação emergem
- `docs/specs/info-arch.md` — atualizar se a feature adicionar novas rotas ou templates
Com:
- Technical approach and library choices (must align with constitution.md)
- Data schemas and interfaces (references spec requirements)
- Component architecture and file structure (explicit file paths)
- UI mockups in ASCII (critical for frontend features)
- "Documents Consulted" section showing the agent read constitution.md, arch.md, design-system.md

**Commit**: `docs: complete plan stage for [feature]`

⛔ **GATE — PLAN APPROVAL**: Present plan.md to the user. Do not advance to Tasks without approval.

> **Flow interruption rule**: If architecture changes during Tasks, return here.
> Commit: `docs: revise plan for [feature] — architecture change`

---

#### TASKS — Decompose

**Input**: Approved `plan.md` — each task must trace to a plan section which traces to a spec REQ-ID.

**Workflow**: `mjrp-sdd-task` → `mjrp-conventional-commits` (for task commit format reference)

**Outputs**: `docs/specs/<feature>/tasks.md` with atomic, implementable checklist:
- Each task completable in one focused agent session (< 1 hour)
- Each task has a clear "done" signal (file created, test passes, UI renders)
- Tasks ordered by dependency (data layer → logic → UI → verification)
- Verification tasks included (test, build, lint, regression check)
- Documentation task at end (update specs, SESSION_HISTORY.md)

**Commit**: `docs: generate tasks for [feature]`

⛔ **GATE — TASK APPROVAL**: Present tasks.md to the user. Do not begin implementation without
explicit approval. This is the last checkpoint before code is written.

> **Flow interruption rule**: Scope change during Implement → return to Specify or Plan as appropriate.

---

#### IMPLEMENT — Execute *(per task, iterative)*

**Input**: Approved `tasks.md` — execute one task at a time.

**Workflow**: `mjrp-dev` (per task) → invoke specialist skill if needed:
`mjrp-frontend-developer` / `mjrp-backend-developer` / `mjrp-mobile-developer`

**Branch**: Create `feat/[feature-name]-[timestamp]` from dev before starting.

**Per-task loop** (from `mjrp-dev`):
1. Load context: read `constitution.md` + relevant specs (spec.md, plan.md, design-system.md)
2. Implement: write code following constitution rules
3. Verify: run tests, lint, validate against spec acceptance criteria
4. Document: update inline docs and relevant specs
5. Commit: `feat: [description] (ref task-N)`

**If blocked**: invoke `mjrp-debug` → systematic bug resolution (intake → analysis → fix → verify → close)

**Outputs**: Code in `src/`, tests in `tests/`

---

### FASE 4 — Quality & Testing

**Why at the end of each sprint**: Shipping debt accumulates fast. Running quality gates after every
sprint (not just before release) keeps the codebase healthy and prevents rework at scale.

**Workflows / Skills**:
- `mjrp-regression-protocol.md` → build + specific regression checks + full test suite
- `mjrp-code-quality-assessment-protocol.md` → sprint-end assessment: metrics, technical debt update, architecture health
- `mjrp-test-suite-audit-protocol.md` → test health: coverage gaps, flaky tests, deprecated patterns
- `mjrp-qa-engineer` (skill) → invoke if new test strategy or acceptance criteria need to be defined

---

### FASE 5 — Documentation & Closure

**Why mandatory**: Specs drift from code over time. Running this phase after every sprint keeps
docs/specs/ as a reliable source of truth for future AI agent sessions.

**Workflows / Skills**:
- `mjrp-doc` → post-implementation documentation checklist (update what changed)
- `mjrp-documentation-audit-protocol.md` → verify spec ↔ code sync (docs say what code does)
- `mjrp-conventional-commits` (skill) → release tag if applicable (`git tag -a vX.Y.Z`)
- Update `ROADMAP.md` → mark completed items, advance to next phase if milestone reached

**Commit**: `docs: update specs post-implementation [feature]`

---

## PATH B — Brownfield (Existing Project)
*Framework v1.2 — project already has code, data, and history.*

The key difference from Greenfield: **start by understanding what exists** before adding the framework.
The goal is to extract and document reality — not impose an ideal structure on top of existing code.

---

### FASE 0 — Audit & Bootstrap

**Why first**: Applying the framework blindly to an existing project breaks things. The inventory
and gap analysis reveal what already exists and what needs to be created vs. extracted vs. adapted.

**Skills**:
- `mjrp-project-bootstrap` *(Brownfield mode)* → inventory checklist + gap analysis
- `mjrp-save-context-handoff` → mine existing session history and AI conversation logs

**Produce `BOOTSTRAP_REPORT.md`** documenting:
- Inventory: code, data, git history, existing docs, AI configs (.gemini/, .mcp.json), design artifacts
- Gap analysis: which framework artifacts exist / partially exist / are missing
- Priority order: constitution.md and VISION.md first (AI agents read these before any action)

**Commit**: `docs: bootstrap MJRP Framework v1.2`
**Tag**: `git tag -a v0-framework-bootstrap -m "Start of MJRP Framework"`

⛔ **GATE — BOOTSTRAP APPROVAL**: User reviews BOOTSTRAP_REPORT.md and confirms the gap analysis
before any artifacts are created or modified.

> **Golden rule**: Do not reorganize code that works. Add `docs/specs/` as a new layer.
> Do not move `src/`, `.gemini/`, or other existing configs without explicit user request.

---

### FASE 0.5 — Extract Foundation Artifacts

**Why extract, not create**: For existing projects, VISION.md, CHARTER.md, and constitution.md
should reflect what the project **already is** — not what it could ideally become. Extract from
README, existing docs, chat history, Google Drive files, and the actual codebase.

**Skills**: `mjrp-project-bootstrap` + `mjrp-save-context-handoff` (to mine past sessions)

**Critical rule for constitution.md**: Document the CURRENT stack, patterns in use, and known
technical debt. Add a `## Legacy Notes` section for inconsistencies to fix gradually. An AI agent
reading an idealized constitution and finding a different reality in the code will produce garbage output.

**Also extract/create**:
- `ROADMAP.md` — derive from existing milestones, README, or project history
- `docs/specs/story.md` — populate from any existing backlog, issues, or feature list

**Commits**:
```
docs: bootstrap vision and charter
docs: initial roadmap from existing project history
docs: project constitution — current state
```

⛔ **GATE — FOUNDATION APPROVAL**: User reviews and confirms VISION.md, CHARTER.md, ROADMAP.md,
constitution.md accurately represent the project as it exists today.

---

### FASE 1B — SpecKit Retrofitting

**Why retrofit before specifying new features**: AI agents need to understand existing features
before working on new ones. Retrofitting creates that shared understanding.

**Choose retrofitting level** based on project size:

| Level | When to use | Artifacts | Effort |
|-------|-------------|-----------|--------|
| **Minimal** | Small project, few features | constitution.md + story.md (feature list) | 1-2h |
| **Standard** | Medium project, next phase is complex | + spec.md + arch.md + data-model.md + info-arch.md | 4-6h |
| **Full** | Large project, multiple agents/devs | All artifacts + mjrp-design-system.md + retroactive plan | 1-2 days |

**Skills**: `mjrp-sdd-speckit` + `mjrp-system-architect` + `mjrp-design-system` (if UI exists)

**Commits**:
```
docs: retrofit specs — existing features
docs: retrofit arch and data model
```

⛔ **GATE — RETROFIT APPROVAL**: User validates that retrofitted specs accurately reflect the
codebase. Inaccurate specs are worse than no specs — they mislead every AI agent that reads them.

---

### FASE 2B — Activate & Migrate

**Skills / Workflows**:
- `mjrp-project-bootstrap` → configure .claudeprompt and .gemini/GEMINI.md with newly created artifacts
- `mjrp-save-context-handoff` → create retroactive SESSION_HISTORY.md entries for past sessions
- `mjrp-environment-setup-protocol.md` → if environment needs additions (new CI/CD, missing tooling)

After this phase, Brownfield projects join the Greenfield flow at **FASE 3 — SDD Cycle**.

---

## Transversal — Active Throughout the Entire Lifecycle

These workflows and skills are not phase-specific — they run continuously:

| When | Workflow / Skill | Purpose |
|------|-------|---------|
| Start of every session | `mjrp-onboarding` | Load SESSION_HISTORY.md + specs before any work |
| End of every session | `mjrp-save-context-handoff` (skill) | Save to cowork_sessions/ + SESSION_HISTORY.md in repo |
| Before sprint / Specify gate | `mjrp-backlog-refine` | Ensure stories are INVEST-ready before SDD Specify |
| Every commit | `mjrp-conventional-commits` (skill) | Enforce commit format, branching, and SpecKit-linked commits |
| Any architectural decision | `mjrp-adr` | Document in docs/architecture/ so future agents understand why |
| When scope/vision shifts | Update `ROADMAP.md` | Reflect current reality; ROADMAP is a living document |

---

## Quick Reference — Skill & Workflow Map

| Phase | ⚙️ Workflow | 🧠 Skill | Artifact | Gate |
|-------|------------|---------|----------|------|
| FASE 0 Setup | `mjrp-environment-setup-protocol.md` | `mjrp-project-bootstrap` | VISION, CHARTER, ROADMAP, constitution | ✅ |
| FASE 1 Discovery | `mjrp-discovery` | `mjrp-product-designer`, `mjrp-it-executive` | story.md, ROADMAP update | — |
| FASE 1 (fim) | — | `mjrp-system-architect`, `sdd-speckit` | arch.md skeleton, data-model.md skeleton | — |
| FASE 2a IA | — | `mjrp-ux-ui-designer` | info-arch.md | ✅ |
| FASE 2b Visual | `mjrp-design-protocol.md` | `mjrp-aesthetic-designer`, `mjrp-design-system` | design-system.md | — |
| FASE 2c Proto | — | `StitchMCP` | design/inception/ | — |
| SDD Specify | `mjrp-sdd-specify` | `mjrp-sdd-speckit`, `mjrp-ba-sm`, `mjrp-qa-engineer` | spec.md (from story.md) | ✅ |
| SDD Plan | `mjrp-sdd-plan` | `mjrp-system-architect` + `mjrp-architecture-review-protocol.md` | plan.md (from spec.md) | ✅ |
| SDD Tasks | `mjrp-sdd-task` | `mjrp-conventional-commits` | tasks.md (from plan.md) | ✅ |
| SDD Implement | `mjrp-dev`, `mjrp-debug` | `mjrp-frontend-developer` / `mjrp-backend-developer` / `mjrp-mobile-developer` | src/, tests/ | — |
| FASE 4 Quality | `mjrp-regression-protocol.md`, `mjrp-code-quality-assessment-protocol.md`, `mjrp-test-suite-audit-protocol.md` | `mjrp-qa-engineer` | — | — |
| FASE 5 Docs | `mjrp-doc`, `mjrp-documentation-audit-protocol.md` | `mjrp-conventional-commits` | ROADMAP update | — |
| Transversal | `mjrp-onboarding`, `mjrp-backlog-refine`, `mjrp-adr` | `mjrp-save-context-handoff`, `mjrp-conventional-commits` | SESSION_HISTORY | — |
| Brownfield 0 | — | `mjrp-project-bootstrap`, `mjrp-save-context-handoff` | BOOTSTRAP_REPORT | ✅ |
| Brownfield 0.5 | — | `mjrp-project-bootstrap`, `mjrp-sdd-speckit`, `mjrp-system-architect` | VISION, CHARTER, ROADMAP, constitution | ✅ |
| Brownfield 2B | `mjrp-environment-setup-protocol.md` | `mjrp-project-bootstrap`, `mjrp-save-context-handoff` | .claudeprompt, GEMINI.md | — |
