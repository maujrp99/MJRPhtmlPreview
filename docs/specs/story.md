# User Stories — MJRPhtmlPreview

> This file will be populated during the Specify stage.
> See constitution.md for project rules and CHARTER.md for scope.

## Backlog

### [US-01] Como desenvolvedor usando IAs, eu quero colar código HTML em uma área de texto para que eu possa ver instantaneamente o preview renderizado.
**Acceptance Criteria:**
- [x] A aplicação possui um campo de texto (`textarea`) claro para entrada de código.
- [x] A aplicação possui um `iframe` atuando como área de preview.
- [x] Ao colar um HTML válido no campo de texto, a área de preview é atualizada em tempo real (< 1 segundo) com o conteúdo renderizado.
- [x] O comportamento de renderização usa o atributo `srcdoc` no `iframe` para segurança e prevenção de erros de CORS.
**Priority:** High
**Milestone:** M1

### [US-02] Como desenvolvedor, eu quero fazer o download do HTML colado como um arquivo `.html` local para que eu possa salvá-lo facilmente no meu Vault do Obsidian.
**Acceptance Criteria:**
- [x] Existe um botão visível de "Download" (ou "Salvar Local").
- [x] Clicar no botão aciona o download de um arquivo chamado `preview_[timestamp].html`.
- [x] O conteúdo do arquivo baixado reflete o texto exato presente no `textarea` no momento do clique.
**Priority:** High
**Milestone:** M1

### [US-03] Como desenvolvedor, eu quero salvar meu HTML diretamente no meu Google Drive, escolhendo a pasta de destino, para organizar as saídas da IA na nuvem.
**Acceptance Criteria:**
- [ ] O botão "Save to Drive" deve estar habilitado.
- [ ] Ao clicar, o fluxo de OAuth2 do Google (perfil pessoal/corporativo) é acionado.
- [ ] Após o login, o Google Picker Modal aparece para que eu escolha uma pasta no Drive.
- [ ] O conteúdo HTML é salvo como um arquivo `.html` na pasta escolhida.
- [ ] O botão fornece feedback visual de "Salvando..." e "Sucesso" (cor verde).
**Priority:** High
**Milestone:** M2

### [US-04] Como desenvolvedor, eu quero fazer o download da página renderizada como PDF para compartilhamento e arquivamento estático.
**Acceptance Criteria:**
- [ ] Existe um botão na toolbar para "PDF".
- [ ] Ao clicar, o diálogo de impressão nativo do navegador é aberto contendo apenas o conteúdo do `iframe` (evitando imprimir a UI do editor).
**Priority:** Medium
**Milestone:** M2

### [US-05] Como desenvolvedor, eu quero gerar um print/imagem (PNG/JPEG) do HTML renderizado.
**Acceptance Criteria:**
- [ ] A funcionalidade importa e usa uma biblioteca externa (ex. html2canvas) lidando de forma contida com as restrições da arquitetura Vanilla.
- [ ] O download do arquivo de imagem reflete o visual do iframe.
**Priority:** Low
**Milestone:** M3
