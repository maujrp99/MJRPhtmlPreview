# Behavior — MJRPhtmlPreview

> Estados observáveis do que o produto **já faz** — alvo do `points_to` dos requisitos (kernel `requirements-graph`).
> Escrito em 2026-10-05 na migração para o grafo de requisitos (S-79 do harness), **a partir dos Acceptance Criteria
> do antigo `story.md`** (`_archive/2026-10-05-story-md/story.md`): é descrição de onde se vê o que foi entregue, não
> critério novo nem julgamento do MJRP. Estados de tela julgados num protótipo, se vierem, moram no `info-arch.md`.

## Preview

- Texto HTML colado na `textarea` aparece renderizado no `iframe` (via `srcdoc`) em menos de 1 segundo. ^preview-live-render
- O botão "⛶ Preview" esconde o editor e o `iframe` ocupa 100% da tela; "✏️ Editor" volta ao modo split. ^preview-fullscreen
- `src="filename.png"` no HTML colado resolve para a pasta `images/` (`<base href>` injetado), local e no GitHub Pages. ^relative-images-resolved
- A pasta `images/` está no `.gitignore`; em produção as imagens vêm de links de thumbnail do Google Drive, no `localhost` vêm do disco. ^images-kept-private
- Markdown colado aparece renderizado como HTML (via `marked.js`), blocos `mermaid` aparecem como SVG; HTML puro aparece como antes. ^markdown-rendered
- "📂 Open File" abre o file picker do sistema filtrado para `.html`, `.htm` e `.md`; o conteúdo do arquivo substitui a `textarea`, o preview atualiza e o nome do arquivo aparece na UI. ^file-loaded

## Salvar e exportar

- "Download" baixa `preview_[timestamp].html` com o texto exato da `textarea` no momento do clique. ^local-file-downloaded
- "Save to Drive" (habilitado após o BYOK) passa pelo OAuth2 e pelo Google Picker; o `.html` aparece na pasta escolhida e o botão mostra "Salvando..." e "Sucesso" em verde. ^drive-file-saved
- "PDF" abre o diálogo de impressão nativo do navegador só com o conteúdo do `iframe`. ^pdf-print-dialog
- "PNG" baixa uma imagem com o visual do `iframe` (via `html2canvas`; HTML dinâmico pode falhar — UAT-001). ^png-downloaded
- "⚙️ Settings" abre um modal para CLIENT_ID, API_KEY e APP_ID; as chaves ficam no `localStorage` (nunca no Git) e o botão Drive só ativa depois delas. ^google-keys-configured

## Edição no preview

- O toggle "✏️ Edit" torna o corpo do `iframe` editável, com cursor de texto e indicador visual de modo; ao sair, o HTML editado volta para a `textarea`; em Markdown, aparece o aviso "Editing will convert Markdown to HTML"; os exports levam as edições. ^preview-edit-mode
