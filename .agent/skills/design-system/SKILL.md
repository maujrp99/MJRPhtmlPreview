---
name: Design System Documentation
description: >
  Use when creating, extracting, or maintaining the design-system.md artifact —
  the single source of truth for design tokens (colors, typography, spacing,
  shadows) and component documentation. Covers Greenfield creation, Brownfield
  extraction from existing CSS/UI, and consistency maintenance rules. This skill
  owns the ARTIFACT — not the design decisions (see UX/UI Designer) or the CSS
  implementation of tokens (see Frontend Developer).
---

# Skill: Design System Documentation

**Purpose**: Teach an AI agent how to create, extract, and maintain a design-system.md that bridges the gap between designers (Stitch/Figma) and developers (Claude Code/Antigravity).

**Related Workflows**: `documentation_protocol.md`, `sdd_plan_protocol.md`

---

## What is design-system.md?

A single markdown file in `docs/specs/` that codifies all visual decisions. It is the "constitution.md for UI" — any agent making UI decisions must consult it.

---

## 1. Creating from Scratch (Greenfield)

### Step 1: Define the Vibe
Start from VISION.md's "The Vibe" and "Design DNA" sections. Translate the aesthetic direction into concrete tokens.

### Step 2: Fill the Template

```markdown
# Design System: [Vibe Name]

## Color Palette
| Token | Hex | Usage |
|-------|-----|-------|
| --color-primary | #XXXXXX | Buttons, links, accents |
| --color-secondary | #XXXXXX | Backgrounds, cards |
| --color-bg | #XXXXXX | Main background |
| --color-text | #XXXXXX | Primary text |
| --color-text-secondary | #XXXXXX | Labels, meta info |
| --color-accent | #XXXXXX | Highlights, badges |
| --color-success | #XXXXXX | Positive states |
| --color-warning | #XXXXXX | Warning states |
| --color-error | #XXXXXX | Error states |

## Typography
| Element | Font | Weight | Size |
|---------|------|--------|------|
| H1 | [font] | Bold | 2.5rem |
| H2 | [font] | Bold | 2rem |
| H3 | [font] | Semibold | 1.5rem |
| Body | [font] | Regular | 1rem |
| Small | [font] | Regular | 0.875rem |
| Code | [monospace font] | Regular | 0.9rem |

## Spacing
- Base unit: [e.g., 8px]
- Grid: [e.g., 12 columns, 24px gap]
- Container max-width: [e.g., 1200px]
- Section padding: [e.g., 64px vertical]
- Card padding: [e.g., 24px]

## Border & Shape
- Border radius (cards): [e.g., 8px]
- Border radius (buttons): [e.g., 4px]
- Border radius (pills/tags): [e.g., 999px]
- Border color (subtle): [hex]

## Shadows
- Card shadow: [e.g., 0 2px 8px rgba(0,0,0,0.1)]
- Hover shadow: [e.g., 0 4px 16px rgba(0,0,0,0.15)]
- Modal shadow: [e.g., 0 8px 32px rgba(0,0,0,0.2)]

## Key Components
### Card
- Background: [color]
- Border: [style]
- Padding: [value]
- Hover behavior: [description]

### Navigation
- Style: [top bar / sidebar / both]
- Active state: [how indicated]
- Mobile behavior: [hamburger / bottom nav]

### Button
- Primary: [bg color, text color, border radius]
- Secondary: [outline style]
- Disabled: [opacity/color]

## Visual Reference
- Stitch Project: [link or ID]
- Reference Screen: [which screen is the "master" for the vibe]
```

---

## 2. Extracting from Existing UI (Brownfield)

### Sources to Extract From

| Source | What to Extract |
|--------|----------------|
| Stitch prototypes | Colors, fonts, spacing, component styles |
| Existing CSS/Tailwind config | Color variables, font stacks, spacing scale |
| Screenshots | Overall layout patterns, component styles |
| Stitch/Figma chat history | Design decisions and rationale |

### Extraction Process

1. **Screenshot the reference screen** — the one that best represents the vibe
2. **Identify colors**: Use a color picker (eyedropper) on the screenshot. Document primary, secondary, background, text colors.
3. **Identify fonts**: Check CSS `font-family` declarations or inspect the prototype.
4. **Identify spacing**: Measure padding and margins on key elements.
5. **Document components**: For each major UI element (card, nav, button), describe its visual properties.

### Tips for CSS Extraction
```bash
# Find all color definitions
grep -r "color:" src/ --include="*.css" --include="*.scss" --include="*.tsx"

# Find Tailwind config colors
cat tailwind.config.js | grep -A 20 "colors"

# Find font definitions
grep -r "font-family" src/ --include="*.css"
```

---

## 3. Maintaining the Design System

### When to Update
- After any "vibe" commit that changes visual patterns
- When a new component type is introduced
- When the Stitch prototype evolves
- After design review sessions

### Consistency Checks
- Does the implementation match design-system.md?
- Are there hardcoded colors/fonts that should use tokens?
- Do new components follow the established patterns?

### Anti-patterns
- ❌ Colors defined in code but not in design-system.md
- ❌ Multiple slightly-different grays (#666, #6B6B6B, #777) — consolidate
- ❌ Font sizes that don't match the scale
- ❌ design-system.md says one thing, code does another
- ✅ Every visual value traces back to a design token

---

## Scope & Boundaries

This skill owns the **design-system.md artifact** — the document itself:

```
"What colors/fonts/spacing should we use?"  → UX/UI Designer (decides) → Design System (documents)
"Create or update design-system.md"         → Design System Documentation (this skill)
"Use tokens in CSS variables or Tailwind"   → Frontend Developer (consumes)
"Extract tokens from existing Stitch/CSS"   → Design System Documentation (this skill)
```

### Decision Tree

```
Need to CREATE or UPDATE design-system.md?
  └─ YES → Design System Documentation
Need to DECIDE visual direction (which colors, which fonts)?
  └─ YES → UX/UI Designer
Need to IMPLEMENT tokens in code (CSS vars, Tailwind config)?
  └─ YES → Frontend Developer
```
