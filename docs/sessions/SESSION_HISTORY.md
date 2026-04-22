# MJRPhtmlPreview — Session History

---

## Session: 2026-04-21 — M5: Load & Edit Implementation

> Data: 2026-04-21
> Participantes: Pedroso + Antigravity
> Branch: dev (merged to main)
> Duração: ~1 hora

### Resumo Executivo
Implementação ponta-a-ponta do Milestone 5 (M5: Load & Edit) via SDD Protocol. Adição de capacidade de carregamento de arquivos locais (HTML/Markdown) com File Picker nativo (`#btnOpen`). Implementação de "Edit Mode" injetando `contentEditable=true` no iframe para edições textuais WYSIWYG, suportando Sync estrutural (`outerHTML` extraction) para evitar perdas de CSS (bug fix). O botão "Local" foi otimizado para usar o gerador de Dialog Nativo (File System Access API). Código aprovado e preparado na `main` para GH Pages.

### Decisões Tomadas
- **Serialization Strategy**: Mudança de sync da raiz `innerHTML` de `body` para `documentElement.outerHTML` para não remover tags meta, `<style>` nem script do `<head>` na saída do modo edição.
- **UX Markdown Alert**: Markdown cru vira permanentemente HTML se o usuário testar a visibilidade no edit e salvar, exigindo um `confirm()` preventivo na UI.
- **Deploy OOB Dialog**: Ao invés de autosave, o app agora invoca o `window.showSaveFilePicker` nativo do MacOS/Chrome sempre que possível.
- **Cancel Edit**: Ao lado do "Save Edits", implementado o botão `❌ Cancel` que recarrega instantaneamente a RAM local descartando a edição sem persistência suja.

### Artefatos Gerados/Modificados
| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `docs/specs/m5/*` | Atualizado | Completação do SDD M5 (Spec/Plan/Tasks DONE) |
| `index.html` | Atualizado | Novos botões na toolbar (File Picker, Edit, Cancel) |
| `js/app.js` | Atualizado | Lógica de carregamento de files locais `FileReader` |
| `js/preview.js` | Atualizado | Lógica de Edição Visual Inline e preservação de head |
| `js/export.js` | Atualizado | Add API Modern Save Native |
| `story.md` / `CHARTER.md` | Atualizado | Marcação de Milestones concluídas |

### Pendências para Próxima Sessão
1. Confirmar fechamento do roadmap / migrar de Active-Feature-Development para Manutenção.
2. Explorar (se necessário) componentização com Vite caso a base se expanda (hoje é Single HTML File Vanilla).

### Dados-Chave
- File System Access API demanda HTTPS ou localhost (Chrome).
- Base tags re-injetadas pelo preview script são devidamente depuradas pelo engine de serialização DOM no exit mode.

---

## Session 1: Project Bootstrap

> Date: 2025-02-25
> Participants: Pedroso + Claude Cowork
> Branch: main (pre-commit — git init done, lock file needs manual cleanup)

### Executive Summary
Brainstormed and bootstrapped the MJRPhtmlPreview project from zero using the MJRP Greenfield Flow. Created full folder structure, all baseline docs (VISION, CHARTER, README), complete SpecKit with constitution.md and placeholders, design-system initial tokens, and AI tool configs (.claudeprompt, GEMINI.md). Also created the `mjrp-project-setup` skill for the MJRP framework itself during this session.

### Decisions Made

1. **Project Name**: MJRPhtmlPreview
2. **Architecture**: Client-side SPA, single HTML file (vanilla JS/CSS), no backend, no build tools for MVP
3. **Vibe**: Minimal Dark — #0d1117 background, #58a6ff cyan accent, #3fb950 green accent, JetBrains Mono + Inter typography
4. **Core Features**:
   - Textarea to paste HTML
   - Real-time iframe preview (using `srcdoc`)
   - Save to Google Drive via OAuth2 + Picker API (folder selection)
   - Local download as .html (for Obsidian vault)
5. **OAuth Strategy**: Support both personal and professional Google accounts
6. **AI Tooling**: Cowork (strategy/specs) + Claude Code (implementation) + Antigravity (code review/Git)
7. **Milestones**: M1 (MVP: paste+preview+local save) → M2 (Drive integration) → M3 (polish)
8. **Hosting**: GitHub Pages (or local file for MVP)
9. **Framework Enhancement**: Updated MJRP lifecycle to include Discovery → Design → SDD (not just SDD alone). Created `environment_setup_protocol.md` as new workflow.

