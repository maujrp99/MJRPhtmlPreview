# Debug Log & Known Issues

## Component: Export to PNG (`html2canvas`)
**Status:** Open / Deferred
**Priority:** Low (M3 Polish)
**Description:**
A captura de tela em formato PNG via `html2canvas` falha ao renderizar corretamente HTMLs compostos por blocos altamente dinâmicos, gráficos renderizados via canvas aninhados (ex: Chart.js configurado no target HTML), iframes internos ou animações CSS/SVG complexas. A biblioteca tira a "foto" ignorando os pixels manipulados diretamente no canvas alvo ou capta o estado inicial da animação resultando em blocos em branco ou malformatados.
**Root Cause Hypothesis:**
O `html2canvas` varre a árvore do DOM recriando os nós em um canvas próprio, processo este que não executa o Javascript contido no layout alvo nem interpreta WebGL/Canvas preexistentes renderizados externamente sem que configurações específicas (como repintar o chart antes da captura) sejam injetadas no próprio script alvo.
**Potential Workarounds (For Future Refinement):**
- Explorar bibliotecas alternativas (ex: `dom-to-image`).
- Orientar o usuário a forçar `animation: false` nos scripts dos gráficos a serem renderizados.
- Substituir a abordagem inteira por uma chamada a uma API externa de Screenshot (como Puppeteer rodando num Cloud Function), o que violaria o manifesto Zero-Dependency.
