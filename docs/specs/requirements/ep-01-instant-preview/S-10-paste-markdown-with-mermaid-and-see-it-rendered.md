---
id: S-10
aliases: [S-10]
type: requirement
format: story
status: Done
priority: P1
epic: "[[prd#^EP-01]]"
points_to: ["[[behavior#^markdown-rendered]]"]
delivered_by: "c7c8555"
---
# S-10 · Colar Markdown (com Mermaid) e ver renderizado

## pt-BR

Como desenvolvedor, eu quero colar texto em Markdown (incluindo diagramas Mermaid) e ver o resultado renderizado, sem precisar converter manualmente para HTML.

**Acceptance Criteria:**
- [x] O sistema detecta automaticamente se o input é Markdown ou HTML.
- [x] Markdown é convertido para HTML via `marked.js` antes de ser injetado no iframe.
- [x] Blocos ````mermaid```` são renderizados como SVGs nativos via `mermaid.js` (lazy-loaded).
- [x] HTML puro continua funcionando sem alteração.

**Priority:** High | **Milestone:** M4 | **Status:** ✅ Done

Comportamento: [[behavior#^markdown-rendered]] · descrição retroativa do que existe (sem julgamento registrado)
Entregue por: `c7c8555` · feature F02 (Done)
Origem: `docs/specs/story.md` [US-10] (arquivado em `_archive/2026-10-05-story-md/story.md`)

## en

**Paste Markdown (with Mermaid) and see it rendered**

As a developer, I want to paste Markdown text (including Mermaid diagrams) and see the rendered result, without having to convert it to HTML manually.

**Acceptance Criteria:**
- [x] The system automatically detects whether the input is Markdown or HTML.
- [x] Markdown is converted to HTML via `marked.js` before being injected into the iframe.
- [x] ````mermaid```` blocks are rendered as native SVGs via `mermaid.js` (lazy-loaded).
- [x] Plain HTML keeps working unchanged.

**Priority:** High | **Milestone:** M4 | **Status:** ✅ Done

Behavior: [[behavior#^markdown-rendered]] · retroactive description of what exists (no recorded judgment)
Delivered by: `c7c8555` · feature F02 (Done)
Origin: `docs/specs/story.md` [US-10] (archived at `_archive/2026-10-05-story-md/story.md`)