### Artifacts Generated

| Artifact | Path | Status |
|----------|------|--------|
| VISION.md | `/VISION.md` | Complete |
| CHARTER.md | `/CHARTER.md` | Complete |
| README.md | `/README.md` | Complete |
| .gitignore | `/.gitignore` | Complete |
| .claudeprompt | `/.claudeprompt` | Complete |
| GEMINI.md | `/GEMINI.md` | Complete |
| constitution.md | `/docs/specs/constitution.md` | Complete |
| design-system.md | `/docs/specs/design-system.md` | Initial tokens |
| story.md | `/docs/specs/story.md` | Placeholder |
| spec.md | `/docs/specs/spec.md` | Placeholder |
| arch.md | `/docs/specs/arch.md` | Placeholder |
| data-model.md | `/docs/specs/data-model.md` | Placeholder |
| plan.md | `/docs/specs/plan.md` | Placeholder |
| tasks.md | `/docs/specs/tasks.md` | Placeholder |
| SESSION_HISTORY.md | `/docs/sessions/SESSION_HISTORY.md` | This file |

### Also Created This Session (in CintVibe, not in this repo)

| Artifact | Path (CintVibe) | Description |
|----------|-----------------|-------------|
| mjrp-project-setup.skill | `.skills-dev/for-claude/mjrp-project-setup.skill` | Packaged skill for Claude |
| Antigravity skill | `.skills-dev/for-antigravity/.agent/skills/mjrp-project-setup/` | Skill in Antigravity format |
| environment_setup_protocol.md | `.skills-dev/mjrp-project-setup/references/environment_setup_protocol.md` | New workflow |

### Pending for Next Session

**IMMEDIATE — Before anything else:**
1. Remove `.git/index.lock` manually: `rm /Users/mpedroso/0.MyPetProjects/MJRPhtmlPreview/.git/index.lock`
2. Set git config (if not global): `git config user.email "mpedroso@ciandt.com" && git config user.name "Pedroso"`
3. Run the commit sequence:
   ```bash
   cd /Users/mpedroso/0.MyPetProjects/MJRPhtmlPreview
   git add .gitignore
   git commit -m "chore: project scaffold"
   git add VISION.md CHARTER.md README.md
   git commit -m "docs: initial vision and charter"
   git add docs/
   git commit -m "chore: folder structure and SpecKit placeholders"
   git add docs/specs/constitution.md docs/specs/design-system.md
   git commit -m "docs: project constitution and design system"
   git add .claudeprompt GEMINI.md
   git commit -m "chore: AI config"
   ```

**NEXT PHASE — Environment Setup (Step 6):**
4. Create GitHub repo: `gh repo create MJRPhtmlPreview --private --source=. --push`
5. Create dev branch: `git checkout -b dev && git push -u origin dev`
6. Set up Google Cloud Console project:
   - Enable Google Drive API
   - Enable Google Picker API
   - Create OAuth 2.0 credentials (Web application type)
   - Add authorized redirect URIs for localhost + GitHub Pages
   - Save Client ID (goes in code, not secret) and Client Secret (goes in env if needed)

**THEN — Discovery Phase (Step 7):**
7. Competitive analysis: look at CodePen, JSFiddle, HTMLPreview.github.io
8. Define exact user flow (paste → preview → save)
9. Validate assumptions about Google APIs

**THEN — Design Phase (Step 8):**
10. Wireframes/mockup (Stitch or ASCII)
11. Finalize design-system.md
12. Architecture review (arch.md)

**THEN — SDD Cycle for M1:**
13. Specify → Plan → Tasks → Implement

### Key Data for Reference
- Google APIs needed: Drive API v3, Picker API, OAuth2
- OAuth2 scopes: `https://www.googleapis.com/auth/drive.file` (create/open files only)
- Picker API scope: `https://www.googleapis.com/auth/drive.readonly` (for folder browsing)
- iframe preview approach: `srcdoc` attribute (avoids CORS issues)
- Obsidian compatibility: .html files render natively in Obsidian vault
- Framework skill location (CintVibe): `.skills-dev/mjrp-project-setup/`
- Framework skill needs to be copied to: `/Users/mpedroso/0.MyPetProjects/MJRPprojSetupFramework`
