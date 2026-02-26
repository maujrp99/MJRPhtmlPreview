# Tasks: M4 — Markdown & Mermaid Render

> **Status**: 🟡 AWAITING APPROVAL
> **Date**: 2026-02-26
> **Spec**: docs/specs/m4/spec.md (APPROVED)
> **Plan**: docs/specs/m4/plan.md (APPROVED)

---

## Step 1: CDN Scripts
- [ ] Adicionar `<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>` no `<head>` do `index.html`, logo após o script do `html2canvas`.
- [ ] Adicionar comentário `<!-- M4: Markdown & Mermaid -->` para rastreabilidade.

## Step 2: Detect Input Type
- [ ] Criar função `detectInputType(text)` que retorna `'html'` ou `'markdown'`.
- [ ] Implementar regex para detecção de tags HTML de bloco no início do texto.
- [ ] Fallback: se não detectar HTML → retorna `'markdown'`.

## Step 3: Markdown Styles
- [ ] Criar função `wrapWithMdStyles(html)` que encapsula o HTML parseado numa stylesheet inline.
- [ ] Estilos devem cobrir: headings, code/pre, blockquote, table, links, images, hr.
- [ ] Tipografia: `system-ui`, max-width `800px`, centralizado.
- [ ] Links usar `#58a6ff` (accent-cyan do design-system).

## Step 4: Mermaid Lazy Load
- [ ] Criar função `initMermaidIfNeeded(iframeDoc)` que verifica a existência de blocos `code.language-mermaid`.
- [ ] Se existirem, injetar dinamicamente o script `mermaid.min.js` dentro do `<head>` do iframe.
- [ ] Criar função `renderMermaid(iframeDoc)` que substitui `<pre><code class="language-mermaid">` por `<div class="mermaid">` e invoca `mermaid.run()`.
- [ ] Variável `mermaidLoaded` para evitar re-injeção do script.

## Step 5: Update Event Listener
- [ ] Refatorar o listener `htmlInput.addEventListener('input', ...)` para chamar `detectInputType()`.
- [ ] Se `'html'` → manter pipeline atual (`injectBaseHref(raw)`).
- [ ] Se `'markdown'` → `marked.parse(raw)` → `wrapWithMdStyles()` → `injectBaseHref()` → `srcdoc`.
- [ ] Adicionar `previewFrame.onload` callback para executar `initMermaidIfNeeded()` após render do Markdown.

## Step 6: Update Placeholder
- [ ] Alterar o placeholder do textarea de `<!-- Paste your HTML here... -->` para `<!-- Paste your HTML or Markdown here... -->`.

## Verification
- [ ] Testar com HTML puro → deve funcionar exatamente como antes.
- [ ] Testar com Markdown puro (headings, bold, lists, links, code blocks, tables).
- [ ] Testar com Markdown contendo bloco ` ```mermaid ` → deve renderizar SVG.
- [ ] Testar PDF export com Markdown renderizado.
- [ ] Testar PNG export com Markdown renderizado.
- [ ] Testar Fullscreen Preview com Markdown.
- [ ] Commit final: `feat(M4): implement Markdown & Mermaid render pipeline`
