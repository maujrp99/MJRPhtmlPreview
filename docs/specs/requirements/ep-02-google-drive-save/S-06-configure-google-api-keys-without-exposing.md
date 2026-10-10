---
id: S-06
aliases: [S-06]
type: requirement
format: story
status: Done
priority: P1
epic: "[[prd#^EP-02]]"
points_to: ["[[behavior#^google-keys-configured]]"]
delivered_by: "f51beaa"
---
# S-06 · Configurar as chaves da API do Google sem expô-las no código

## pt-BR

Como desenvolvedor, eu quero configurar minhas chaves da API do Google sem expô-las no código-fonte público.

**Acceptance Criteria:**
- [x] Existe um botão ⚙️ Settings na toolbar que abre um modal.
- [x] O modal permite inserir CLIENT_ID, API_KEY e APP_ID.
- [x] As chaves são salvas no `localStorage` do navegador (nunca no Git).
- [x] O botão Drive só é ativado após as chaves serem configuradas.
- [x] O arquivo `config.js` foi eliminado da arquitetura.

**Priority:** High | **Milestone:** M3.5 | **Status:** ✅ Done

Comportamento: [[behavior#^google-keys-configured]] · descrição retroativa do que existe (sem julgamento registrado)
Entregue por: `f51beaa` · feature F01 (Done)
Origem: `docs/specs/story.md` [US-06] (arquivado em `_archive/2026-10-05-story-md/story.md`)

## en

**Configure the Google API keys without exposing them in the code**

As a developer, I want to configure my Google API keys without exposing them in the public source code.

**Acceptance Criteria:**
- [x] There is a ⚙️ Settings button in the toolbar that opens a modal.
- [x] The modal lets me enter CLIENT_ID, API_KEY and APP_ID.
- [x] The keys are saved in the browser's `localStorage` (never in Git).
- [x] The Drive button is only enabled after the keys are configured.
- [x] The `config.js` file was removed from the architecture.

**Priority:** High | **Milestone:** M3.5 | **Status:** ✅ Done

Behavior: [[behavior#^google-keys-configured]] · retroactive description of what exists (no recorded judgment)
Delivered by: `f51beaa` · feature F01 (Done)
Origin: `docs/specs/story.md` [US-06] (archived at `_archive/2026-10-05-story-md/story.md`)
