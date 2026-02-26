# Tasks: Milestone 3 (Polish)

**Status**: In Progress
**Date**: 2026-02-25
**Plan Reference**: docs/specs/plan.md

## Pre-Implementation
- [x] Specs, stories and plan for M3 (PNG support).

## Implementation: Export to PNG
- [x] Injetar a biblioteca externa `html2canvas` (`<script>`) no `index.html`, pois captura de pixels do DOM não é nativa da engine JS de forma leve.
- [x] Adicionar um botão de Imagem (`<button id="btnPng">`) na Toolbar (Style: `.btn-ghost` ao lado do PDF).
- [x] Interceptar clique para construir a base 64 rodando o `html2canvas()` internamente no `contentDocument.body` do iframe.
- [x] Extrair base64 e forçar download como arquivo `preview_[timestamp].png`.

## Verification & Documentation
- [x] Teste lógico do download PNG validando renderizações com CSS.
- [ ] Fazer Commit.
