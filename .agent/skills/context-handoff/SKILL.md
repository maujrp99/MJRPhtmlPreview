---
name: Context Handoff & Session Recovery
description: >
  Use when ending a session, starting a new session, or transferring work between
  AI tools. Covers SESSION_HISTORY.md writing, session recovery protocol, cross-tool
  transfer via Git (Bridge Pattern), retroactive entries for Brownfield projects,
  and context compression strategies.
---

# Skill: Context Handoff & Session Recovery

**Purpose**: Teach an AI agent how to preserve, transfer, and recover context between sessions and across different AI tools.

**Related Workflows**: `onboarding_protocol.md`

---

## Core Problem

AI agents lose all context between sessions. Without a handoff mechanism, every new session starts from zero — wasting time re-reading files and risking contradictory decisions.

---

## 1. Writing a SESSION_HISTORY.md Entry

### When to Write
- At the END of every work session (mandatory)
- When switching between AI tools (Cowork → Antigravity, etc.)
- Before a long pause in the project

### Template

```markdown
## Session: [YYYY-MM-DD] — [Brief Title]

> Date: [full date and time]
> Participants: [human] + [AI tool name]
> Branch: [active git branch]
> Duration: [approximate]

### Resumo Executivo
[2-3 sentences: what was accomplished this session]

### Decisões Tomadas
- [Decision 1]: [Context and rationale]
- [Decision 2]: [Context and rationale]

### Artefatos Gerados/Modificados
| Arquivo | Ação | Descrição |
|---------|------|-----------|
| [path] | Criado/Modificado | [what changed] |

### Pendências para Próxima Sessão
1. [Highest priority pending item]
2. [Second priority]
3. [Third priority]

### Dados-Chave para Referência
- [Key metric, count, or value that future sessions need]
```

### Quality Criteria
- **Resumo Executivo**: Must be understandable without reading the rest. A new agent should know what happened in 10 seconds.
- **Decisões**: Only include decisions that CONSTRAIN future work. "We chose Next.js over Quartz" is relevant. "We discussed color options" is not (unless a color was chosen).
- **Artefatos**: Must include file paths, not just descriptions.
- **Pendências**: Ordered by priority. First item = what the next session should start with.
- **Dados-Chave**: Numbers, counts, versions that would be expensive to re-derive.

### Anti-patterns
- ❌ Too detailed: 500+ word entries that agents won't fully read
- ❌ Too vague: "Worked on the project" — useless for recovery
- ❌ Missing paths: "Updated the spec" — which spec? where?
- ❌ No pendências: Next session has no starting point
- ✅ Goldilocks: 150-300 words, specific, actionable

---

## 2. Recovering Context (Session Start or User Asking to Get Updated)

### The Recovery Protocol

When starting a new session, the agent should:

1. **Read SESSION_HISTORY.md** — Focus on the LAST entry
2. **Check Pendências** — These are your starting tasks
3. **Check git status** — What branch? Any uncommitted changes?
4. **Check git log (last 5)** — What was the last commit?
5. **Acknowledge to user**: State what you loaded and what you plan to do

### Recovery Statement Template

> "I've loaded context from the session on [date] with [tool]. Last session: [1-sentence summary]. Pending items: [list top 3]. Current branch: [branch]. I'll start with [first pending item]. Ready?"

### What to Do When There's No History

If SESSION_HISTORY.md doesn't exist or is empty:
1. Run the full onboarding protocol (read VISION, CHARTER, constitution, arch, specs)
2. Check git log for recent activity
3. Ask the user for context
4. Create the first SESSION_HISTORY.md entry at the end of this session

---

## 3. Cross-Tool Context Transfer

When context needs to move between AI tools (e.g., Cowork → Antigravity):

### The Bridge Pattern

The Git repo is the universal bridge. All tools read from and write to the same repo.

```
Cowork Session                    Antigravity Session
     │                                  │
     ├── Updates docs/specs/            │
     ├── Updates SESSION_HISTORY.md     │
     ├── git commit + push         ───► git pull
     │                                  ├── Reads SESSION_HISTORY.md
     │                                  ├── Reads docs/specs/
     │                                  └── Continues work
```

### Rules for Cross-Tool Handoff
- Always commit and push before switching tools
- SESSION_HISTORY.md entry must mention which tool is expected next
- Include tool-specific notes: "Antigravity should focus on implementing tasks 1-3 from tasks.md"
- Never assume the next tool has chat history — everything must be in files

---

## 4. Retroactive Context (Brownfield)

For sessions that happened BEFORE the framework was adopted:

### Template for Retroactive Entries

```markdown
## [RETROATIVO] Sessão Consolidada: [period]

> Fontes: [where this info was extracted from]
> Consolidado por: [tool] em [date]

### O que foi feito
[Summary of activities during this period]

### Decisões que impactam o projeto
[Only decisions relevant to future work]

### Estado ao final
[Snapshot: what existed at the end of this period]
```

### Extraction Sources
- `.gemini/antigravity/conversations/` — Antigravity chat history
- Cowork session transcripts
- Git commit messages and diffs
- Google Docs, Stitch chats, or other collaboration tools
- The human's memory (ask them!)

---

## 5. Context Compression

Over time, SESSION_HISTORY.md grows. Keep it useful:

### Compression Rules
- After 10+ entries: Archive older entries to `docs/archive/session_history_[period].md`
- Keep the last 5 entries in the main file
- Create a "Project Timeline Summary" section at the top with 1-line-per-session

### Timeline Summary Example

```markdown
# Project Timeline

| Date | Tool | Summary |
|------|------|---------|
| 2026-02-15 | Cowork | Initial spec, data analysis, vault migration |
| 2026-02-16 | Cowork | Vault ops skill, framework design |
| 2026-02-17 | Cowork | Framework v1.1/v1.2, workflows, skills |
```
