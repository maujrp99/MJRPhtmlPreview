# Architecture — MJRPhtmlPreview

> Documentação Arquitetural e Decisões Técnicas.
> Última atualização: 2026-02-27 (M4 completa)

## System Overview
Um visualizador de HTML/Markdown client-side puramente estático. Single-page app sem backend, sem build tools, hospedado no GitHub Pages. Código modularizado em 4 arquivos JS vanilla.

## File Structure
```
MJRPhtmlPreview/
├── index.html          ← HTML + CSS (estrutura e estilo, 421 linhas)
├── js/
│   ├── app.js          ← Bootstrap, DOM refs, event wiring (50 linhas)
│   ├── preview.js      ← Render pipeline: detect, parse, inject (153 linhas)
│   ├── drive.js        ← Google OAuth, Picker, Upload, BYOK Settings (173 linhas)
│   └── export.js       ← Download (.html/.md), PDF print, PNG capture (78 linhas)
├── docs/specs/         ← SpecKit artifacts (spec, plan, tasks, stories)
└── images/             ← Local dev images (gitignored)
```

## Component Diagram
- **UI Container** (`index.html`): Layout grid 50/50, CSS-only dark theme com tokens visuais.
- **Code Editor**: `<textarea>` com escuta de evento `input` contínuo.
- **Preview Engine** (`preview.js`): Iframe `sandbox="allow-scripts allow-popups allow-same-origin allow-modals"` que recebe conteúdo via `srcdoc`.
- **Toolbar**: Barra de botões (Clear, Fullscreen, Drive Save, PDF, PNG, Local Download).
- **Markdown Parser** (`preview.js`): Detecção automática MD vs HTML → marked.js → stylesheet inline → srcdoc.
- **Mermaid Renderer** (`preview.js`): Lazy-loaded dentro do iframe quando blocos ```` ```mermaid ```` são detectados.
- **File Exporter** (`export.js`): Download HTML/MD, PDF print, PNG via html2canvas.
- **Drive Module** (`drive.js`): OAuth2 + Picker + Upload + BYOK Settings modal.

## Data Flow

### HTML Pipeline (M1-M3):
```
textarea.value → injectBaseHref() → iframe.srcdoc
```

### Markdown Pipeline (M4):
```
textarea.value → detectInputType()
  ├─ "html"     → injectBaseHref() → iframe.srcdoc
  └─ "markdown" → marked.parse() → wrapWithMdStyles() → injectBaseHref() → iframe.srcdoc
                                                           ↓
                                                   initMermaidIfNeeded() (lazy, iframe.onload)
```

### Export Flow:
```
textarea.value → detectInputType()
  ├─ "html"     → Blob(text/html) → download preview_YYYYMMDD.html
  └─ "markdown" → Blob(text/markdown) → download preview_YYYYMMDD.md
```

## API Integration Design
Google Drive integration via BYOK (Bring Your Own Keys):
- Credenciais armazenadas no `localStorage` (nunca no Git).
- `js/drive.js` encapsula OAuth2 (`gsi/client`), Picker API, e Upload (`multipart/related`).
- Scripts Google carregam com `async defer` no final do `<body>`, após os módulos da app.

## External Dependencies
| Lib | CDN | Size | Purpose |
|-----|-----|------|---------|
| marked.js | jsdelivr | ~40KB | Markdown → HTML parser |
| mermaid.js | jsdelivr | ~1.5MB | Diagrama → SVG (lazy-loaded) |
| html2canvas | cdnjs | ~40KB | DOM → PNG capture |
| Google GSI | google | ~30KB | OAuth2 authentication |
| Google GAPI | google | ~50KB | Drive API + Picker |

## Security Architecture
- Iframe sandboxed: `allow-scripts allow-popups allow-same-origin allow-modals`.
- Scripts do usuário rodam isolados dentro do iframe sandbox.
- API keys no `localStorage` (client-side only, nunca transmitidas ao nosso servidor — não temos servidor).
- Mermaid.js carrega **dentro do iframe**, não no DOM principal da app.
