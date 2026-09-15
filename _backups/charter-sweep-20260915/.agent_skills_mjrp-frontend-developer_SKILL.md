---
name: mjrp-frontend-developer
description: >
  Use when IMPLEMENTING frontend code: component architecture (atomic design,
  composition), CSS mastery (layout, cascade, custom properties, animations,
  modern CSS), typography systems (type scale, fluid type, variable fonts,
  line-height, letter-spacing, web font loading, OpenType features),
  performance optimization (Core Web Vitals, lazy loading, bundle size),
  responsive and container query implementation, state management patterns,
  consuming design tokens, and writing frontend tests. Trigger on: "implement",
  "write the CSS", "fix the layout", "flexbox vs grid", "dark mode",
  "CSS animation", "specificity", "CSS architecture", "design token",
  "Tailwind vs CSS modules", "state management", "frontend test", "font size",
  "type scale", "line height", "letter spacing", "variable font", "web font",
  "typography". This skill owns HOW to build — not WHAT to build (see
  UX/UI Designer) or WHAT to test (see QA Engineer).
---

# Skill: Frontend Developer

**Purpose**: Guide an AI agent through frontend development best practices — from component architecture to CSS mastery to performance — ensuring code is maintainable, performant, and consistent with the design system.

**Related Workflows**: `mjrp-sdd-task`, `mjrp-code-quality-assessment-protocol.md`, `mjrp-regression-protocol.md`

---

## §0 — Pre-flight Protocol
> **STOP. Execute this checklist before writing a single line of code.**

