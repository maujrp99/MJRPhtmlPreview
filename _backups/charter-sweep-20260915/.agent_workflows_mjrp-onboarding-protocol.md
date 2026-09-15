---
description: Context Loader Protocol — Session Recovery + Project Onboarding + Deep Context Loading for AI Agents
---

# Context Loader Protocol (Onboarding)

**Purpose**: Recover previous session context, establish the "Mental Model" for Agents, and perform
deep context loading before starting any work.

**Trigger**: At the START of every new session, before a complex refactor, or when asked to "Audit"
or "Understand" a feature.

**Responsibility split**:
- This workflow (`mjrp-onboarding-protocol.md`) → owns session **START**: context recovery + project loading
- `mjrp-save-context-handoff` skill → owns session **END**: saving + cross-tool bridge

---

## Phase 0: Session Recovery (Always First)

> Before doing anything else, check if there is previous session context to load.

1. **Check for Session History**: Read `docs/SESSION_HISTORY.md`.
   Also check `docs/sessions/SESSION_HISTORY.md` if the former doesn't exist (legacy path).
   - If it exists: Load the most recent entry. Pay special attention to:
     - **Resumo Executivo**: What was done last time.
     - **Decisões Tomadas**: Decisions that constrain current work.
     - **Pendências para Próxima Sessão**: These are your starting tasks.
     - **Dados-Chave para Referência**: Metrics and values to keep in mind.
   - If it doesn't exist: This is a fresh start — proceed to Phase 1.

2. **Check for Cowork Session File**: If the user shared a `.md` file from
   `claude_cowork_sessions/`, read it and prioritize it — it's more detailed than
   SESSION_HISTORY.md entries.

3. **Check for Debug Log**: Read `docs/sessions/DEBUG_LOG.md` (if it exists).
   Are there active/unresolved issues from the previous session?

4. **Check Current Branch**: Run `git status` and `git log --oneline -5` to understand where
   the code left off.

5. **Acknowledge Context**: State to the user:
   > "Carreguei o contexto da sessão de [data]. Última sessão cobriu [resumo em 1 frase].
   > Pendências: [lista top 3]. Branch atual: [branch]. Vou começar por [primeiro item]. Bora?"

---

## Phase 1: Project Identity (If First Session or Deep Reset)

> Skip this phase if Phase 0 provided sufficient context to proceed.

1. Read `VISION.md` — align with the project's core philosophy and goals.
2. Read `CHARTER.md` — understand scope, stakeholders, initial milestones, and constraints.
3. Read `ROADMAP.md` — load current tactical phase, active priorities, and upcoming milestones.
   ROADMAP derives from CHARTER and reflects the living state of the project.
4. Read `docs/specs/constitution.md` — load technical rules, stack, patterns to follow and avoid.

> **Derivation chain reminder**: CHARTER → ROADMAP → story.md (backlog) → spec.md → plan.md → tasks.md.
> Reading CHARTER and ROADMAP first prevents contradicting strategic decisions during implementation.

---

## Phase 2: Technical Context

5. Read `docs/specs/arch.md` — understand the system architecture and component map.
6. Read `docs/specs/story.md` — the **product backlog**: INVEST-ready user stories prioritized by
   phase. This tells you WHAT is planned to be built next. Note: story.md is the backlog input
   to SDD Specify — it feeds spec.md but is not the same as spec.md.
7. Read `docs/specs/spec.md` (current feature, if known) — detailed requirements, REQ-IDs,
   success criteria, and acceptance criteria for what is currently being built.
8. Read `docs/specs/tasks.md` — current implementation checklist and progress.

---

## Phase 3: Deep Context Loading (Targeted by Role)

> Select areas relevant to your current task. Read "All" only on full onboarding.

### Architecture & Infrastructure
*Files*: `docs/specs/arch.md`, `docs/specs/data-model.md`
*Goal*: Understand high-level data flow, infrastructure constraints, and deployment model.

### Logic & Services (The "Brain")
*Files*: `docs/specs/spec.md`, `docs/specs/story.md`
*Goal*: Understand how things work — key algorithms, service orchestration, business rules.

### UI & Experience (The "Face")
*Files*: `docs/specs/design-system.md`, `docs/specs/plan.md`
*Goal*: Understand the visual system, component hierarchy, and design patterns.
*Optional*: Check Stitch/Figma project reference if the task is UI-focused.

### Data & State
*Files*: `docs/specs/data-model.md`
*Goal*: Understand entity shapes, schemas, relationships, and persistence models.

### Testing
*Files*: Test suite docs + `README.md` (commands section)
*Goal*: Understand test strategy, available commands, and coverage baseline.

---

## Phase 4: Synthesis & Verification

1. **Identify Constraints**: What patterns MUST be followed? (from constitution.md)
2. **Spot Dependencies**: What services/components interact with the feature you're about to modify?
3. **Check ROADMAP alignment**: Does the task you're about to start match the current phase in ROADMAP.md?
4. **Brief Summary**: State:
   > "Carreguei contexto de [lista de arquivos]. Entendo [padrões chave]. Branch [branch].
   > Pronto para começar."

---

## Session End: Context Handoff (Mandatory)

> At the END of every session, save context so the next session (or next tool) can recover it.

Invoke the **`mjrp-save-context-handoff`** skill to:
- Generate the session file in `claude_cowork_sessions/YYYY-MM-DD_Projeto.md`
- Update `docs/SESSION_HISTORY.md` in the project repo
- Commit and push if switching tools (cross-tool bridge)

Never end a session without saving — the next session starts blind otherwise.
