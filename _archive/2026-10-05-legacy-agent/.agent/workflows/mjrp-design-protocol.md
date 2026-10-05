---
description: Design Protocol — UX/UI prototyping and architectural strategy using Stitch, mjrp-ux-ui-designer, and mjrp-system-architect.
---

# Design Protocol

**Purpose**: To bridge the gap between Discovery (the "What") and SDD Implementation (the "How-to-code"). This workflow focuses on the visual and structural architecture required before writing any code.

## 1. When to Trigger
- After Discovery completes and a new Epic/Story is selected for the active Milestone.
- Before coding any new major UI components or views.
- When new backend architecture (Data Models, APIs) must support the UI.

## 2. Participating Skills & Tools
- **`mjrp-ux-ui-designer`**: Owns the usability heuristics, accessibility, wireframes, and UX flow.
- **`mjrp-system-architect`**: Ensures the design can be supported cleanly by the architecture (`arch.md`, `data-model.md`).
- **`StitchMCP` (Tool)**: Generates high-fidelity UI mockups and HTML for visual approval.

## 3. Workflow Steps

### Phase 1: UX Strategy (`mjrp-ux-ui-designer`)
1. **Analyze Requirements**: Review the User Story and Acceptance Criteria in `docs/specs/story.md`.
2. **Define Flow & Heuristics**: Determine the user journey, states (loading, error, empty), and accessibility constraints.
3. **Draft UI Constraints**: Provide layout and interaction instructions tailored to the project's visual identity (e.g., Organic Blueprint).

### Phase 2: Architectural Feasibility (`mjrp-system-architect`)
1. **Data Model Check**: Does `docs/specs/data-model.md` support the proposed UX? If not, propose data structure changes.
2. **Layer Boundaries**: Ensure the UX doesn't force a layer violation (e.g., frontend directly mutating local files bypassing Vault APIs).

### Phase 3: High-Fidelity Prototyping (`StitchMCP`)
1. **Generate Mockup**: Combine UX instructions and visual identity to prompt StitchMCP.
   - Example prompt: "Generate an interface for [User Story] applying the [Vibe] style. Background: [Color]. Headings: [Typography]."
2. **Save & Review**: Output HTML files locally (e.g., `stitch-component.html`) and ask the User to review it in their browser.
3. **Iterate**: Adjust based on user feedback until the "Source of Truth" visual is approved.

### Phase 4: Documentation Update
1. **Log the Output**: Add the approved Stitch IDs and HTML references to `docs/specs/design-reference.md` or `design-system.md`.
2. **Mark Ready**: Change the story status in `story.md` to `Ready (Design Approved)`.

## 4. Exit Criteria
- A concrete visual reference exists and is approved by the user.
- Architecture and data models are confirmed to support the design.
- The next step is a clear hand-off to Implementation via `.agent/workflows/mjrp-sdd-protocol.md` (Specify & Plan).
