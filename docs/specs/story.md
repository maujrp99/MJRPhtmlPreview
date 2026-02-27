# User Stories — MJRPhtmlPreview

> Histórico cumulativo de User Stories com Acceptance Criteria rastreáveis.

## Backlog

### [US-01] Como desenvolvedor usando IAs, eu quero colar código HTML em uma área de texto para que eu possa ver instantaneamente o preview renderizado.
**Acceptance Criteria:**
- [x] A aplicação possui um campo de texto (`textarea`) claro para entrada de código.
- [x] A aplicação possui um `iframe` atuando como área de preview.
- [x] Ao colar um HTML válido no campo de texto, a área de preview é atualizada em tempo real (< 1 segundo) com o conteúdo renderizado.
- [x] O comportamento de renderização usa o atributo `srcdoc` no `iframe` para segurança e prevenção de erros de CORS.
**Priority:** High | **Milestone:** M1 | **Status:** ✅ Done

### [US-02] Como desenvolvedor, eu quero fazer o download do HTML colado como um arquivo `.html` local para que eu possa salvá-lo facilmente no meu Vault do Obsidian.
**Acceptance Criteria:**
- [x] Existe um botão visível de "Download" (ou "Salvar Local").
- [x] Clicar no botão aciona o download de um arquivo chamado `preview_[timestamp].html`.
- [x] O conteúdo do arquivo baixado reflete o texto exato presente no `textarea` no momento do clique.
**Priority:** High | **Milestone:** M1 | **Status:** ✅ Done

### [US-03] Como desenvolvedor, eu quero salvar meu HTML diretamente no meu Google Drive, escolhendo a pasta de destino, para organizar as saídas da IA na nuvem.
**Acceptance Criteria:**
- [x] O botão "Save to Drive" deve estar habilitado (após configuração BYOK).
- [x] Ao clicar, o fluxo de OAuth2 do Google é acionado.
- [x] Após o login, o Google Picker Modal aparece para que eu escolha uma pasta no Drive.
- [x] O conteúdo HTML é salvo como um arquivo `.html` na pasta escolhida.
- [x] O botão fornece feedback visual de "Salvando..." e "Sucesso" (cor verde).
**Priority:** High | **Milestone:** M2 | **Status:** ✅ Done

### [US-04] Como desenvolvedor, eu quero fazer o download da página renderizada como PDF para compartilhamento e arquivamento estático.
**Acceptance Criteria:**
- [x] Existe um botão na toolbar para "PDF".
- [x] Ao clicar, o diálogo de impressão nativo do navegador é aberto contendo apenas o conteúdo do `iframe`.
**Priority:** Medium | **Milestone:** M2 | **Status:** ✅ Done

### [US-05] Como desenvolvedor, eu quero gerar um print/imagem (PNG) do HTML renderizado.
**Acceptance Criteria:**
- [x] A funcionalidade importa e usa a biblioteca `html2canvas`.
- [x] O download do arquivo de imagem reflete o visual do iframe.
- [x] ⚠️ Limitação conhecida: HTML dinâmico (canvas, charts) pode falhar. Documentado em `docs/debug-log.md`.
**Priority:** Low | **Milestone:** M3 | **Status:** ✅ Done

### [US-06] Como desenvolvedor, eu quero configurar minhas chaves da API do Google sem expô-las no código-fonte público.
**Acceptance Criteria:**
- [x] Existe um botão ⚙️ Settings na toolbar que abre um modal.
- [x] O modal permite inserir CLIENT_ID, API_KEY e APP_ID.
- [x] As chaves são salvas no `localStorage` do navegador (nunca no Git).
- [x] O botão Drive só é ativado após as chaves serem configuradas.
- [x] O arquivo `config.js` foi eliminado da arquitetura.
**Priority:** High | **Milestone:** M3.5 | **Status:** ✅ Done

### [US-07] Como desenvolvedor, eu quero ver o preview em tela cheia, escondendo o editor, para apresentar ou avaliar o resultado final.
**Acceptance Criteria:**
- [x] Existe um botão "⛶ Preview" na toolbar que esconde o painel do editor.
- [x] O iframe ocupa 100% da tela em modo fullscreen.
- [x] Um botão "✏️ Editor" permite retornar ao modo split.
**Priority:** Medium | **Milestone:** Session 02/26 | **Status:** ✅ Done

### [US-08] Como desenvolvedor, eu quero que imagens com caminhos relativos no meu HTML sejam resolvidas automaticamente.
**Acceptance Criteria:**
- [x] O sistema injeta automaticamente `<base href="...images/">` no HTML renderizado.
- [x] Usar `src="filename.png"` resolve corretamente (local e GitHub Pages).
**Priority:** Medium | **Milestone:** Session 02/26 | **Status:** ✅ Done

### [US-09] Como desenvolvedor, eu não quero que imagens sensíveis fiquem públicas no repositório GitHub.
**Acceptance Criteria:**
- [x] Pasta `images/` adicionada ao `.gitignore`.
- [x] Imagens servidas via Google Drive thumbnail links em produção.
- [x] Imagens locais funcionam no `localhost` para desenvolvimento.
**Priority:** High | **Milestone:** Session 02/26 | **Status:** ✅ Done

### [US-10] Como desenvolvedor, eu quero colar texto em Markdown (incluindo diagramas Mermaid) e ver o resultado renderizado, sem precisar converter manualmente para HTML.
**Acceptance Criteria:**
- [x] O sistema detecta automaticamente se o input é Markdown ou HTML.
- [x] Markdown é convertido para HTML via `marked.js` antes de ser injetado no iframe.
- [x] Blocos ````mermaid```` são renderizados como SVGs nativos via `mermaid.js` (lazy-loaded).
- [x] HTML puro continua funcionando sem alteração.
**Priority:** High | **Milestone:** M4 | **Status:** ✅ Done

