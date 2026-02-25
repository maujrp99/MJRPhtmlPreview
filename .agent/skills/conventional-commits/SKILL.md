---
name: Conventional Commits & SCM Governance
description: >
  Use when making Git commits, creating branches, or tagging releases. Covers
  commit types (feat, fix, docs, refactor, vibe, chore), message format,
  SpecKit-linked commits, branching strategy (main/dev/feat), tagging, and
  Brownfield-specific migration rules.
---

# Skill: Conventional Commits & SCM Governance

**Purpose**: Teach an AI agent the commit conventions, branching strategy, and Git governance rules of the MJRP Vibe Coding Framework.

**Related Workflows**: `developer_protocol.md`, `sdd_protocol.md`

---

## Commit Types

| Type | When to Use | Example |
|------|------------|---------|
| `feat` | New functionality | `feat: add book card component with cover grid` |
| `fix` | Bug correction | `fix: resolve filter reset on page navigation` |
| `docs` | Documentation/specs changes | `docs: complete specify stage for bookshelf` |
| `refactor` | Code change without behavior change | `refactor: extract API calls into shared service` |
| `vibe` | UI/UX aesthetic adjustments | `vibe: adjust card shadows and hover transitions` |
| `chore` | Maintenance (deps, configs, CI) | `chore: update Next.js to 15.2` |
| `test` | Adding or updating tests | `test: add unit tests for BookCard component` |

---

## Commit Message Format

```
<type>: <short description in imperative mood>

[optional body — explain WHY, not WHAT]

[optional footer — references, breaking changes]
```

### Rules
- **Imperative mood**: "add feature" not "added feature" or "adds feature"
- **Lowercase**: Start with lowercase after the type prefix
- **No period**: Don't end the subject line with a period
- **Max 72 chars**: Keep the subject line concise
- **Body for WHY**: The diff shows WHAT changed; the body explains WHY

### Good Examples
```
feat: add garden status filter to bookshelf page

Users can now filter books by garden status (seed, seedling, growing, evergreen).
Filter persists across page navigation via URL params.

Ref: docs/specs/bookshelf/tasks.md #3
```

```
docs: complete specify stage for bookshelf

- Define requirements for book grid display
- Add filter and search specifications
- Document success criteria and edge cases

Gate: Ready for Plan phase review
```

```
vibe: soften card shadows and adjust hover state

Aligned with Organic Blueprint theme — cards now feel
more paper-like with subtle depth.
```

### Bad Examples
- ❌ `Updated stuff` — no type, vague
- ❌ `feat: Added the new book card component.` — past tense, period
- ❌ `fix: fix bug` — redundant, no context
- ❌ `docs/feat/fix: multiple things` — one type per commit

---

## SpecKit-Linked Commits

Each SpecKit stage transition generates a documentation commit:

| Stage Completed | Commit Pattern |
|----------------|----------------|
| Specify | `docs: complete specify stage for <feature>` |
| Plan | `docs: complete plan stage for <feature>` |
| Tasks | `docs: generate tasks for <feature>` |
| Implement | `feat: implement <description>` (ref task) |
| Rollback | `docs: revise <stage> for <feature> — requirement change` |

---

## Branching Strategy

### Branches
- **main**: Stable, deployable code. Protected.
- **dev**: Integration branch for features in progress.
- **feat/<name>-<timestamp>**: Short-lived feature branches.

### Branch Naming
```
feat/bookshelf-filters-20260217
feat/about-page-20260218
fix/cover-loading-20260217
```

### Flow
```
main ← dev ← feat/my-feature-YYYYMMDD
```

1. Create feature branch from `dev`
2. Work on feature (multiple commits)
3. Merge to `dev` when feature is complete
4. Merge `dev` to `main` when stable

---

## Tagging

### When to Tag
- Framework bootstrap: `v0-framework-bootstrap`
- Major milestones: `v1.0`, `v1.1`
- Sprint completions: `sprint-01-complete`

### Tag Format
```bash
git tag -a v1.0 -m "First stable release with bookshelf and about page"
```

---

## Brownfield-Specific Rules

1. **Never rebase or squash existing history** — the past is the past
2. **Apply conventions going forward** from the bootstrap commit
3. **Create a bootstrap tag**: `v0-framework-bootstrap`
4. **Keep existing branches** until natural merge — don't force main/dev if it didn't exist
