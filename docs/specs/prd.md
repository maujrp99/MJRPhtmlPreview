# PRD — MJRPhtmlPreview

> O que o produto **é**, para quem, com que objetivo, e **o que ele explicitamente não é**.
> Documento **vivo** — ao contrário do charter, que era um retrato do kickoff. Alimenta o
> [`story.md`](story.md); não o substitui.
>
> *Migrado do `docs/specs/prd.md` em 2026-09-15 pelo `charter_to_prd.py`, no retrofit do MJRP Harness.*
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

## Requisitos por épico

O backlog de produto — cada requisito é um nó: um arquivo em `docs/specs/requirements/<pasta do épico>/<ID>.md`, com
status, prioridade e arestas no frontmatter, nas seções `## pt-BR` e `## en` (kernel `requirements-graph`). Aqui fica o
mapa: cada épico declara a pasta dos seus requisitos (`folder::`) e o resultado do [`ROADMAP.md`](../../ROADMAP.md) que
serve (`serves::`), e embute os seus requisitos. Os épicos seguem os quatro objetivos de § *Objetivo e métricas*.

> **Migrado em 2026-10-05** do `story.md` (arquivado em `_archive/2026-10-05-story-md/story.md`): `US-NN` → `S-NN`,
> mesmo número. As features entregues estão em `docs/specs/features/` (F01 = M1–M3.5 + sessão 02/26 + M6, F02 = M4,
> F03 = M5).

### Transversais

**Não-funcionais** — valem para todas as features e não são importados por nenhuma: cada um é um arquivo
`docs/specs/requirements/nfr/NFR-xx.md` (vindos de `spec.md` §3 NFR01–NFR04; NFR05–NFR07 eram as stories S-07, S-08, S-09).

![[NFR-01]]

![[NFR-02]]

![[NFR-03]]

![[NFR-04]]

### EP-01 · Preview instantâneo
folder:: ep-01-instant-preview
serves:: [[ROADMAP#^OUT-01]] ^EP-01

![[S-01]]

![[S-07]]

![[S-08]]

![[S-09]]

![[S-10]]

![[S-11]]

### EP-02 · Salvar no Google Drive
folder:: ep-02-google-drive-save
serves:: [[ROADMAP#^OUT-02]] ^EP-02

![[S-03]]

![[S-06]]

### EP-03 · Salvar localmente e exportar
folder:: ep-03-local-save-and-export
serves:: [[ROADMAP#^OUT-03]] ^EP-03

![[S-02]]

![[S-04]]

![[S-05]]

### EP-04 · Edição de texto no preview
folder:: ep-04-inline-text-editing
serves:: [[ROADMAP#^OUT-04]] ^EP-04

![[S-12]]
