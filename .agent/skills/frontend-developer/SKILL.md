---
name: Frontend Developer
description: >
  Use when IMPLEMENTING frontend code: component architecture (atomic design,
  composition), performance optimization (Core Web Vitals, lazy loading, bundle
  size), responsive CSS implementation, state management patterns, consuming
  design tokens in code, and writing frontend tests (unit, component, visual
  regression, E2E). This skill owns HOW to build — not WHAT to build (see
  UX/UI Designer) or WHAT to test (see QA Engineer).
---

# Skill: Frontend Developer

**Purpose**: Teach an AI agent frontend development best practices — from component architecture to performance, ensuring code is maintainable, performant, and consistent with the design system.

**Related Workflows**: `sdd_task_protocol.md`, `code_quality_assessment_protocol.md`, `regression_protocol.md`

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

## 3. Responsive Implementation

### Strategy: Mobile-First CSS

```css
/* Base: Mobile (< 640px) */
.grid { display: flex; flex-direction: column; gap: 1rem; }

/* Tablet (>= 640px) */
@media (min-width: 640px) {
  .grid { flex-direction: row; flex-wrap: wrap; }
  .grid-item { flex: 0 0 calc(50% - 0.5rem); }
}

/* Desktop (>= 1024px) */
@media (min-width: 1024px) {
  .grid-item { flex: 0 0 calc(25% - 0.75rem); }
}
```

### Responsive Patterns
- **Fluid typography**: `clamp(1rem, 2.5vw, 1.5rem)` — scales smoothly
- **Container queries**: Use when component needs to respond to its own size, not viewport
- **Responsive images**: `<picture>` with `<source>` for art direction changes
- **Touch vs pointer**: `@media (hover: hover)` to detect mouse vs touch

### Testing
- Test on real devices when possible (not just browser DevTools)
- Minimum: 320px (small phone), 375px (iPhone), 768px (iPad), 1024px (laptop), 1440px (desktop)
- Test landscape orientation for tablets and phones

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

### Token Usage
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

---

## Scope & Boundaries

This skill owns frontend **implementation patterns**. Other skills own adjacent concerns:

```
"How should this page look/feel?"       → UX/UI Designer
"How do I build this component?"        → Frontend Developer (this skill)
"How do I create the design tokens?"    → Design System Documentation
"How do I consume tokens in CSS/code?"  → Frontend Developer (this skill)
"What should I test?"                   → QA Engineer
"How do I write this frontend test?"    → Frontend Developer (this skill)
"Is the app responsive enough?"         → UX/UI Designer (criteria) + Frontend Developer (implementation)
```

### Decision Tree

```
Need to decide layout, flow, or user experience?
  └─ YES → UX/UI Designer
Need to create or update design tokens?
  └─ YES → Design System Documentation
Need to implement a component, optimize performance, or write CSS?
  └─ YES → Frontend Developer
Need to decide responsive breakpoints and behavior?
  └─ Design criteria? → UX/UI Designer
  └─ CSS implementation? → Frontend Developer
Need to build for mobile app (not mobile web)?
  └─ YES → Mobile Developer
```

---

## When to Apply This Skill

- During **Plan** phase: Choose component architecture, define state management strategy
- During **Tasks** phase: Ensure tasks are decomposed following atomic design (data layer → atoms → molecules → organisms → pages)
- During **Implementation**: Follow performance checklist, use design tokens, write tests
- During **Review**: Validate Core Web Vitals, check responsiveness, run visual regression
