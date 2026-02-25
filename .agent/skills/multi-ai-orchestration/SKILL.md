---
name: Multi-AI Orchestration
description: >
  Use when coordinating work across multiple AI tools or handing off between them.
  Defines roles (Cowork as Strategist, Claude Code and Antigravity as Builders,
  Stitch as Designer), context flow patterns, the Git-as-hub model, cross-tool
  handoff rules, and .claudeprompt/GEMINI.md templates.
---

# Skill: Multi-AI Orchestration

**Purpose**: Teach an AI agent how to operate within a multi-AI ecosystem where different tools have different roles, and context flows through shared artifacts in Git.

**Related Workflows**: `onboarding_protocol.md`, `developer_protocol.md`

---

## The Ecosystem Model

Each AI tool has a defined role. No tool does everything. The Git repo is the universal hub.

```
                    ┌─────────────┐
                    │   Git Repo  │
                    │  (The Hub)  │
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │   Cowork    │ │ Claude Code │ │ Antigravity │
    │ (Strategist)│ │ (Builder)   │ │ (Builder)   │
    └─────────────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           │        ┌──────▼──────┐        │
           └───────►│   Stitch    │◄───────┘
                    │ (Designer)  │
                    └─────────────┘
```

---

## Tool Roles

### Claude Cowork — The Strategist
**Strengths**: Broad context (reads files, Drive, browser), brainstorming, analysis, document generation
**Best for**:
- Creating and refining SpecKit artifacts (spec, plan, tasks)
- Data analysis and decision support
- Session history and context consolidation
- Framework setup and bootstrap
- Skill and workflow creation
**Writes to Git**: docs/specs/, docs/sessions/, skills/, VISION.md, CHARTER.md

### Claude Code — The Builder
**Strengths**: Terminal access, full codebase context via .claudeprompt, fast iteration
**Best for**:
- Code implementation (following tasks.md)
- Refactoring and testing
- Git operations (commits, branches, merges)
- Build and deploy scripts
- Debugging with full stack traces
**Writes to Git**: src/, tests/, package.json, configs

### Antigravity (Jules) — The Builder
**Strengths**: Full code implementation, GitHub integration, code_tracker, persistent conversations, visual file explorer
**Best for**:
- Code implementation (following tasks.md) — same capability as Claude Code
- Refactoring, testing, and debugging
- Code review and suggestions
- Following implementation plans step by step
- Working with GitHub issues and PRs
- Git operations via GitHub integration
**Writes to Git**: src/, tests/, configs, via code_tracker

> **Nota**: Antigravity e Claude Code são ambos Builders. A escolha entre eles depende de preferência pessoal e contexto — Claude Code é terminal-first (ideal para quem vive no terminal), Antigravity é visual-first (ideal para quem prefere UI e integração direta com GitHub). Ambos podem executar tasks.md com a mesma qualidade.

### Stitch — The Designer
**Strengths**: AI-powered UI design, prototyping, visual iteration
**Best for**:
- Creating UI mockups and prototypes
- Exploring visual directions
- Design system creation
- Responsive layout experimentation
**Outputs**: Design assets, referenced in docs/specs/design-system.md

---

## Context Flow Patterns

### Pattern 1: Spec → Implement
```
Cowork: Creates spec.md + plan.md + tasks.md
         ↓ (commit + push)
Claude Code or Antigravity: Pulls, reads tasks.md, implements
         ↓ (commit + push)
Cowork: Reviews, updates SESSION_HISTORY.md
```

### Pattern 2: Design → Implement
```
Stitch: Creates UI prototypes
         ↓ (human exports to design-system.md or references Stitch link)
Cowork: Documents in docs/specs/design-system.md + plan.md
         ↓ (commit + push)
Claude Code or Antigravity: Implements following design-system.md
```

### Pattern 3: Debug → Fix
```
Any tool: Identifies bug
         ↓
Cowork: Analyzes, writes debug plan (if complex)
         ↓ (commit)
Claude Code: Implements fix, runs tests
         ↓ (commit + push)
Cowork: Updates SESSION_HISTORY.md + DEBUG_LOG.md
```

---

## Rules for Multi-AI Work

### 1. Always Commit Before Switching Tools
The next tool can only see what's in Git. Uncommitted work is invisible.

### 2. SESSION_HISTORY.md is the Relay Baton
When handing off to another tool, the session history entry should include:
- What was accomplished
- What the NEXT tool should do
- Which files are relevant

### 3. Each Tool Reads constitution.md First
Regardless of which tool is active, it should read constitution.md before making technical decisions.

### 4. Don't Duplicate Work Across Tools
If Cowork already wrote the spec, Antigravity shouldn't rewrite it. Tools build on each other's work.

### 5. Respect Tool Boundaries
- Cowork doesn't write production code (it writes specs, docs, skills)
- Claude Code and Antigravity don't do brainstorming sessions (they execute plans)
- Stitch doesn't write code (it designs interfaces)
- When both Builders are active on the same repo, coordinate via SESSION_HISTORY.md to avoid merge conflicts

### 6. Conflict Resolution
If two tools made conflicting changes:
1. Check which change aligns with constitution.md
2. Check which change was more recent
3. If unclear, escalate to human decision
4. Document the resolution in an ADR if it changes a pattern

---

## .claudeprompt Template

For Claude Code, the `.claudeprompt` file acts as a persistent system prompt:

```
You are a developer working on [Project Name].
Before any implementation, read:
- VISION.md (purpose)
- CHARTER.md (scope and limits)
- docs/specs/constitution.md (technical rules)
- docs/specs/design-system.md (visual patterns)
- docs/specs/tasks.md (current backlog)

Rules:
- Follow Conventional Commits
- Never implement without a task in tasks.md
- Consult constitution.md before suggesting dependencies
- Update SESSION_HISTORY.md at end of session
```

## GEMINI.md Template

For Antigravity, a similar role definition:

```
You are a developer on [Project Name].
Consult these files before any work:
- VISION.md, CHARTER.md
- docs/specs/constitution.md
- docs/specs/tasks.md

Follow Conventional Commits.
Check constitution.md before adding dependencies.
```
