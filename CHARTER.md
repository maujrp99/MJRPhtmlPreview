# MJRPhtmlPreview — Charter

## Title and Description
**MJRPhtmlPreview** — A client-side web application for previewing HTML code and saving it to Google Drive or locally (Obsidian vault). Single-page app, no backend, zero dependencies beyond Google APIs.

## Justification (Business Case)
AI-generated HTML (from Cowork, Claude Code, ChatGPT, etc.) needs to be previewed and archived. Currently there's no streamlined way to go from "clipboard HTML" to "organized file in Drive/vault." This tool closes that gap for personal productivity.

## Main Goals and Success Metrics
- **Goal 1**: Paste HTML → see rendered preview in < 1 second
- **Goal 2**: Save to Google Drive with folder picker in < 3 clicks
- **Goal 3**: Save locally (download .html) for Obsidian vault in 1 click
- **Success metric**: Daily personal use without friction

## High-Level Scope

### In Scope
- HTML paste area with syntax highlighting (optional)
- Real-time iframe preview
- Google OAuth2 authentication (personal + professional accounts)
- Google Drive save with folder picker (Google Picker API)
- Local download as .html file
- Responsive layout (desktop-first, mobile-friendly)

### Out of Scope
- HTML editing/IDE features (this is a viewer, not an editor)
- Backend/server (fully client-side)
- User accounts or databases
- CSS/JS separate file support (single HTML only)
- Collaboration features

## Main Stakeholders
- **User**: Pedroso (sole user, personal tool)
- **Builder**: Claude Cowork + Claude Code + Antigravity

## Roadmap (Milestones)
| Milestone | Target | Description |
|-----------|--------|-------------|
| M1: MVP | Week 1 | Paste + Preview + Local Save |
| M2: Drive Integration | Week 2 | OAuth2 + Picker + Drive Save |
| M3: Polish | Week 3 | UX refinements, keyboard shortcuts, mobile |

## Risks and Constraints
- **Google OAuth2 setup**: Requires Google Cloud Console project with Drive API and Picker API enabled. User must configure OAuth credentials.
- **CORS/iframe restrictions**: Some HTML content may not render in sandboxed iframes. Mitigation: use `srcdoc` attribute.
- **Single user**: No need for multi-tenant considerations, but OAuth must support multiple Google accounts (personal + work).

## AI Tooling
| Tool | Role | When |
|------|------|------|
| Claude Cowork | Strategy, specs, brainstorming | Discovery, Design, Specify |
| Claude Code | Implementation | Plan, Tasks, Implement |
| Antigravity | Code review, Git ops | Implement, Review |
