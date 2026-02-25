---
name: Project Bootstrap (Greenfield & Brownfield)
description: >
  Use when bootstrapping a NEW project or adopting the framework on an EXISTING
  codebase. Covers folder structure creation, VISION.md and CHARTER.md writing
  guides, Brownfield audit and gap analysis, extraction process from legacy code,
  and bootstrap commit strategy.
---

# Skill: Project Bootstrap (Greenfield & Brownfield)

**Purpose**: Teach an AI agent how to set up or adopt the MJRP Vibe Coding Framework on a project — either from scratch (Greenfield) or on an existing codebase (Brownfield).

**Related Workflows**: `onboarding_protocol.md`, `developer_protocol.md`, `architecture_decision_protocol.md`
**Related Templates**: `onboarding_developer.md`, `onboarding_qa.md`, `onboarding_ux_ui.md`, `onboarding_devops.md`, `reference_guide_index.md`, `adr_template.md`, `technical_debt.md`, `agent_rules_template.md`, `roadmap.md`

---

## Greenfield Bootstrap

### Step-by-Step

```
1. Create VISION.md + CHARTER.md           → commit: docs: initial vision and charter
2. git init + .gitignore + first commit    → commit: chore: project scaffold
3. Create folder structure                 → commit: chore: folder structure
4. Create constitution.md                  → commit: docs: project constitution
5. Create design-system.md (if UI)         → commit: docs: design system
6. Specify first feature                   → commit: docs: specify <feature>
7. Plan first feature                      → commit: docs: plan <feature>
8. Generate tasks                          → commit: docs: tasks <feature>
9. Configure .claudeprompt / GEMINI.md     → commit: chore: AI config
10. Start implementing                     → commit: feat: <feature>
```

### Folder Structure Template

```
/project-root
├── .github/                # CI/CD workflows
├── .claudeprompt           # Claude Code system prompt
├── .gemini/                # Antigravity config
├── docs/
│   ├── specs/              # SpecKit (the project brain)
│   │   ├── constitution.md
│   │   ├── story.md
│   │   ├── arch.md
│   │   ├── data-model.md
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── design-system.md
│   │   └── regression_checklist.md
│   ├── architecture/       # ADRs (see adr_template.md)
│   ├── manual/             # Reference Guide (see reference_guide_index.md)
│   │   └── 00_INDEX.md
│   ├── onboarding/         # Role-based onboarding (see templates)
│   │   ├── DEVELOPER.md
│   │   ├── QA_ENGINEER.md
│   │   ├── UX_UI.md
│   │   └── DEVOPS.md
│   ├── sessions/           # AI session history
│   │   ├── SESSION_HISTORY.md
│   │   └── DEBUG_LOG.md
│   ├── TECHNICAL_DEBT.md   # Tech debt registry (see template)
│   └── ROADMAP.md          # Living roadmap (see roadmap.md template)
├── src/                    # Source code
├── tests/                  # Tests
├── VISION.md
├── CHARTER.md
├── README.md
└── .gitignore
```

### VISION.md Writing Guide

Keep it short (under 100 words). It answers: "Why does this project exist?"

```markdown
# [Project Name]

## Core Objective
[One sentence defining success]

## The Vibe
[Aesthetic direction — color palette name, mood, references]

## User Empathy
[The main pain point this project alleviates]

## Design DNA
[Visual reference — Stitch link, screenshot, or description]
```

**Tips**:
- "The Vibe" is not fluff — it guides every UI decision agents make
- "User Empathy" forces you to think from the user's perspective
- Keep updating this as the vision evolves

### CHARTER.md Writing Guide

The boundary document. It answers: "What are we building, and what are we NOT building?"

**Essential sections** (from PMI + Asana best practices):
- Title and Description
- Justification (Business Case)
- Main Goals and Success Metrics
- High-Level Scope (In / Out)
- Main Stakeholders
- Roadmap (Milestones) — initial high-level milestones; evolves into `docs/ROADMAP.md`
- Risks and Constraints
- AI Tooling (which AI tools and their roles)

---

## Brownfield Bootstrap

### Phase 0: Audit & Inventory

Before anything, map what exists:

| Category | What to check | Where to look |
|----------|--------------|---------------|
| Code | Languages, frameworks, structure | src/, package.json, requirements.txt |
| Data | Schemas, models, content | DB, vault, APIs, data files |
| Git | Branches, commits, history | git log, git branch -a |
| Documentation | Specs, docs, READMEs | docs/, README.md, *.md |
| AI Tools | Configs, histories, prompts | .gemini/, .mcp.json, .claudeprompt |
| Design | Prototypes, wireframes, UI | Stitch, Figma, screenshots |
| Sessions | Past AI session context | SESSION_HISTORY.md, saved chats |

### Phase 1: Gap Analysis

For each Framework artifact, determine:
- **Exists**: Already present in compatible format → keep as-is
- **Partial**: Content exists but in different format → extract and adapt
- **Missing**: No equivalent exists → create from scratch

### Phase 2: Extract or Create

**Extraction Rule**: If equivalent content exists somewhere, EXTRACT it into the correct format rather than writing from scratch. Sources:
- Google Docs → VISION.md, CHARTER.md
- Package.json + code patterns → constitution.md
- Existing READMEs / specs → story.md, spec.md
- UI prototypes / CSS → design-system.md
- Git history → arch.md (infer architecture from commit patterns)
- AI chat histories → SESSION_HISTORY.md (retroactive entries)

### Phase 3: Bootstrap Commit

One commit for all new framework artifacts:

```
docs: bootstrap MJRP Framework v1.2

- Add VISION.md, CHARTER.md
- Add docs/specs/ with constitution, story, spec, arch, data-model, plan, tasks
- Add docs/sessions/SESSION_HISTORY.md
- Add .claudeprompt
```

Then tag: `git tag -a v0-framework-bootstrap -m "Start of MJRP Framework"`

### Key Brownfield Principles

1. **Don't move working code.** Add docs/specs/ as a layer, don't reorganize src/.
2. **constitution.md reflects REALITY.** Write what IS, not what SHOULD BE. Evolution goes in the backlog.
3. **One commit for bootstrap.** Easy to revert if something breaks.
4. **Don't rewrite Git history.** Apply conventions going forward only.
5. **Legacy Notes in constitution.** Document known debt so agents are aware.
