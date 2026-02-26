# Specification: M4 — Markdown & Mermaid Render

> **Status**: ✅ APPROVED (2026-02-26 20:09)
> **Date**: 2026-02-26
> **Author**: Antigravity
> **Refs**: constitution.md, arch.md, design-system.md

---

## 1. Objective (WHAT & WHY)
Permitir que o usuário cole texto em **Markdown** (incluindo blocos de diagrama **Mermaid**) diretamente no textarea, e veja o resultado renderizado no iframe — sem precisar converter manualmente para HTML antes de colar.

**Por quê?** As IAs modernas (Claude, ChatGPT, Gemini) respondem nativamente em Markdown. Obrigar o usuário a pedir "converta para HTML" gera fricção desnecessária. O MJRPhtmlPreview evolui de "HTML Previewer" para "Universal Content Previewer".

## 2. Functional Requirements

### FR04.1 — Auto-Detect Input Type
O sistema deve detectar automaticamente se o conteúdo do textarea é **HTML** ou **Markdown**, usando a seguinte heurística:
- Se o texto começa com `<!DOCTYPE`, `<html`, `<head`, `<body`, `<div`, `<section`, `<table`, ou qualquer tag HTML de bloco → tratar como **HTML puro** (pipeline atual, sem transformação).
- Caso contrário → tratar como **Markdown** e passar pelo parser antes de injetar no iframe.

> **Edge case**: O usuário pode colar HTML fragments (sem doctype). A heurística deve verificar a presença de tags HTML como `<div>`, `<span>`, `<h1>`, `<p>`, `<img>`, `<style>`, `<script>` no início do texto.

### FR04.2 — Markdown → HTML Conversion
- Biblioteca: **`marked.js`** (CDN, ~40KB gzip, zero deps, MIT license).
- O parser deve converter todo Markdown padrão (headings, bold, italic, lists, links, images, code blocks, tables, blockquotes).
- O HTML resultante deve ser encapsulado com uma folha de estilos mínima dentro do srcdoc para garantir legibilidade (tipografia, espaçamento, syntax highlighting para code blocks).

### FR04.3 — Mermaid Diagram Rendering
- Biblioteca: **`mermaid.js`** (CDN, ~1.5MB, MIT license).
- Blocos de código marcados com ` ```mermaid ` no Markdown devem ser identificados após a conversão do `marked.js`.
- O mermaid engine deve ser inicializado e os blocos convertidos para **SVGs inline** dentro do iframe.
- Tipos de diagrama suportados (todos nativos do Mermaid): flowchart, sequence, gantt, pie, class, state, ER, journey, gitgraph.

### FR04.4 — Markdown Styling (Iframe)
- O HTML convertido de Markdown deve receber uma stylesheet interna leve para legibilidade:
  - Tipografia base: `system-ui, sans-serif`
  - Code blocks: fundo `#f6f8fa`, borda `1px solid #d0d7de`, monospace
  - Tables: bordas sutis, padding
  - Blockquotes: borda esquerda com accent color
  - Links: cor `#58a6ff` (accent-cyan do design system)
  - Max-width: `800px`, margem centralizada (para leitura confortável)

## 3. Non-Functional Requirements

### NFR-M4.1 — Performance
- A detecção MD vs HTML deve ser instantânea (<1ms, é um regex simples).
- A conversão Markdown → HTML via `marked.js` deve completar em <50ms para documentos de até 10.000 caracteres.
- A inicialização do Mermaid deve ser **lazy**: o script só é carregado se um bloco `mermaid` for detectado no texto (evitar carregar 1.5MB desnecessariamente).

### NFR-M4.2 — Vanilla-First Compliance
- As bibliotecas `marked.js` e `mermaid.js` são carregadas via CDN `<script>`, sem bundler, npm, ou build step.
- A decisão de adicionar essas dependências externas está justificada pela impossibilidade de implementar um parser Markdown ou renderer SVG de diagramas em Vanilla JS de forma razoável.

### NFR-M4.3 — Backward Compatibility
- HTML puro colado no textarea DEVE continuar funcionando exatamente como antes.
- A M4 não pode quebrar nenhuma funcionalidade existente (Download, PDF, PNG, Drive, BYOK, Fullscreen).

## 4. Architecture Impact

### Pipeline Atual (M1-M3):
```
textarea.value → injectBaseHref() → iframe.srcdoc
```

### Pipeline Proposto (M4):
```
textarea.value → detectInputType()
  ├─ HTML → injectBaseHref() → iframe.srcdoc     (sem mudança)
  └─ Markdown → marked.parse() → injectMdStyles() → injectBaseHref() → iframe.srcdoc
                                                      ↓
                                              mermaid.run() (lazy, se detectar bloco)
```

## 5. External Dependencies

| Lib | CDN URL | Size | License | Justification |
|-----|---------|------|---------|---------------|
| marked.js | `https://cdn.jsdelivr.net/npm/marked/marked.min.js` | ~40KB | MIT | Parser MD → HTML. Não existe alternativa vanilla razoável. |
| mermaid.js | `https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js` | ~1.5MB | MIT | Render de diagramas como SVG. Impossível em vanilla. |

## 6. Edge Cases & Constraints
- **Mixed content**: Se o usuário colar um HTML que também contém Markdown dentro, o sistema NÃO deve tentar converter. A regra é: se parece HTML, trata como HTML.
- **Mermaid errors**: Se um diagrama Mermaid tiver sintaxe inválida, o mermaid.js exibe uma mensagem de erro vermelha inline. Isso é aceitável como comportamento (fail gracefully).
- **Export compatibility**: PDF e PNG devem funcionar normalmente com Markdown renderizado (já que o export opera sobre o conteúdo final do iframe, que será HTML de qualquer forma).
