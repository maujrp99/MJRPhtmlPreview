# UAT — MJRPhtmlPreview
**Status**: Live · **Atualizado**: 2026-09-27 00:05

## Rodada 1 — Export to PNG (`html2canvas`) · registrado antes do harness · migrado do debug log antigo em 2026-09-26

| ID | Contexto | Tipo | Reportado em | Descrição | Status | OK do humano |
|---|---|---|---|---|---|---|
| UAT-001 | Export to PNG (`html2canvas`) · M3 Polish | bug | 2026-02-25 23:19 | HTML com blocos dinâmicos (canvas aninhado, ex.: Chart.js; iframes; animação CSS/SVG) sai em branco ou malformado no PNG — o `html2canvas` recria o DOM sem executar o JS do alvo nem ler canvas/WebGL já renderizados. Esperado: o PNG igual ao que a tela mostra. Caminhos considerados (para refinar): `dom-to-image`; orientar `animation: false` nos gráficos do alvo; screenshot via serviço externo (fere o Zero-Dependency). Prioridade baixa, adiado. | open | |

**Aceite da rodada**: em aberto
