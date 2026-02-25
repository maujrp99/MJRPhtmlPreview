---
description: Context Loader Protocol — Session Recovery + Project Onboarding + Deep Context Loading for AI Agents
---

# Context Loader Protocol (Onboarding)

**Purpose**: Recover previous session context, establish the "Mental Model" for Agents, and perform deep context loading before starting work.
**Trigger**: At the start of every new session, before a complex refactor, or when asked to "Audit" or "Understand" a feature.

---

## Phase 0: Session Recovery (Always First)

> Before doing anything else, check if there is previous session context to load.

1. **Check for Session History**: Read `docs/sessions/SESSION_HISTORY.md`.
   - If it exists: Load the most recent entry. Pay special attention to:
     - **Resumo Executivo**: What was done last time.
     - **Decisões Tomadas**: Decisions that constrain current work.
     - **Pendências para Próxima Sessão**: These are your starting tasks.
     - **Dados-Chave para Referência**: Metrics and values to keep in mind.
   - If it doesn't exist: This is a fresh start — proceed to Phase 1.

2. **Check for Debug Log**: Read `docs/sessions/DEBUG_LOG.md` (if it exists).
   - Are there active/unresolved issues from the previous session?

3. **Check Current Branch**: Run `git status` and `git log --oneline -5` to understand where the code left off.

4. **Acknowledge Context**: State to the user:
   > "I've loaded context from the previous session on [date]. Last session covered [summary]. Pending items are: [list]. Current branch is [branch]. Ready to continue."

---

## Phase 1: Project Identity (If First Session or Deep Reset)

> Skip this phase if Session Recovery (Phase 0) provided sufficient context.

1. Read `VISION.md` to align with the project's core philosophy and vibe.
2. Read `CHARTER.md` to understand scope, stakeholders, and constraints.
3. Read `docs/specs/constitution.md` to load technical rules, stack, and patterns.

## Phase 2: Technical Context

4. Read `docs/specs/arch.md` to understand the system architecture.
5. Read `docs/specs/story.md` and `docs/specs/spec.md` to understand current features and requirements.
6. Read `docs/specs/tasks.md` to understand the current backlog and progress.

## Phase 3: Deep Context Loading (Targeted by Role)

> Select the areas relevant to your current task. Read "All" if this is a full onboarding.

### Architecture & Infrastructure
*Files to Read*: `docs/specs/arch.md`, `docs/specs/data-model.md`
*Goal*: Understand the high-level data flow, infrastructure constraints, and deployment model.

### Logic & Services (The "Brain")
*Files to Read*: `docs/specs/spec.md`, `docs/specs/story.md`
*Goal*: Understand *how* things work. Key algorithms, service orchestration, business rules.

### UI & Experience (The "Face")
*Files to Read*: `docs/specs/design-system.md`, `docs/specs/plan.md`
*Goal*: Understand the Visual System, Component Hierarchy, and Design Patterns.
*Optional*: Check Stitch/Figma project reference if UI task.

### Data & State
*Files to Read*: `docs/specs/data-model.md`
*Goal*: Understand the shape of the data, schemas, and persistence models.

### Testing
*Files to Read*: Test suite docs + `README.md` (commands section)
*Goal*: Understand test strategy, available commands, and coverage baseline.

## Phase 4: Synthesis & Verification

1. **Identify Constraints**: What patterns MUST be followed? (from constitution.md)
2. **Spot Dependencies**: What services/components interact with the feature you are about to modify?
3. **Brief Summary**: State: "I have loaded context from [list files]. I understand [key patterns]. Ready to proceed."

---

## Session End: Context Handoff (Mandatory)

> At the END of every session, update `docs/sessions/SESSION_HISTORY.md` so the next session can recover context.

Follow the SESSION_HISTORY.md template defined in the MJRP Vibe Coding Framework (Section 8).
