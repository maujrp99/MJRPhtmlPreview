# Tasks: Milestone 3.5 (BYOK Settings)

**Status**: In Progress
**Date**: 2026-02-25
**Plan Reference**: docs/specs/plan.md

## Implementation: Settings UI
- [x] Criar ícone de engrenagem "⚙️ Settings" ao lado do título ou actions da Toolbar.
- [x] Criar estrutura em HTML (escondida por padrão) para o Modal Overlay contendo:
  - Input para `CLIENT_ID`
  - Input para `API_KEY`
  - Input para `APP_ID`
  - Botão "Save Settings" e botão "Close/Cancel".
- [x] Estilizar o modal usando os design-tokens já existentes (`--bg-surface`, `--accent-green`, etc).

## Implementation: Storage Logic
- [x] Ao salvar, pegar os values dos inputs e persistir no `localStorage.setItem('mjrp_goolge_keys', JSON)`.
- [x] Ajustar o fluxo inicial de página (`onload`): buscar no localStorage, e se as chaves existirem, hidratar a variável `GOOGLE_CONFIG` globalmente e dar Load no script do GSI.
- [x] Deletar a dependência do arquivo `config.js` externo e remover sua tag de import do Head do HTML.
