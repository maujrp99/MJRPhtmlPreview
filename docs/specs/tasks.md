# Tasks — MJRPhtmlPreview

> Registro cumulativo de todas as tarefas por Milestone.

---

## Milestone 1: MVP (Paste + Preview + Local Save) ✅
**Status**: Concluído | **Date**: 2026-02-25

### Pre-Implementation
- [x] Cerimônia de Design com Wireframes Stitch (Green Accent aprovado).
- [x] Verify spec and plan are APPROVED.

### Implementation: UI Structure
- [x] Criar a base do `index.html` com suporte a `viewport` mobile.
- [x] Montar container grid para Split Screen layout (50/50).
- [x] Construir a barra do topo (Toolbar) do painel esquerdo:
      - Título: "MJRPhtmlPreview"
      - Botão secundário "Clear"
      - Botão desabilitado "Save to Drive" (Google icon stub)
      - Botão primário verde "Download Local"
- [x] Inserir a `<textarea>` de entrada de código preenchendo o resto da coluna esquerda.

### Implementation: Styling (Minimal Dark)
- [x] Injetar tokens visuais do Design System em variáveis CSS (`:root`).
- [x] Estilizar a Toolbar, botões (`.btn-ghost`, `.btn-primary`), textarea e preview panel.
- [x] Fontes Google (Inter + JetBrains Mono) via CDN `<link>`.
- [x] Responsividade mobile: media query empilhando editor sobre preview em `<768px`.

### Implementation: Logic JS
- [x] Data-binding: Listener `input` no textarea atualizando `iframe.srcdoc` em tempo real.
- [x] Botão Clear: Resetar textarea e iframe para estado vazio (placeholder).
- [x] Botão Download: Gerar Blob `text/html`, criar URL temporária, forçar download com nome `preview_YYYYMMDD_HHMM.html`.

---

## Milestone 2: Drive Integration ✅
**Status**: Concluído | **Date**: 2026-02-25

### Pre-Implementation
- [x] Update specs, stories and plan for M2.
- [x] Usuário forneceu credenciais: `CLIENT_ID`, `API_KEY` e `APP_ID` do Google Cloud Console.

### Implementation: GSI & APIs Setup
- [x] Adicionar as bibliotecas do Google no `<head>`: `gsi/client` e `api.js`.
- [x] Implementar as variáveis globais `CLIENT_ID`, `API_KEY`, e `APP_ID`.
- [x] Função assíncrona para inicializar a biblioteca GSI e a GAPI Client (`gapi.client.init`).

### Implementation: Authentication Flow
- [x] Atualizar o botão "Save to Drive" para acionar trigger OAuth se escopo `drive.file` não estiver garantido.
- [x] Tratar estados de loading (desabilitar botão, mudar texto provisório) durante a checagem Auth.

### Implementation: Google Picker Flow
- [x] Implementar a função `createPicker()`:
    - [x] Instanciar a `google.picker.PickerBuilder`.
    - [x] Setar modo "seleção de pasta" habilitando `google.picker.ViewId.FOLDERS`.
    - [x] Capturar o `folderId` destino no callback do Picker.

### Implementation: Drive Upload Routine
- [x] Upload via `POST multipart/related` com Metadata JSON + Body HTML.
- [x] Feedback visual no botão ("Saving..." → "Saved!").

---

## Milestone 3: Export Multimídia (Polish) ✅
**Status**: Concluído | **Date**: 2026-02-25

### Implementation: Export to PDF
- [x] Botão PDF (`#btnPdf`) na Toolbar (Style: `.btn-ghost`).
- [x] Listener invocando `contentWindow.print()` isolando impressão do iframe.

### Implementation: Export to PNG
- [x] Injetar biblioteca `html2canvas` via CDN.
- [x] Botão PNG (`#btnPng`) na Toolbar ao lado do PDF.
- [x] Captura via `html2canvas(iframeDoc.body)` → Base64 → download como `.png`.
- [x] ⚠️ Limitação documentada: falha com HTML dinâmico (charts, canvas). Ver `docs/debug-log.md`.

---

## Milestone 3.5: BYOK Settings ✅
**Status**: Concluído | **Date**: 2026-02-25

### Implementation: Settings UI
- [x] Ícone de engrenagem "⚙️ Settings" ao lado do título na Toolbar.
- [x] Modal Overlay com inputs para `CLIENT_ID`, `API_KEY`, `APP_ID`.
- [x] Estilização do modal usando design-tokens existentes.

### Implementation: Storage Logic
- [x] Persistência em `localStorage.setItem('mjrp_google_keys', JSON)`.
- [x] Fluxo `onload`: buscar no localStorage → hidratar `GOOGLE_CONFIG` → inicializar GSI.
- [x] Removida dependência do arquivo `config.js` externo.

---

## Session 2026-02-26: UX Improvements ✅
**Status**: Concluído | **Date**: 2026-02-26

### Implementation: Base Href Injection
- [x] Função `injectBaseHref()` insere `<base href="...images/">` no HTML antes do iframe.
- [x] Permite usar `src="filename.png"` sem path completo.

### Implementation: Fullscreen Preview
- [x] Botão "⛶ Preview" (azul) na toolbar para esconder editor.
- [x] CSS classe `.fullscreen-preview` no `<main>` para grid 1fr.
- [x] Barra "✏️ Editor" no topo do preview para voltar ao modo split.

### Implementation: Image Privacy
- [x] Imagens removidas do repositório público.
- [x] `images/` adicionado ao `.gitignore`.
- [x] Estratégia definida: Google Drive thumbnail links para produção.

---

## Milestone 4: Markdown & Mermaid (Pendente)
**Status**: Não iniciado | **Plan Ref**: docs/specs/plan.md

### Implementation: Markdown Parser
- [ ] Injetar `marked.js` via CDN.
- [ ] Injetar `mermaid.js` via CDN.
- [ ] Detecção automática MD vs HTML no textarea.
- [ ] Pipeline: Markdown → HTML → iframe srcdoc (com Mermaid SVG inline).

