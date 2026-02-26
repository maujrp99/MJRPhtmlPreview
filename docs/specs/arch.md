# Architecture — MJRPhtmlPreview

> Documentação Arquitetural e Decisões Técnicas.

## System Overview
Um visualizador de HTML client-side puramente estático (Single-page app contido em um único arquivo `index.html` na M1). Não utiliza um backend tradicional nem ferramentas de build (como Webpack ou Vite) inicialmente para garantir atrito zero e máxima simplicidade na distribuição.

## Component Diagram
- **UI Container**: Controlador de eventos DOM e layout flexbox/grid.
- **Code Editor**: Um elemento `<textarea>` com escuta de evento de input contínuo.
- **Preview Engine**: Um `<iframe sandbox="allow-scripts allow-popups">` que recebe conteúdo renderizado de forma isolada via o atributo `srcdoc`. Esta configuração abstrai a necessidade de comunicação baseada em URI e previne algumas restrições CORS.
- **Toolbar Overlay**: Barra de botões com as ações de manipulação do estado (Limpar, Baixar Local).
- **File Exporter**: Função JS que transforma o texto em um Blob (`text/html`) e orquestra o clique forçado numa tag `<a>` para simular download.

## Data Flow
1. Usuário cola (ou digita) a string HTML no *Code Editor*.
2. Event Listener de entrada no *Code Editor* atualiza o *Preview Engine* imediatamente (< 1 segundo).
3. A String em memória (JS Vanilla) é injetada direto na prop `srcdoc` do Iframe.
4. Iframe executa o layout painting nativamente.
5. Em paralelo, clicar em "Download Local" pega a String HTML vigente, converte para Blob e baixa via link virtual no navegador para integração na Vault de notas locais.

## API Integration Design
(Espaço reservado para M2). A API de nuvem (Google Drive Auth + Picker) será isolada do renderizador front-end para modularidade. Até lá, a M1 possui 0 chamadas de rede externas.

## Security Architecture
O ambiente sendo estrito pelo sandboxing do Iframe. Manipulações de script inseridos pelo usuário rodam apenas dentro da caixinha (Sandbox domain) não acessando localStorage nem cookies do domínio onde este index.html viver. Atributos recomendados no iframe: `sandbox="allow-scripts allow-same-origin"`.
