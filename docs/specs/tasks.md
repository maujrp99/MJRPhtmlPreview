# Tasks: Milestone 1 (MVP)

**Status**: In Progress
**Date**: 2026-02-25
**Plan Reference**: docs/specs/plan.md

## Pre-Implementation
- [x] Cerimônia de Design com Wireframes Stitch (Green Accent aprovado).
- [x] Verify spec and plan are APPROVED.

## Implementation: UI Structure
- [x] Criar a base do `index.html` com suporte a `viewport` mobile.
- [x] Montar container grid para Split Screen layout (50/50).
- [x] Construir a barra do topo (Toolbar) do painel esquerdo: 
      - Título: "MJRPhtmlPreview"
      - Botão secundário "Clear"
      - Botão desabilitado "Save to Drive" (Google icon stub)
      - Botão primário verde "Download Local"
- [x] Inserir a `<textarea>` de entrada de código preenchendo o resto da coluna esquerda.
- [x] Inserir a tag `<iframe>` branca pura no painel direito.

## Implementation: Theme & Styling (CSS Inline)
- [x] Declarar variáveis CSS globais baseadas no `design-system.md` (Minimal Dark).
- [x] Estilizar botões (states de hover e active) e tipografia.
- [x] Injetar tipografia: JetBrains Mono (para o textarea) e Inter (labels).
- [x] Incluir Media Query para design empilhado (código em cima, iframe embaixo) em mobile.

## Implementation: Logic (JS Inline)
- [x] Adicionar evento de *input* ao `<textarea>` que pegue o valor e atualize o atributo `srcdoc` do `<iframe>` em tempo real.
- [x] Adicionar lógica ao botão "Clear" para esvaziar a `<textarea>` e embutir template HTML básico padrão.
- [x] Adicionar lógica ao botão "Download Local" que cria dinamicamente um Blob text/html do conteúdo no textarea e simule um clique numa tag `<a>` para disparar download passando o nome "preview_YYYMMDD.html".

## Verification & Documentation
- [ ] Manual verification do pipeline: colar snippet, ver live preview, fazer download do .html.
- [ ] Commit e review do código de M1.
