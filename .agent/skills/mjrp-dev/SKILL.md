---
name: mjrp-dev
description: >
  Full Stack Developer skill for AI-assisted development. Covers pre-flight protocol, componentization and modularization rules, architecture principles (Clean Architecture, SOLID, dependency isolation), data flow discipline, golden rules for AI agents, verifiable code quality checklist, operational mindset, and anti-patterns catalog.
  Trigger: implement feature, write code, develop, coding, full stack, start development, new enhancement, bug fix, add feature, refactor, create component, build module, protocolo de desenvolvimento, implementar feature, escrever código, desenvolver.
---

# Full Stack Developer

## §0 — Pre-flight Protocol
> **STOP. Execute this checklist before writing a single line of code.**

- [ ] Read `VISION.md` — product direction and north star
- [ ] Read `CHARTER.md` — scope boundaries (what is and isn't in scope)
- [ ] Read `ROADMAP.md` — current milestone context
- [ ] Read `docs/specs/constitution.md` — this is the law of the project. If it doesn't exist, ask the user to create it before proceeding.
- [ ] Read `docs/specs/arch.md` — understand the layer map and data flow chain. Never improvise layers.
- [ ] Read `docs/specs/info-arch.md` — understand the information architecture (if exists).
- [ ] Read `docs/specs/design-system.md` — understand the design system and component library (if exists).
- [ ] Identify the **correct layer** for the code you're about to write. Ask: which directory does this belong to?
- [ ] Check `docs/specs/<feature>/` for SDD artifacts (`spec.md`, `plan.md`, `tasks.md`). If implementing a new feature and none exist, ask: *"Do we need an SDD cycle for this?"*
- [ ] Confirm you understand the **data flow chain** of this project (documented in `arch.md`). Every layer must be respected.
- [ ] Always follow the process in `.agent/skills/mjrp-project-lifecycle/SKILL.md`

**If any of the above is missing or unclear: STOP and ask the user before proceeding.**

---

## §1 — Componentization & Modularization

### When to extract a component or module
Extract when **any one** of these is true:
- The unit has a **single, nameable responsibility** that could be tested in isolation
- The same logic appears (or will appear) in **more than one place**
- The file exceeds **300 lines** — this is a signal, not a hard rule; investigate the SRP violation
- A collaborator reading the code would benefit from a named abstraction

Do **not** extract speculatively. Wait for a second usage or a clear boundary.

### Where code lives — respect the layer map
Every type of code has a **defined home** in `arch.md`. Before creating a file, ask:
- Is this **domain logic**? → domain layer (entities, value objects)
- Is this **application logic** (orchestration, use cases)? → services / use-case layer
- Is this **external dependency access** (API, DB, filesystem, auth)? → adapter layer
- Is this **UI presentation**? → component / view layer
- Is this **shared state**? → store layer
- Is this **reusable UI behavior**? → composable / hook layer

**Never create a file in the wrong layer.** If the layer map doesn't cover your case, update `arch.md` first — make it a conscious decision.

### Atomic Design for UI
When building UI components, follow the project's atomic hierarchy:
- **Atom**: single-purpose, no local state beyond display (Button, Input, Label)
- **Molecule**: combines atoms into a functional unit (SearchBar, FormField)
- **Organism**: self-contained feature section (Header, ProductCard, CommentThread)
- **Template**: layout structure with slots, no real data
- **Page / View**: wires template to real data via store/composable

Promote an atom to molecule only when composition is genuinely needed — not for cosmetic grouping.

### New enhancement vs. bug fix — different navigation protocols

**New enhancement:**
1. Identify the layer where the new behavior belongs
2. Create a **new file** for the new behavior (OCP — Open/Closed Principle)
3. Wire it into the existing structure without modifying working logic
4. Add test for the new behavior before marking done

**Bug fix:**
1. Reproduce the bug with a failing test first (if feasible)
2. Locate the **single file** responsible — resist the urge to fix adjacent issues
3. Fix only what's broken; commit the fix separately from any cleanup
4. Verify the test now passes; run regression suite

### The 300-line signal
A file approaching 300 lines is a **code smell detector**, not a formatter setting:
- Multiple `if/else` trees → Strategy Pattern (each branch = new file)
- Multiple unrelated methods → SRP violation (split into focused modules)
- Deeply nested logic → extract named functions
- Repeated setup code → extract shared fixture or factory

---

## §2 — Architecture Principles

### Dependency Rule (Clean Architecture)
Dependencies always point **inward only**:
```
Frameworks & Drivers
  → Interface Adapters
    → Application Logic
      → Domain / Entities
```
- Outer layers know about inner layers. Inner layers know nothing about outer layers.
- Framework APIs (Next.js, Vue Router, Firebase, Prisma) live **only** in the outermost layer (Interface Adapters / Frameworks).
- Domain logic must be framework-agnostic and independently testable.

### SOLID at module level
Apply these at file/module granularity — not just at class level:

| Principle | Practical rule |
|-----------|---------------|
| **SRP** | One file, one reason to change |
| **OCP** | New behavior = new file; don't modify working code to add features |
| **LSP** | Subtypes must be substitutable without breaking callers |
| **ISP** | Expose only what the caller needs; split fat interfaces |
| **DIP** | Depend on interfaces/abstractions, not concrete implementations |

### Isolate what can change
If an external dependency could be swapped, mocked in tests, or replaced in the future — encapsulate it. Scale the pattern to the complexity:

```
Simple module separation
  → Adapter (wraps one external concern)
    → Repository + Adapter (abstracts data access behind an interface)
      → Repository + Adapter + Facade (hides complexity of multiple dependencies)
```

Apply the **minimum pattern that solves the isolation problem**. Never apply Repository+Facade to a project with a single, stable data source.

### Third-party isolation
- No direct calls to third-party SDKs from domain or application layers
- All third-party integrations go through an adapter that the application layer consumes via interface
- This makes swapping vendors a single-file change

### File discipline
- **Naming**: Follow the conventions in `constitution.md` exactly. Do not invent naming styles.
- **Size limit**: Flag files over 300 lines for review before submitting
- **One export per file** (unless the file is an index barrel with explicit intent)

---

## §3 — Data Flow

### The cardinal rule
Data flow must be **unidirectional, explicit, and documented in `arch.md`**. Never improvise a shortcut between layers.

### Read the flow before writing code
`arch.md` defines the data flow chain for this project. Before implementing:
1. Trace the full path: from user interaction → through every layer → to data source → back
2. Identify exactly which files you'll touch
3. If a link in the chain doesn't exist yet, create it in the correct layer

### State = Single Source of Truth
- All shared state lives in one place (store, context, or server state manager)
- Components/views are **consumers** of state, not owners of derived duplicates
- Never copy state into local variables that won't be kept in sync
- Derived values are computed (memoized/computed properties), not stored

### Side effects are explicit
- Side effects (API calls, logging, cache writes) belong in the application layer or adapter — never in domain entities or pure UI components
- If a component needs a side effect, it delegates to a composable/hook/service

---

## §4 — Golden Rules for AI-Assisted Development
> **These are operational imperatives — execute them, do not interpret them.**

1. **Spec first, code second.** If no `spec.md` exists for a new feature, stop and ask the user. Do not infer requirements from vague descriptions.

2. **Read before you write.** Always read the files you'll modify before editing. Never patch code you haven't seen.

3. **One task at a time.** Implement one atomic task from `tasks.md` per cycle. Verify it works before starting the next.

4. **New behavior = new file (default).** Prefer creating a new file over modifying an existing one. Modify only when fixing a bug or when the behavior genuinely belongs to the existing unit.

5. **Never assume the stack.** Read `constitution.md`. The tech stack, allowed libraries, and forbidden patterns are defined there — not in your training data.

6. **Type everything.** No `any`, no implicit types, no type assertions without an inline comment explaining why it's necessary.

7. **Document non-obvious decisions.** Inline comment for anything that would surprise a reader. ADR for anything structural.

8. **Validate your own output before declaring done:**
   - Diff the changes — does this match the task?
   - Does it compile / pass linting?
   - Is there a test for the new behavior?
   - Does it violate any rule from `constitution.md`?

9. **Secrets never in code.** Environment variables, `.env` files, or secret managers only. If you see a hardcoded credential in existing code, flag it — don't copy the pattern.

10. **When blocked, say so explicitly.** Do not hallucinate a solution. State what's missing and ask.

---

## §5 — Code Quality Checklist
> **Run through this before marking any task complete. Each item is binary: pass or fail.**

### Typing
- [ ] Zero `any` types introduced
- [ ] Zero type assertions (`as SomeType`) without an inline justification comment
- [ ] All function signatures have explicit parameter and return types

### Structure
- [ ] No file exceeds 300 lines (flag, don't auto-fix without reviewing)
- [ ] Every new file is in the correct layer per `arch.md`
- [ ] Naming follows `constitution.md` conventions exactly
- [ ] No import crosses layer boundaries in the wrong direction

### Tests
- [ ] New behavior has at least one test covering the happy path
- [ ] Bug fix has a regression test that would have caught the original bug
- [ ] Existing tests still pass (run the suite)

### Security
- [ ] No hardcoded secrets, tokens, API keys, or passwords
- [ ] No credentials in `localStorage` (unless BYOK pattern explicitly approved in `constitution.md`)
- [ ] All user input that reaches an external system is validated

### Accessibility (UI only)
- [ ] All interactive elements have accessible labels (`aria-label`, `aria-labelledby`, or visible text)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Keyboard navigation works for all interactive flows

### Commits
- [ ] Follows Conventional Commits format (invoke `mjrp-conventional-commits` if unsure)
- [ ] Commit message references the task ID if applicable (`ref task-N`)

---

## §6 — Operational Mindset

### Logging
- Add **structured logs** (key-value pairs, not string concatenation) at the start of every new feature
- Log at appropriate levels: `debug` for internals, `info` for user-visible events, `warn` for recoverable issues, `error` for failures
- Never swallow errors silently (empty `catch` blocks are forbidden)

### Error handling
- Every `async` operation has explicit error handling
- Errors surface to the user with a useful message — not a raw stack trace
- Network errors and timeout scenarios have graceful degradation paths

### Caching
- Caching is an **explicit architectural decision**, not an ad-hoc optimization
- Document the cache strategy (what, where, TTL) in `arch.md` when introducing it
- Cache invalidation logic is tested

### Performance
- Measure before optimizing — no premature optimization
- Lazy load routes and heavy components by default
- Be aware of the infrastructure cost of what you build (queries, API calls, storage)

---

## §7 — Anti-patterns Catalog

### Project-specific (read from `constitution.md`)
Before starting, scan `constitution.md` for its explicit prohibition list. Apply it strictly.

### Universal anti-patterns to avoid

| Anti-pattern | Why it's harmful | Correct approach |
|---|---|---|
| **God Component / God Module** | One file does everything; impossible to test or modify safely | Extract by responsibility; apply SRP |
| **Prop Drilling** | Passes data through N layers of components that don't use it | Shared store or context |
| **Magic Numbers / Strings** | Undocumented constants in logic | Named constants in a dedicated config/constants file |
| **Direct Framework Calls in wrong layer** | Locks domain logic to a specific framework | Move to adapter; domain stays pure |
| **Implicit side effects in pure functions** | Hidden state mutation breaks predictability | Make side effects explicit and isolate them |
| **Copy-paste inheritance** | Duplicated logic that diverges over time | Extract shared abstraction |
| **Speculative generality** | Abstractions built for hypothetical future needs | YAGNI — build for what's needed now |
| **Shotgun surgery** | One change requires touching N unrelated files | Consolidate related behavior into a cohesive module |
| **Testing the implementation, not the behavior** | Tests break on refactors that don't change behavior | Test public contracts, not internals |
| **Skipping the spec** | Code written before requirements are clear | SDD: spec → plan → tasks → code |

---

## §8 — Completion Protocol

When a task is complete:

1. **Verify** — run through §5 checklist
2. **Test** — run the project's test suite; fix failures before proceeding
3. **Regression** — if the change touches existing behavior, invoke `mjrp-regression`
4. **Document** — update `tasks.md` to mark the task done; update inline docs
5. **Commit** — use `mjrp-conventional-commits`; reference task ID
6. **Log** — if bug fix, add entry to `docs/sessions/DEBUG_LOG.md`
7. **Request review** — surface the diff to the user with a one-line summary of what changed and why
