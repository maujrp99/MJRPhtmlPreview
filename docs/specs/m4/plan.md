# Plan: M4 — Markdown & Mermaid Render

> **Status**: 🟡 AWAITING APPROVAL
> **Date**: 2026-02-26
> **Spec Reference**: docs/specs/m4/spec.md (APPROVED)

---

## Documents Consulted
- **constitution.md** — Vanilla-first philosophy. Duas dependências CDN justificadas.
- **arch.md** — Pipeline textarea → srcdoc. M4 insere etapa intermediária de parsing.
- **design-system.md** — Iframe mantém fundo branco. Markdown styling usa system-ui.
- **index.html** — Ponto de inserção mapeado: linhas 8-11 (scripts head), linhas 503-521 (pipeline data binding).

---

## 1. Strategy Overview

A implementação segue a regra **"Add, don't break"**: inserimos uma camada nova de processamento entre o textarea e o iframe, sem alterar nenhuma das funções existentes.

```
ANTES (M1-M3):
  textarea.value ──→ injectBaseHref() ──→ iframe.srcdoc

DEPOIS (M4):
  textarea.value ──→ detectInputType()
                       ├─ "html"     → injectBaseHref() → iframe.srcdoc
                       └─ "markdown" → marked.parse()
                                        → wrapWithMdStyles()
                                        → injectBaseHref()
                                        → iframe.srcdoc
                                        → initMermaidIfNeeded() (lazy)
```

## 2. Implementation Order

### Step 1: Add CDN Scripts (Head)
Insert after line 11 (`html2canvas`):
```html
<!-- M4: Markdown & Mermaid -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<!-- Mermaid loaded lazily in JS, not here -->
```
> **Decisão**: `marked.js` carrega no boot (40KB, leve). `mermaid.js` é injetado via JS apenas quando necessário (1.5MB, pesado).

### Step 2: Create `detectInputType()` function
```javascript
function detectInputType(text) {
    const trimmed = text.trim();
    // Check for common HTML indicators at the start
    const htmlPattern = /^(<\!DOCTYPE|<html|<head|<body|<div|<section|<table|<nav|<header|<footer|<main|<article|<style|<script|<link|<meta)/i;
    // Also check for ANY html tag in the first 200 chars
    const hasHtmlTags = /<[a-z][\s\S]*?>/i.test(trimmed.substring(0, 200));
    return htmlPattern.test(trimmed) || (hasHtmlTags && !trimmed.startsWith('#')) ? 'html' : 'markdown';
}
```

### Step 3: Create `wrapWithMdStyles()` function
Wraps parsed Markdown HTML in a minimal, readable stylesheet:
```javascript
function wrapWithMdStyles(html) {
    return `
    <style>
        body { font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; 
               max-width: 800px; margin: 0 auto; padding: 24px; color: #1f2328; }
        h1, h2, h3 { margin-top: 24px; margin-bottom: 16px; font-weight: 600; }
        h1 { font-size: 2em; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; }
        h2 { font-size: 1.5em; border-bottom: 1px solid #d0d7de; padding-bottom: 6px; }
        code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px; font-size: 0.875em; }
        pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; }
        pre code { background: none; padding: 0; }
        blockquote { border-left: 4px solid #58a6ff; padding: 8px 16px; margin: 16px 0; color: #656d76; }
        table { border-collapse: collapse; width: 100%; margin: 16px 0; }
        th, td { border: 1px solid #d0d7de; padding: 8px 12px; text-align: left; }
        th { background: #f6f8fa; font-weight: 600; }
        a { color: #58a6ff; }
        img { max-width: 100%; }
        hr { border: none; border-top: 1px solid #d0d7de; margin: 24px 0; }
    </style>
    ${html}`;
}
```

### Step 4: Create `initMermaidIfNeeded()` function
```javascript
let mermaidLoaded = false;

function initMermaidIfNeeded(iframeDoc) {
    // Check if any mermaid blocks exist
    const mermaidBlocks = iframeDoc.querySelectorAll('code.language-mermaid, pre > code.language-mermaid');
    if (mermaidBlocks.length === 0) return;

    // Lazy load mermaid.js into the iframe
    if (!mermaidLoaded) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js';
        script.onload = () => {
            mermaidLoaded = true;
            renderMermaid(iframeDoc);
        };
        iframeDoc.head.appendChild(script);
    } else {
        renderMermaid(iframeDoc);
    }
}

function renderMermaid(iframeDoc) {
    // Convert code blocks to mermaid div containers
    const blocks = iframeDoc.querySelectorAll('code.language-mermaid');
    blocks.forEach(block => {
        const pre = block.parentElement;
        const div = iframeDoc.createElement('div');
        div.className = 'mermaid';
        div.textContent = block.textContent;
        pre.replaceWith(div);
    });
    // Run mermaid
    iframeDoc.defaultView.mermaid.initialize({ startOnLoad: false, theme: 'default' });
    iframeDoc.defaultView.mermaid.run();
}
```

### Step 5: Update the Input Event Listener
Replace the current simple listener with the dual-pipeline:
```javascript
htmlInput.addEventListener('input', () => {
    const raw = htmlInput.value;
    if (!raw.trim()) {
        previewFrame.srcdoc = EMPTY_PREVIEW;
        return;
    }

    const inputType = detectInputType(raw);

    if (inputType === 'html') {
        previewFrame.srcdoc = injectBaseHref(raw);
    } else {
        const parsedHtml = marked.parse(raw);
        const styled = wrapWithMdStyles(parsedHtml);
        previewFrame.srcdoc = injectBaseHref(styled);

        // After iframe loads, check for mermaid
        previewFrame.onload = () => {
            const iframeDoc = previewFrame.contentDocument;
            if (iframeDoc) initMermaidIfNeeded(iframeDoc);
        };
    }
});
```

### Step 6: Update placeholder text
```
<!-- Paste your HTML or Markdown here... -->
```

## 3. UI Mockup (ASCII)

Nenhuma mudança visual na UI externa. A experiência muda apenas **dentro do iframe**:

```
┌──────────────────────────┐  ┌──────────────────────────┐
│ MJRPhtmlPreview ⚙️       │  │                          │
│ [Clear] [⛶] [☁] [PDF]..│  │   # My Document          │
├──────────────────────────┤  │                          │
│ # My Document            │  │   This is a paragraph    │
│                          │  │   with **bold** text.    │
│ This is a paragraph      │  │                          │
│ with **bold** text.      │  │   ┌─────────────────┐   │
│                          │  │   │  ┌──┐    ┌──┐   │   │
│ ```mermaid               │  │   │  │A │───→│B │   │   │
│ graph LR                 │  │   │  └──┘    └──┘   │   │
│   A --> B                │  │   └─────────────────┘   │
│ ```                      │  │          (SVG)          │
│                          │  │                          │
└──────────────────────────┘  └──────────────────────────┘
     TEXTAREA (Markdown)           IFRAME (Rendered)
```

## 4. Risk Mitigation
- **Mermaid.js falhando silenciosamente**: Se CDN estiver down, `onload` never fires → diagrama fica como texto. Aceitável.
- **Falso positivo na detecção**: Se Markdown começar com `<div>`, será tratado como HTML. Aceitável (edge case raro, usuário pode remover a tag).
