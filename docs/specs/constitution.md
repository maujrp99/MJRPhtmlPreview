# Project Constitution — MJRPhtmlPreview

## 1. Technical Stack
- **Frontend**: Vanilla HTML + CSS + JavaScript (single file SPA)
- **Styling**: Custom CSS — Vibe: Minimal Dark (#0d1117 background, #58a6ff cyan accent, #3fb950 green accent)
- **Typography**: JetBrains Mono (code/textarea), Inter (UI labels)
- **Backend**: None (fully client-side)
- **APIs**: Google OAuth2, Google Drive API v3, Google Picker API
- **Hosting**: GitHub Pages or local file (no server required for MVP)

## 2. Development Methodology (SDD)
- Flow: Specify -> Plan -> Tasks -> Implement
- No implementation without a defined Task in tasks.md
- Iteration via Kanban per feature (M1 → M2 → M3)
- Pre-SDD phases: Discovery → Design (for each milestone)

## 3. SCM & Governance
- Branching: main (stable), dev (integration)
- Commits: Conventional Commits (feat, fix, docs, refactor, vibe, chore)
- Review: Every implementation validated against story.md

## 4. AI Orchestration
- Claude Cowork: Strategy, specs, brainstorming, analysis
- Claude Code: Terminal implementation, refactoring, tests, git ops
- Antigravity: Code implementation, code review, Git ops via GitHub
- Always check this file before suggesting packages or patterns
- No external dependencies unless absolutely necessary (vanilla-first philosophy)

## 5. Design System Reference
- Consult design-system.md for visual decisions
- Never deviate from the Minimal Dark palette
- Accessibility: WCAG AA contrast ratios on dark backgrounds

## 6. Key Constraints
- Single HTML file for MVP (inline CSS + JS)
- No build tools for M1 (may add for M2/M3 if needed)
- Google API credentials managed via .env (never committed)
- Must work with both personal and professional Google accounts
