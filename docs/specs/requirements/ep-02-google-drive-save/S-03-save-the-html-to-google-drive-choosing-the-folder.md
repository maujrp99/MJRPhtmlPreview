---
id: S-03
aliases: [S-03]
type: requirement
format: story
status: Done
priority: P1
epic: "[[prd#^EP-02]]"
points_to: ["[[behavior#^drive-file-saved]]"]
delivered_by: "ff78aa1"
---
# S-03 · Salvar o HTML no Google Drive, escolhendo a pasta

## pt-BR

Como desenvolvedor, eu quero salvar meu HTML diretamente no meu Google Drive, escolhendo a pasta de destino, para organizar as saídas da IA na nuvem.

**Acceptance Criteria:**
- [x] O botão "Save to Drive" deve estar habilitado (após configuração BYOK).
- [x] Ao clicar, o fluxo de OAuth2 do Google é acionado.
- [x] Após o login, o Google Picker Modal aparece para que eu escolha uma pasta no Drive.
- [x] O conteúdo HTML é salvo como um arquivo `.html` na pasta escolhida.
- [x] O botão fornece feedback visual de "Salvando..." e "Sucesso" (cor verde).

**Priority:** High | **Milestone:** M2 | **Status:** ✅ Done

Comportamento: [[behavior#^drive-file-saved]] · descrição retroativa do que existe (sem julgamento registrado)
Entregue por: `ff78aa1` · feature F01 (Done)
Origem: `docs/specs/story.md` [US-03] (arquivado em `_archive/2026-10-05-story-md/story.md`)

## en

**Save the HTML to Google Drive, choosing the folder**

As a developer, I want to save my HTML directly to my Google Drive, choosing the destination folder, to organize the AI outputs in the cloud.

**Acceptance Criteria:**
- [x] The "Save to Drive" button must be enabled (after BYOK configuration).
- [x] On click, the Google OAuth2 flow is triggered.
- [x] After login, the Google Picker Modal appears so that I can choose a folder in Drive.
- [x] The HTML content is saved as an `.html` file in the chosen folder.
- [x] The button gives visual feedback of "Salvando..." ("Saving...") and "Sucesso" ("Success") (green color).

**Priority:** High | **Milestone:** M2 | **Status:** ✅ Done

Behavior: [[behavior#^drive-file-saved]] · retroactive description of what exists (no recorded judgment)
Delivered by: `ff78aa1` · feature F01 (Done)
Origin: `docs/specs/story.md` [US-03] (archived at `_archive/2026-10-05-story-md/story.md`)
