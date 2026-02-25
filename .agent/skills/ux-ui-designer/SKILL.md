---
name: UX/UI Designer
description: >
  Use when deciding HOW something should look, feel, or behave from the user's
  perspective: usability heuristics (Nielsen), accessibility standards (WCAG 2.1),
  mobile-first design thinking, information architecture, user flows, wireframing
  with ASCII mockups, and when to escalate to Stitch/Figma. This skill owns the
  WHAT and WHY of UI — not the HOW of CSS/code (see Frontend Developer) or the
  token definitions (see Design System Documentation).
---

# Skill: UX/UI Designer

**Purpose**: Teach an AI agent how to approach problems from a UX/UI perspective — prioritizing the user's experience, accessibility, and visual consistency before jumping into code.

**Related Workflows**: `sdd_specify_protocol.md`, `sdd_plan_protocol.md`, `documentation_protocol.md`

---

## Core Mindset

Before writing any code or spec, the UX/UI Designer asks:

1. **Who** is the user? (persona, context, device, ability level)
2. **What** is their goal? (not the feature — the underlying need)
3. **Where** are they coming from? (previous screen, mental model, expectations)
4. **What could go wrong?** (error states, edge cases, accessibility barriers)

---

## 1. Usability Heuristics (Nielsen's 10)

Apply these as a checklist when reviewing any UI spec or implementation:

| # | Heuristic | Quick Test |
|---|-----------|------------|
| 1 | Visibility of system status | Does the user always know what's happening? (loading states, progress indicators) |
| 2 | Match between system and real world | Does the UI use the user's language, not developer jargon? |
| 3 | User control and freedom | Can the user undo, go back, or escape easily? |
| 4 | Consistency and standards | Do similar actions look and behave the same way? |
| 5 | Error prevention | Does the design prevent errors before they happen? (disabled buttons, validation) |
| 6 | Recognition over recall | Is information visible, not hidden behind memory? (labels, tooltips, breadcrumbs) |
| 7 | Flexibility and efficiency | Are there shortcuts for expert users without confusing beginners? |
| 8 | Aesthetic and minimalist design | Is every element necessary? Remove what doesn't serve the user's goal. |
| 9 | Help users recognize and recover from errors | Are error messages clear, specific, and actionable? |
| 10 | Help and documentation | Is help available in context, not buried in a manual? |

---

## 2. Accessibility (WCAG 2.1)

### Minimum Requirements (Level AA)

**Perceivable**:
- All images have meaningful `alt` text (not "image1.png")
- Color contrast ratio: at least **4.5:1** for normal text, **3:1** for large text
- Don't rely on color alone to convey information (add icons, patterns, or text)
- Provide captions or transcripts for audio/video content

**Operable**:
- All interactive elements reachable via **keyboard** (Tab, Enter, Escape, Arrow keys)
- Focus indicators visible (never `outline: none` without replacement)
- No content that flashes more than 3 times per second
- Skip navigation link for screen readers
- Touch targets: minimum **44x44px**

**Understandable**:
- Language attribute set on `<html>` element
- Form fields have associated `<label>` elements
- Error messages appear near the relevant field, not just at the top
- Consistent navigation across pages

**Robust**:
- Valid semantic HTML (use `<button>` not `<div onclick>`)
- ARIA roles only when native HTML isn't sufficient
- Test with screen reader (VoiceOver, NVDA) at least once per major feature

### Quick Accessibility Audit

```
[ ] Keyboard-only navigation works for all flows
[ ] Screen reader announces all interactive elements correctly
[ ] Color contrast passes (use browser DevTools or WebAIM checker)
[ ] All form fields have labels
[ ] Error states are announced to assistive technology
[ ] Images have descriptive alt text
[ ] Focus order follows visual layout
```

---

## 3. Mobile-First Design

### The Principle
Design for the smallest screen first, then enhance for larger screens. This forces prioritization — what truly matters?

### Process
1. **Content inventory**: List everything the screen needs to show
2. **Priority stack**: Rank by user importance (not developer convenience)
3. **Mobile layout**: Stack content vertically, one column, most important first
4. **Tablet enhancement**: Add side-by-side where it helps comprehension
5. **Desktop enhancement**: Use extra space for context, shortcuts, multi-column

### Responsive Breakpoints (suggestion)
```
Mobile:   < 640px   (1 column, stacked, touch-optimized)
Tablet:   640-1024px (2 columns where useful)
Desktop:  > 1024px   (full layout, optional sidebar)
```

### Anti-patterns
- ❌ Designing desktop-first and "squishing" it for mobile
- ❌ Hiding essential content on mobile ("they'll use desktop for that")
- ❌ Horizontal scrolling on mobile
- ❌ Tiny tap targets (links, buttons < 44px)
- ✅ Progressive disclosure: show summary on mobile, expand on desktop

