# Specification: MJRPhtmlPreview

> Documento de Especificação Técnica do Produto (PRD/Spec). Fonte da Verdade para o que está sendo construído.

## 1. Product Vision e Escopo
Um visualizador rápido, "frictionless" e zero-dependências externas pesado para colar saídas generativas geradas por IAs e ter o preview imediato renderizado na tela. Permite exportação fácil do resultado final (Local, PDF, PNG ou GDrive). O foco primário é velocidade e usabilidade em ambiente seguro (Client-side absoluto).

## 2. Requisitos Funcionais (FR)

### M1: MVP Core (HTML Previewer)
- **FR01.1 [Editor]:** A interface deve possuir um painel para entrada de texto bruto (Textarea).
- **FR01.2 [Live Preview]:** Um `iframe` deverá renderizar o código HTML da Textarea em tempo real usando o atributo protegido `srcdoc` sempre que houver o evento `input`.
- **FR01.3 [Local Export]:** A aplicação deverá gerar arquivo `.html` (via Blob URI) disparando o download nativo.
- **FR01.4 [Clear Action]:** Um botão na barra lateral deverá resetar o DOM e a UI para o estado vazio.

### M2: Integração Google Drive
- **FR02.1 [Auth OAuth]:** O sistema deve oferecer suporte a login Google Account, requisitando o scope `drive.file` usando a Google Identity Services Library, validando em cache (Token silencioso).
- **FR02.2 [Drive Picker]:** View dinâmica baseada na Google Picker API V3 instanciada no callback do Auth pra escolha de pasta destino (`ViewId.FOLDERS`).
- **FR02.3 [File Upload]:** Envio (POST `multipart/related`) inserindo Metadata (nome timestamp) e Base string do Editor em um arquivo novo, com timeout feedback na UX.

### M3: Exportação Multimídia (Polish)
- **FR03.1 [PDF Print]:** Ação via API Nativa `contentWindow.print()` chamando o Iframe Dialog ignorando a Toolbar da aplicação externa.
- **FR03.2 [Image Capture]:** Transição dos Pixels DOM do Iframe p/ Base64 Image (`.png`) injetando dinamicamente e usando a biblioteca `html2canvas`.

### M4: Markdown & Mermaid Parser (Novo)
- **FR04.1 [Interpreter]:** Injeção de bibliotecas `marked.js` e `mermaid.js` suportadas na Engine Client (Zero build). O texto na textarea deverá ser interpretado condicionalmente caso detecte sintaxe `.md`.
- **FR04.2 [Converter Pipeline]:** O sistema passará a conversão `Markdown -> HTML Puro` antes de aplicar ao `<iframe srcdoc>`. Gráficos ````mermaid```` serão cacheados pelo Mermaid Engine e injetados de volta como `svgs` nativos.

## 3. Requisitos Não Funcionais (NFR)
- **NFR01 [Arquitetura Vanilla]:** Nenhuma compilação ou bundler (ex: Webpack, Vite, NodeJS) será necessário no runtime. 100% da regra funcionará direto pelo navegador.
- **NFR02 [Segurança Mútua]:** O iframe alvo deve conter explicitamente a flag sandbox `allow-scripts allow-popups allow-same-origin allow-modals` bloqueando que HTML inseguro afete os tokens da M2 globais.
- **NFR03 [Responsividade]:** O Layout Flex 50/50 Desktop deverá virar um empilhamento "Stack-Y" no mobile mantendo visado a área do editor.

## 4. API & External Contracts
### Contract: Google Identity Services (GSI)
- **Escopos**: `https://www.googleapis.com/auth/drive.file`.
- **Método Adotado**: Multipart Upload via Vanilla Fetch Call no endpoint do GDrive v3.
- **Payload Expectation (JSON)**: `{ "name": "preview_YYYYMMDD_HHMM.html", "mimeType": "text/html", "parents": ["<FOLDER_ID>"] }`
