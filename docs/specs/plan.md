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

## M4: Markdown & Extended Render (Novo) - ATUAL
- [ ] Injetar Biblioteca de Parser Markdown (`marked.js`).
- [ ] Injetar Biblioteca de Fluxogramas Mermaid (`mermaid.js`).
- [ ] Atualizar o Listener do `textarea` para verificar a presença de Tags base e fazer um "If/Else" (Se tiver cara de HTML renderiza direto, se aparentar Markdown -> Passa pelo motor `marked` antes).
- [ ] Construir lógica para detectar os blocos de código com a tag `mermaid`, invocar o SVG via `mermaid.run()` e substituir o nó no output limpo.
