# Tasks: M4 — Markdown & Mermaid Render

> **Status**: ✅ COMPLETED (2026-02-27)
> **Date**: 2026-02-26 → 2026-02-27
> **Spec**: docs/specs/m4/spec.md (APPROVED)
> **Plan**: docs/specs/m4/plan.md (APPROVED)

---

## Step 0: Modularization (Refactoring)
- [x] Criar pasta `js/` na raiz do projeto.
- [x] Extrair lógica do Google Drive (OAuth, Picker, Upload) para `js/drive.js`.
- [x] Extrair lógica de Exports (Download, PDF, PNG) para `js/export.js`.
- [x] Extrair lógica de Preview (detectInputType, injectBaseHref, BYOK settings) para `js/preview.js`.
- [x] Criar `js/app.js` como bootstrap (DOM refs, event listeners, init).
- [x] Remover `<script>` inline do `index.html`, substituir por `<script src="js/...">` tags.
- [x] Testar que TODAS as funcionalidades existentes continuam operando.
- [x] Commit: `refactor: modularize JS into separate files`

## Step 1: CDN Scripts
- [x] Adicionar `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>` no final do `<body>`.
- [x] Mermaid carregado via lazy-load em preview.js (não no HTML).

## Step 2: Detect Input Type
- [x] Criar função `detectInputType(text)` que retorna `'html'` ou `'markdown'`.
- [x] Implementar regex para detecção de tags HTML de bloco no início do texto.
- [x] Fallback: se não detectar HTML → retorna `'markdown'`.

## Step 3: Markdown Styles
- [x] Criar função `wrapWithMdStyles(html)` que encapsula o HTML parseado numa stylesheet inline.
- [x] Estilos cobrem: headings, code/pre, blockquote, table, links, images, hr.
- [x] Tipografia: `system-ui`, max-width `800px`, centralizado.
- [x] Links usam `#58a6ff` (accent-cyan do design-system).

## Step 4: Mermaid Lazy Load
- [x] Criar função `initMermaidIfNeeded(iframeDoc)` que verifica a existência de blocos `code.language-mermaid`.
- [x] Se existirem, injetar dinamicamente o script `mermaid.min.js` dentro do `<head>` do iframe.
- [x] Criar função `renderMermaid(iframeDoc)` que substitui `<pre><code class="language-mermaid">` por `<div class="mermaid">` e invoca `mermaid.run()`.
- [x] Variável `mermaidLoaded` para evitar re-injeção do script.

## Step 5: Update Event Listener
- [x] Refatorar o listener `htmlInput.addEventListener('input', ...)` para chamar `detectInputType()`.
- [x] Se `'html'` → manter pipeline atual (`injectBaseHref(raw)`).
- [x] Se `'markdown'` → `marked.parse(raw)` → `wrapWithMdStyles()` → `injectBaseHref()` → `srcdoc`.
- [x] Adicionar `previewFrame.onload` callback para executar `initMermaidIfNeeded()` após render do Markdown.

## Step 6: Update Placeholder
- [x] Alterar o placeholder do textarea para `<!-- Paste your HTML or Markdown here... -->`.

## Step 7: Script Load Order Fix
- [x] Mover CDN scripts do `<head>` para o final do `<body>` (antes dos módulos).
- [x] Google API scripts com `async defer` carregam por último (callbacks já definidos em drive.js).
- [x] Remover `DOMContentLoaded` wrapper (desnecessário com scripts no final do body).

## Step 8: Download Type Detection
- [x] Download detecta se input é Markdown → salva como `.md`.
- [x] Download detecta se input é HTML → salva como `.html`.
- [x] Deferred `URL.revokeObjectURL` com `setTimeout` para evitar race condition.

## Verification
- [x] Testar com HTML puro → funciona exatamente como antes.
- [x] Testar com Markdown puro (headings, bold, lists, links, code blocks, tables).
- [x] Testar com Markdown contendo bloco ` ```mermaid ` → renderiza SVG.
- [x] Testar PDF export com Markdown renderizado.
- [x] Testar PNG export com Markdown renderizado.
- [x] Testar Fullscreen Preview com Markdown.
- [x] Download `.md` com nome correto.
- [x] Deploy final no GitHub Pages via merge main.
