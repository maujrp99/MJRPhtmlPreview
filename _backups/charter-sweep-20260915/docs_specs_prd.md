# PRD — MJRPhtmlPreview

> O que o produto **é**, para quem, com que objetivo, e **o que ele explicitamente não é**.
> Documento **vivo** — ao contrário do charter, que era um retrato do kickoff. Alimenta o
> [`story.md`](story.md); não o substitui.
>
> *Migrado do `CHARTER.md` em 2026-09-15 pelo `charter_to_prd.py`, no retrofit do MJRP Harness.*
> *De onde veio cada parte: *Justification (Business Case)* → Contexto e encaixe estratégico · *Main Goals and Success Metrics* → Objetivo e métricas · *High-Level Scope* → Requisitos · *Main Stakeholders* → Papéis e ferramentas · *Risks and Constraints* → Premissas e questões em aberto · *AI Tooling* → Papéis e ferramentas.*
> *O conteúdo foi **movido, não reescrito** — se alguma frase envelheceu, o lugar de*
> *corrigir é aqui, porque agora este documento é o vivo.*

## Objetivo e métricas

- **Goal 1**: Load or paste HTML → see rendered preview in < 1 second
- **Goal 2**: Save to Google Drive with folder picker in < 3 clicks
- **Goal 3**: Save locally (download .html) for Obsidian vault in 1 click
- **Goal 4**: Select and edit any text directly in the preview without touching HTML code
- **Success metric**: Daily personal use without friction

## Contexto e encaixe estratégico

AI-generated HTML (from Cowork, Claude Code, ChatGPT, etc.) needs to be previewed and archived. Currently there's no streamlined way to go from "clipboard HTML" to "organized file in Drive/vault." This tool closes that gap for personal productivity.

## Requisitos

### In Scope
- HTML paste area with syntax highlighting (optional)
- **File picker to load .html/.htm/.md files from disk** (M5)
- Real-time iframe preview
- **Inline text editing in preview** — select any text and edit in-place (M5)
- Google OAuth2 authentication (personal + professional accounts)
- Google Drive save with folder picker (Google Picker API)
- Local download as .html file
- Export to PDF (native print) and PNG (html2canvas)
- BYOK (Bring Your Own Keys) — credenciais Google salvas no localStorage do browser
- Fullscreen Preview mode (toggle para esconder editor)
- Base Href injection para resolução de imagens relativas
- Responsive layout (desktop-first, mobile-friendly)
- Markdown rendering via marked.js (M4)
- Mermaid diagram rendering via mermaid.js (M4)

### Out of Scope
- Full HTML/IDE editing (adding/removing elements, changing styles, drag & drop — this is a viewer with light text editing, not a CMS)
- Backend/server (fully client-side)
- User accounts or databases
- CSS/JS separate file support (single HTML only)
- Collaboration features

## Papéis e ferramentas

### Main Stakeholders

- **User**: Pedroso (sole user, personal tool)
- **Builder**: Claude Cowork + Claude Code + Antigravity

### AI Tooling

| Tool | Role | When |
|------|------|------|
| Claude Cowork | Strategy, specs, brainstorming | Discovery, Design, Specify |
| Claude Code | Implementation | Plan, Tasks, Implement |
| Antigravity | Code review, Git ops | Implement, Review |

## Premissas e questões em aberto

- **Google OAuth2 setup**: Requires Google Cloud Console project with Drive API and Picker API enabled. User must configure OAuth credentials.
- **CORS/iframe restrictions**: Some HTML content may not render in sandboxed iframes. Mitigation: use `srcdoc` attribute.
- **Single user**: No need for multi-tenant considerations, but OAuth must support multiple Google accounts (personal + work).

## Fora de escopo

*Extraia do § Requisitos acima o que o charter marcava como fora — o texto original os
trazia juntos, e separá-los é julgamento, não mecânica.*

## Stories

O backlog de produto mora em [`story.md`](story.md); os milestones, no
[`ROADMAP.md`](../../ROADMAP.md).