- [ ] Read `VISION.md` — product direction and north star
- [ ] Read `CHARTER.md` — scope boundaries (what is and isn't in scope)
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

## 1. Component Architecture

### Atomic Design Hierarchy

```
Atoms → Molecules → Organisms → Templates → Pages

Atoms:       Button, Input, Label, Icon, Badge
Molecules:   SearchBar (Input + Button), FormField (Label + Input + Error)
Organisms:   Header (Logo + Nav + SearchBar), BookCard (Cover + Title + Author + Badge)
Templates:   PageLayout (Header + Main + Footer), GridLayout (FilterBar + CardGrid)
Pages:       BookshelfPage (PageLayout + GridLayout with data)
```

### Rules
- **Atoms and Molecules are dumb**: They receive props, render UI, emit events. No business logic, no API calls, no state management.
- **Organisms can be smart**: They may connect to stores or fetch data, but keep logic thin.
- **Pages are assemblers**: They compose organisms and handle routing/data loading.

### Prop Design
- Props should be **explicit and typed** (TypeScript interfaces or PropTypes)
- Avoid prop drilling > 2 levels — use Context, stores, or composition
- Use **slots/children** for layout flexibility instead of deeply configurable props
- Default props should produce a usable component (no required config for basic usage)

### Anti-patterns
- ❌ God Components: > 300 LOC, doing rendering + logic + API calls
- ❌ Prop drilling through 4+ levels
- ❌ Business logic in UI components (filtering, sorting, calculations)
- ❌ Direct DOM manipulation in framework components
- ✅ Composition over configuration: `<Card><CardHeader/><CardBody/></Card>` over `<Card headerTitle="..." bodyContent="...">`

---

## 2. Performance (Core Web Vitals)

### Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5-4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |

### Optimization Checklist

**Loading Performance**:
- [ ] Images: Use modern formats (WebP/AVIF), responsive `srcset`, lazy load below fold
- [ ] Fonts: `font-display: swap`, preload critical fonts, limit to 2-3 font files
- [ ] Code splitting: Route-based lazy loading (dynamic imports)
- [ ] Critical CSS: Inline above-the-fold styles, defer the rest
- [ ] Preload/prefetch: `<link rel="preload">` for critical resources

**Runtime Performance**:
- [ ] Memoize expensive computations (`useMemo`, `computed`, memoize pattern)
- [ ] Virtualize long lists (> 100 items): react-window, @tanstack/virtual
- [ ] Debounce/throttle scroll and resize handlers
- [ ] Avoid layout thrashing (batch DOM reads, then writes)
- [ ] Use `requestAnimationFrame` for animations, never `setInterval`

**Bundle Size**:
- [ ] Analyze with bundler visualizer (webpack-bundle-analyzer, vite-plugin-visualizer)
- [ ] Tree-shake unused exports
- [ ] Prefer lightweight alternatives (date-fns over moment, preact over react for simple apps)
- [ ] Lazy load heavy libraries (chart libs, rich editors)

---

## 3. CSS Mastery

CSS is a layout and painting engine, not just a styling language. Master it by understanding the cascade, the box model, and the rendering pipeline — then everything else follows.

### 3.1 Layout: Grid vs Flexbox

Use **Flexbox** for single-axis layouts (a row of buttons, a nav bar, a vertical stack). Use **Grid** for two-dimensional layouts (a card grid, a page shell, a form with labels + inputs aligned across rows).

```css
/* Flexbox: one axis — distribute items in a row */
.toolbar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* Grid: two axes — columns AND rows in sync */
.page-shell {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: 64px 1fr;
  grid-template-areas:
    "sidebar header"
    "sidebar main";
  min-height: 100vh;
}

/* Intrinsic responsive grid — no media queries needed */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
```

**Advanced Grid patterns**:
```css
/* Subgrid: let children align to parent grid tracks */
.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid; /* Chrome 117+, FF 71+ */
}

/* Named lines for readable placement */
.layout {
  grid-template-columns: [content-start] 1fr [content-end aside-start] 300px [aside-end];
}
```

### 3.2 The Cascade & Specificity

The cascade resolves conflicts in this order: **Origin** → **@layer** → **Specificity** → **Order**. Understanding this eliminates most "why won't my style apply?" bugs.

**Specificity score** (highest wins):
```
Inline style      1-0-0-0
ID selector       0-1-0-0
Class/attr/pseudo 0-0-1-0
Element/pseudo-el 0-0-0-1
```

**Control specificity with `@layer`** — layers resolve before specificity, giving you predictable override order:
```css
@layer reset, base, tokens, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; margin: 0; }
}

@layer components {
  .btn { background: var(--color-primary); }
}

@layer utilities {
  /* Utility classes always win over components — no !important needed */
  .bg-transparent { background: transparent; }
}
```

**Anti-patterns**:
- ❌ `!important` for specificity wars — use `@layer` instead
- ❌ Deep nesting (`nav ul li a span`) — creates fragile, hard-to-override selectors
- ❌ ID selectors in component CSS — IDs have unavoidable high specificity
- ✅ Keep selectors flat (1–2 levels max), rely on class names

### 3.3 CSS Architecture: Choosing Your Approach

| Approach | Best for | Downside |
|---|---|---|
| **CSS Modules** | React/Vue/Svelte, scoped by default | No global utilities without workaround |
| **Utility-first (Tailwind)** | Rapid UI, design system enforced via tokens | HTML gets verbose; complex states need `@apply` |
| **BEM** | Plain HTML/CSS, no build tooling | Verbose class names; discipline-dependent |
| **Scoped (Vue/Svelte)** | Single-file components | Leaks with deep selectors; global styles separate |
| **CSS-in-JS** | Dynamic runtime styles based on JS state | Runtime overhead; SSR complexity |

**Hybrid approach** (most practical for component-based apps):
- CSS custom properties for tokens (global, theming)
- CSS Modules or scoped styles for component encapsulation
- Utility classes for spacing/layout (thin utility layer via `@layer utilities`)

### 3.4 Custom Properties: Token Architecture & Theming

Custom properties (CSS variables) are the foundation of a maintainable design system. Structure them in semantic layers — primitive → semantic → component:

```css
/* Layer 1: Primitives — raw values, never used directly in components */
:root {
  --blue-500: #3b82f6;
  --blue-600: #2563eb;
  --gray-100: #f3f4f6;
  --gray-900: #111827;
  --space-4: 1rem;
  --space-6: 1.5rem;
}

/* Layer 2: Semantic tokens — named by intent, not color */
:root {
  --color-primary: var(--blue-500);
  --color-primary-hover: var(--blue-600);
  --color-bg: var(--gray-100);
  --color-text: var(--gray-900);
  --radius-card: 0.75rem;
  --shadow-card: 0 2px 8px rgb(0 0 0 / 0.08);
}

/* Layer 3: Dark mode — override semantic tokens only */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: var(--gray-900);
    --color-text: var(--gray-100);
  }
}

/* Class-based dark mode (for manual toggle) */
[data-theme="dark"] {
  --color-bg: var(--gray-900);
  --color-text: var(--gray-100);
}

/* Layer 4: Component tokens — scoped overrides via cascade */
.card {
  --card-padding: var(--space-6);
  --card-radius: var(--radius-card);
  padding: var(--card-padding);
  border-radius: var(--card-radius);
}

.card--compact {
  --card-padding: var(--space-4); /* Override only what changes */
}
```

**Power pattern — contextual theming via inheritance**:
```css
/* The sidebar inherits a different token set — all children adapt automatically */
.sidebar {
  --color-bg: #1e293b;
  --color-text: #e2e8f0;
  background: var(--color-bg);
  color: var(--color-text);
}
```

### 3.5 Responsive CSS & Modern Queries

**Mobile-first media queries** — base styles are mobile, scale up:
```css
.grid { display: flex; flex-direction: column; gap: 1rem; }

@media (min-width: 640px)  { .grid { flex-direction: row; flex-wrap: wrap; } }
@media (min-width: 1024px) { .grid { display: grid; grid-template-columns: repeat(3, 1fr); } }
```

**Fluid values with `clamp()`** — eliminate breakpoints for typography and spacing:
```css
/* font-size scales from 1rem (320px) to 1.5rem (1200px) without steps */
font-size: clamp(1rem, 0.5rem + 1.5vw, 1.5rem);

/* Fluid spacing */
padding: clamp(1rem, 3vw, 3rem);
```

**Container queries** — components respond to their container, not the viewport. Use when the same component renders in a sidebar (narrow) and a main area (wide):
```css
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card { flex-direction: row; }
  .card__image { width: 40%; }
}
```

**Modern selectors**:
```css
/* :has() — parent selector, style parent based on child state */
.form-group:has(input:invalid) { border-color: var(--color-error); }
.card:has(img) { padding-top: 0; } /* Cards with images: remove top padding */

/* Logical properties — writing-mode aware, better for i18n */
margin-inline: auto;        /* instead of margin-left + margin-right */
padding-block: 1rem;        /* instead of padding-top + padding-bottom */
inset-inline-start: 1rem;  /* instead of left: 1rem */
```

### 3.6 Animations & Transitions

**Rule**: only animate `transform` and `opacity`. Everything else (width, height, top, left, color) triggers layout or paint, causing jank. `transform` and `opacity` run on the compositor thread — silky smooth at 60fps.

```css
/* ✅ Compositor-only — no layout, no paint */
.modal {
  opacity: 0;
  transform: translateY(-8px) scale(0.97);
  transition: opacity 200ms ease, transform 200ms ease;
}
.modal.is-open {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* ❌ Triggers layout — forces full recalculate */
.panel { transition: height 300ms ease; }

/* Promote to compositor layer ONLY when you have a complex animation */
.heavy-animation {
  will-change: transform; /* Use sparingly — costs memory */
}
```

**Keyframe patterns**:
```css
@keyframes fade-slide-in {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}

.toast {
  animation: fade-slide-in 250ms ease forwards;
}

/* Stagger children with custom properties */
.item { animation-delay: calc(var(--index) * 50ms); }
```

**Respect user preferences — always**:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Scroll-driven animations (no JS needed)**:
```css
@keyframes reveal { from { opacity: 0; } to { opacity: 1; } }

.section {
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% entry 30%;
}
```

### 3.7 Modern Color

```css
/* oklch: perceptually uniform, great for accessible palettes */
:root {
  --color-primary: oklch(55% 0.2 264);        /* L C H */
  --color-primary-light: oklch(75% 0.15 264); /* Lighter, same hue */
}

/* color-mix: blend two colors */
.button:hover {
  background: color-mix(in oklch, var(--color-primary) 85%, white);
}

/* Relative color syntax */
.button-ghost {
  --alpha: 0.12;
  background: oklch(from var(--color-primary) l c h / var(--alpha));
}
```

### 3.8 CSS Debugging Checklist

When a style isn't applying or layout breaks:

1. **Specificity conflict?** — Open DevTools, inspect the element, check if the property is crossed out (overridden). Use `@layer` to fix.
2. **Stacking context issue?** (z-index not working) — An ancestor has `transform`, `opacity < 1`, `filter`, or `isolation: isolate`. Use `isolation: isolate` on the containing layer.
3. **Margin collapse?** — Vertical margins between block siblings collapse to the larger value. Fix: use `gap` on flex/grid parents, or `padding` instead of `margin`.
4. **Image causing CLS?** — Missing `width`/`height` attributes. Browser can't reserve space before load. Always set both.
5. **Custom property not inheriting?** — Check the element is a descendant of where the variable is defined. Use `@layer` ordering or `:root` for globals.
6. **Paint performance?** — Open DevTools → Rendering → Paint flashing. If large areas flash on interaction, you have a layout-triggering animation.

### 3.9 Typography System

Typography is a system, not a list of font sizes. Good type scales have internal logic — every size, weight, and spacing decision relates to the others.

**Type scale — modular ratio approach**:
Build your scale on a ratio (1.25 = Major Third, 1.333 = Perfect Fourth, 1.5 = Perfect Fifth). Each step multiplies the base by the ratio:

```css
:root {
  --text-base: 1rem;        /* 16px */

  /* Scale down (1 ÷ ratio) */
  --text-xs:   0.64rem;     /* 10.24px  — captions, labels */
  --text-sm:   0.8rem;      /* 12.8px   — secondary text */

  /* Scale up (base × ratio, Major Third 1.25×) */
  --text-md:   1rem;        /* 16px     — body */
  --text-lg:   1.25rem;     /* 20px     — lead text */
  --text-xl:   1.563rem;    /* 25px     — h4 */
  --text-2xl:  1.953rem;    /* 31px     — h3 */
  --text-3xl:  2.441rem;    /* 39px     — h2 */
  --text-4xl:  3.052rem;    /* 49px     — h1 */
}
```

**Fluid type scale — the whole scale adapts, not just one size**:
```css
/* Generate a fluid scale with clamp() — scales from 320px to 1200px viewport */
:root {
  --text-sm:  clamp(0.75rem,  0.68rem + 0.35vw,  0.875rem);
  --text-md:  clamp(1rem,     0.9rem  + 0.5vw,   1.125rem);
  --text-lg:  clamp(1.125rem, 0.95rem + 0.88vw,  1.375rem);
  --text-xl:  clamp(1.25rem,  1rem    + 1.25vw,  1.75rem);
  --text-2xl: clamp(1.5rem,   1.1rem  + 2vw,     2.25rem);
  --text-3xl: clamp(1.875rem, 1.2rem  + 3.38vw,  3rem);
  --text-4xl: clamp(2.25rem,  1.3rem  + 4.75vw,  4rem);
}
```

**Line-height and letter-spacing — the rules**:
```css
/* Line-height: larger text needs tighter leading; body text needs breathing room */
h1, h2    { line-height: 1.1; }   /* Tight — optical alignment for display text */
h3, h4    { line-height: 1.25; }
p, li     { line-height: 1.6; }   /* Comfortable reading — 1.5–1.7 for body */
caption   { line-height: 1.4; }

/* Letter-spacing: large headings look better tighter; small text often needs more air */
h1        { letter-spacing: -0.03em; }  /* Negative tracking for large display */
h2        { letter-spacing: -0.02em; }
body      { letter-spacing: 0; }        /* Default — don't touch */
.caption  { letter-spacing: 0.02em; }  /* Micro text benefits from positive tracking */
.overline { letter-spacing: 0.1em; }   /* ALL CAPS labels need wide tracking */
```

**`font-weight` — use the right weights, not just bold/normal**:
```css
:root {
  --weight-light:    300;
  --weight-regular:  400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;
}

/* Semantic roles */
body           { font-weight: var(--weight-regular); }
h1, h2, h3     { font-weight: var(--weight-bold); }
.label         { font-weight: var(--weight-medium); }
.button        { font-weight: var(--weight-semibold); }
.caption       { font-weight: var(--weight-regular); }
```

**Variable fonts — one file, full expressiveness**:
```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter.var.woff2') format('woff2');
  font-weight: 100 900;   /* Entire weight range from one file */
  font-style: normal;
  font-display: swap;
}

/* Use font-variation-settings for fine control */
.hero-title {
  font-variation-settings: 'wght' 750, 'opsz' 32; /* optical size axis */
}

/* With variable fonts, intermediate weights work perfectly */
.subtle-emphasis { font-weight: 450; }
```

**Web font loading — avoid CLS and FOUT**:
```css
/* 1. Preload in <head> (only the most critical font files) */
/* <link rel="preload" href="/fonts/Inter.var.woff2" as="font" type="font/woff2" crossorigin> */

/* 2. font-display: swap allows text to render immediately with fallback */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter.var.woff2') format('woff2');
  font-display: swap;
}

/* 3. size-adjust: match fallback font metrics to reduce CLS */
@font-face {
  font-family: 'Inter-Fallback';
  src: local('Arial');
  size-adjust: 107%;           /* Adjust until fallback matches web font metrics */
  ascent-override: 90%;
  descent-override: 22%;
}

body {
  font-family: 'Inter', 'Inter-Fallback', system-ui, sans-serif;
}
```

**System font stacks — when no custom font is loaded**:
```css
:root {
  /* System UI — native feel, zero loading cost */
  --font-system: system-ui, -apple-system, BlinkMacSystemFont,
                 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;

  /* Monospace — code blocks */
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code',
               ui-monospace, 'SF Mono', Menlo, monospace;

  /* Serif — editorial / long-form reading */
  --font-serif: 'Georgia', 'Cambria', 'Times New Roman', serif;
}
```

**OpenType features — polish the details**:
```css
/* Enable ligatures and contextual alternates for body text */
body {
  font-feature-settings: 'liga' 1, 'calt' 1;
  text-rendering: optimizeLegibility;
}

/* Oldstyle figures for running text (numbers blend with lowercase) */
.prose { font-feature-settings: 'onum' 1; }

/* Tabular (lining) figures for tables — numbers align in columns */
table { font-feature-settings: 'tnum' 1, 'lnum' 1; }

/* Small caps */
.overline { font-variant-caps: small-caps; }
```

**Measure (line length) — readability rule**:
```css
/* Optimal reading length: 45–75 characters per line */
.prose {
  max-width: 65ch;   /* ch = width of the '0' character — adapts to font size */
}

/* Tighter for UI text (labels, captions) */
.card-text { max-width: 40ch; }
```

**Text overflow patterns**:
```css
/* Single-line truncation */
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Multi-line clamp (no JS needed) */
.clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Balanced headlines — prevents awkward single-word last lines */
h1, h2, h3 { text-wrap: balance; }

/* Pretty wrapping for body text */
p { text-wrap: pretty; }
```

---

## 4. State Management

### Decision Framework

| Scope | Solution | Example |
|-------|----------|---------|
| **Local** (single component) | Component state (useState, ref) | Form input value, dropdown open/close |
| **Shared** (sibling components) | Lift state up or Context | Filter bar + results grid |
| **Feature-wide** (module) | Feature store (Zustand slice, Pinia module) | Shopping cart items |
| **Global** (app-wide) | Global store (Redux, Zustand, Pinia) | Auth state, theme, user preferences |
| **Server** (remote data) | Server state lib (TanStack Query, SWR) | API responses, caching, revalidation |

### Rules
- **Don't put everything in global state**: Most state is local or feature-scoped
- **Server state ≠ client state**: Use TanStack Query / SWR for API data, not Redux
- **Derive, don't duplicate**: If you can compute it from existing state, don't store it separately
- **Normalize when needed**: For relational data (entities with IDs), normalize to avoid stale copies

---

## 5. Design System Integration

### Consuming the Design System

When implementing UI, always check `docs/specs/design-system.md` first:

1. **Tokens first**: Use design tokens (colors, spacing, typography) — never hardcode values
2. **Existing components**: Check if a component already exists before creating a new one
3. **Variants, not forks**: If a component needs a slight variation, add a variant — don't copy-paste
4. **Document new components**: Any new reusable component gets added to design-system.md

```css
/* ❌ Hardcoded */
color: #1a73e8;
padding: 16px;
font-size: 14px;

/* ✅ Token-based */
color: var(--color-primary);
padding: var(--spacing-4);
font-size: var(--text-sm);
```

---

## 6. Frontend Testing

### Testing Pyramid (Frontend)

```
         ╱╲
        ╱ E2E ╲         Few: Critical user flows (login, checkout)
       ╱────────╲
      ╱Integration╲     Some: Component + store + API interactions
     ╱──────────────╲
    ╱   Unit Tests    ╲  Many: Pure functions, hooks, utilities
   ╱____________________╲
```

### What to Test

| Layer | What | Tool Examples |
|-------|------|---------------|
| **Unit** | Utils, hooks, pure logic, formatters | Vitest, Jest |
| **Component** | Rendering, props, events, states | Testing Library, Vitest |
| **Integration** | Feature flows, store interactions | Testing Library + MSW |
| **Visual** | UI regressions, design consistency | Chromatic, Percy, Playwright screenshots |
| **E2E** | Full user journeys | Playwright, Cypress |

### Testing Rules
- Test **behavior**, not implementation ("user sees error message" not "setState was called")
- Mock APIs at the network level (MSW), not at the module level
- Visual regression tests for any component with design system tokens
- E2E for every critical user path (the ones that lose money or users if broken)

---

## Scope & Boundaries

```
"How should this page look/feel?"       → UX/UI Designer
"How do I build this component?"        → Frontend Developer (this skill)
"How do I create the design tokens?"    → Design System Documentation
"How do I consume tokens in CSS/code?"  → Frontend Developer (this skill)
"What should I test?"                   → QA Engineer
"How do I write this frontend test?"    → Frontend Developer (this skill)
"Is the app responsive enough?"         → UX/UI Designer (criteria) + Frontend Developer (implementation)
"CSS layout / specificity / animation?" → Frontend Developer (this skill)
```

### Decision Tree

```
Need to decide layout, flow, or user experience?
  └─ YES → UX/UI Designer
Need to create or update design tokens?
  └─ YES → Design System Documentation
Need to implement a component, write CSS, optimize performance?
  └─ YES → Frontend Developer
Need to debug a CSS issue (z-index, specificity, layout, animation)?
  └─ YES → Frontend Developer
Need to build for mobile app (not mobile web)?
  └─ YES → Mobile Developer
```

---

## When to Apply This Skill

- During **Plan** phase: Choose component architecture, CSS approach, define state management strategy
- During **Tasks** phase: Decompose following atomic design (tokens → atoms → molecules → organisms → pages)
- During **Implementation**: Follow CSS architecture, use tokens, performance checklist, write tests
- During **Review**: Validate Core Web Vitals, check responsiveness, audit cascade/specificity, run visual regression
