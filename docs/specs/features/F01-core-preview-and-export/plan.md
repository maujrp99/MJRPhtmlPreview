# Plan — MJRPhtmlPreview

> Estratégia de implementação mapeada por Milestones. Trilha o "Como faremos".

## M1: MVP (Paste + Preview + Local Save) - CONCLUÍDO
- [x] Initial Scaffold & Framework Setup (GitHub + Docs)
- [x] Discovery & Ideation
- [x] Design Flow & Wireframes Aprovados (Variant 2: Green Accent)
- [x] Arquitetura System & Component Layout Planejado
- [x] Implementação de Front-End HTML Base (`index.html` structure)
- [x] Implementação Estilos Minimal Dark (CSS inline na tag `<style>`) e Layout Flexbox Responsivo.
- [x] Implementação Logic JS: Data-binding do textarea para o atributo `srcdoc` do iframe.
- [x] Implementação Logic JS: Serviço FileExporter para construção do Blob HTML `.html` e trigger do download (suporte Obsidian Vault).

## M2: Drive Integration - CONCLUÍDO
- [x] Incluir bibliotecas do Google Identity Services (`gsi/client`) e Google APIs (`api.js`) no `index.html`.
- [x] Ponto de integração OAuth 2.0 Client (necessita de `CLIENT_ID` e `APP_ID` do Console de Nuvem).
- [x] Construção do Service Google Picker UI para seleção de pastas.
- [x] Escrita das rotinas da API GDrive para enviar Blob file (Create Object vazio) persistindo os metadados.
- [x] Request secundária através de método PATCH/PUT para escrever a String da UI para o corpo do File no Drive.
- [x] Implementação de Botão Secundário: Download do layout em `.pdf` (via API nativa `print()`).

## M3: Polish - CONCLUÍDO
- [x] Adicionar feature "Clear Code" (Já implementado na toolbar).
- [x] Implementar Download para `.png`/`.jpeg` através da inclusão de conversor canvas externo (`html2canvas`).
- [x] Feedback tátil e micro-interações via transições CSS.

## M4: Markdown & Extended Render + Modularization - CONCLUÍDO
- [x] Modularizar JS inline em 4 arquivos (`js/app.js`, `js/drive.js`, `js/export.js`, `js/preview.js`).
- [x] Injetar Biblioteca de Parser Markdown (`marked.js`).
- [x] Injetar Biblioteca de Fluxogramas Mermaid (`mermaid.js`) — lazy-loaded no iframe.
- [x] Atualizar o Listener do `textarea` com `detectInputType()` (If HTML → direto, if MD → `marked.parse()` antes).
- [x] Construir lógica para detectar os blocos de código mermaid, invocar o SVG via `mermaid.run()` e substituir o nó no output.
- [x] Download detecta tipo e salva `.md` ou `.html` conforme o input.