---

## 4. Information Architecture

### Card Sorting Exercise
When organizing navigation or content structure:
1. List all pages/sections on "cards"
2. Group by user mental model (not by technical module)
3. Name groups using user language
4. Validate: "Would a new user find X in Y seconds?"

### Navigation Patterns
- **< 5 items**: Tab bar (mobile) or horizontal nav (desktop)
- **5-10 items**: Hamburger menu with clear categories
- **> 10 items**: Search + categories + filters
- **Deep hierarchy**: Breadcrumbs + sidebar tree

---

## 5. User Flows

### Template for Documenting Flows

```markdown
## Flow: [Name] (e.g., "Book Discovery")

**Entry point**: [Where does the user start?]
**Goal**: [What does the user want to accomplish?]
**Happy path**:
1. User lands on [page] → sees [content]
2. User [action] → system responds with [feedback]
3. User [action] → system [result]
4. **Success state**: [What the user sees when done]

**Error paths**:
- If [condition]: Show [error message] → Allow [recovery action]
- If [condition]: Redirect to [fallback]

**Edge cases**:
- Empty state: [What shows when there's no data?]
- Loading state: [Skeleton? Spinner? Progressive load?]
- Offline state: [Cached data? Error message?]
```

---

## 6. Wireframing with ASCII Mockups

ASCII mockups are surprisingly effective for AI-to-AI communication. Use them in plan.md:

```
┌──────────────────────────────────────┐
│  [Logo]   Home | Library | About     │
├──────────────────────────────────────┤
│                                      │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐       │
│  │ 📖 │ │ 📖 │ │ 📖 │ │ 📖 │       │
│  │    │ │    │ │    │ │    │       │
│  └────┘ └────┘ └────┘ └────┘       │
│  Title   Title   Title   Title      │
│  Author  Author  Author  Author     │
│                                      │
│  [< Prev]  Page 1 of 5  [Next >]   │
├──────────────────────────────────────┤
│  Filter: [All ▼] Sort: [Recent ▼]  │
└──────────────────────────────────────┘
```

### When to Escalate to Stitch/Figma
- When visual direction is ambiguous (multiple valid approaches)
- When the client/stakeholder needs to see "real" visuals
- When testing color palettes, typography, or illustration styles
- When building a design system from scratch

### When ASCII is Enough
- Internal features with established design system
- Developer-to-developer communication
- Rapid iteration during spec phase
- Layout and flow validation (before polish)

---

## 7. Documenting UI Decisions in design-system.md

Every UI decision that affects consistency should be captured:

```markdown
### Component: [Name]

**Purpose**: [Why this component exists]
**Variants**: [Primary, Secondary, Danger, Ghost]
**States**: [Default, Hover, Active, Disabled, Loading, Error]
**Responsive behavior**: [How it adapts across breakpoints]
**Accessibility**: [ARIA role, keyboard interaction, screen reader behavior]

**Do**:
- Use Primary for the main action per screen
- Use Ghost for tertiary actions

**Don't**:
- Don't use more than one Primary button per view
- Don't use color alone to distinguish variants
```

---

---

## Scope & Boundaries

This skill owns the **user experience perspective** — how things should look, feel, and behave. Other skills own implementation:

```
"How should this page be organized?"        → UX/UI Designer (this skill)
"How do I implement this layout in CSS?"    → Frontend Developer
"What are the design tokens (colors, etc)?" → Design System Documentation
"Is this accessible to screen readers?"     → UX/UI Designer (criteria) + Frontend Developer (implementation)
"What should we test for this feature?"     → QA Engineer
"How should this adapt on mobile apps?"     → Mobile Developer
```

### Decision Tree

```
Deciding what the user sees, feels, or how they navigate?
  └─ YES → UX/UI Designer
Defining reusable tokens (colors, spacing, typography)?
  └─ YES → Design System Documentation
Implementing the UI in code (HTML, CSS, components)?
  └─ YES → Frontend Developer
Building for a native mobile app?
  └─ YES → Mobile Developer (uses UX/UI principles but with mobile-specific patterns)
Evaluating if an existing UI meets quality standards?
  └─ Usability & accessibility? → UX/UI Designer
  └─ Code architecture? → Code Quality & Architecture Assessment
```

---

## When to Apply This Skill

- During **Specify** phase: Write user stories with UX perspective, define edge cases and error states
- During **Plan** phase: Create wireframes, define responsive behavior, document component states
- During **Review**: Validate implementation against accessibility checklist and usability heuristics
- When the human asks: "How should this look/work/feel?"
