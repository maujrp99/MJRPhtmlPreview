# Tasks: Milestone 2 (Drive Integration)

**Status**: In Progress
**Date**: 2026-02-25
**Plan Reference**: docs/specs/plan.md

## Pre-Implementation
- [x] Update specs, stories and plan for M2.
- [ ] O Usuário (mpedroso) precisa fornecer as credenciais: `CLIENT_ID`, `API_KEY` e `APP_ID` obtidos no Google Cloud Console com as APIs do Drive e Picker ativadas, e adicionar os domínios `http://localhost`, `http://127.0.0.1` e a URL do GitHub Pages nos Origins Permitidos de Javascript. Estas credenciais deverão ser injetadas de forma declarativa e não enviadas no git.

## Implementation: GSI & APIs Setup
- [ ] Adicionar as bibliotecas do Google no `<head>`: `https://accounts.google.com/gsi/client` e `https://apis.google.com/js/api.js`.
- [ ] Implementar as variáveis globais `CLIENT_ID`, `API_KEY`, e `APP_ID`.
- [ ] Função assíncrona para inicializar a biblioteca GSI (Google Identity Services) e a GAPI Client (`gapi.client.init`).

## Implementation: Authentication Flow
- [ ] Atualizar o botão "Save to Drive" (`#btnDrive`) para acionar o trigger OAuth se o escopo (`drive.file`) ainda não estiver garantido no Token.
- [ ] Tratar estados de loading (desabilitar botão, mudar ícone ou texto provisório) durante a checagem Auth.

## Implementation: Google Picker Flow
- [ ] Implementar a função `createPicker()`:
    - Instanciar a `google.picker.PickerBuilder`.
    - Setar o modo "seleção de pasta" habilitando `google.picker.ViewId.FOLDERS`.
    - Capturar o `folderId` destino no evento de Callback do Picker (`google.picker.Action.PICKED`).

## Implementation: Drive Upload Routine
- [ ] Implementar função para salvar o HTML dentro da pasta alvo na API Drive V3.
  - [ ] Método 1 (Metadados): Realizar Request `POST https://www.googleapis.com/drive/v3/files` passando o nome do documento e definindo a `parents: [folderId]`.
    - [ ] Método 2 (Conteúdo em Si): Realizar requisição Multipart/Multipart-upload contendo o Blob `text/html`.
- [ ] Atualizar status na interface (Mudar o botão de Drive ou notificar com o link do arquivo criado no drive via `file.id`).

## Implementation: Export to PDF
- [x] Adicionar um botão discreto de PDF (`<button id="btnPdf">`) na Toolbar (Style: `.btn-ghost`).
- [x] Injetar listener para invocar o sub-documento via `.contentWindow.print()` isolando a impressão só do Iframe alvo (necessário `allow-modals` no sandbox).

## Verification & Documentation
- [ ] Teste E2E do clique do Botão Drive, Abertura Pessoal, Seleção de Pasta Root, e checagem no Drive Real.
- [ ] Validação contra o `origin` do OAuth2 no GitHub Pages se houver deploy M2 planejado.
