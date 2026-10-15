---
title: Executar uma nota de conformidade
aliases: [conformance-notes, nota de migração, nota CM, executar nota de conformidade, notas de conformidade]
summary: como a skill dona de um item do catálogo canônico executa uma nota de migração (CM-NNNN) de um filho — o check do catálogo é o juiz, o conteúdo do projeto é editado no lugar, o que é do humano é perguntado e quem registra é o modo conform da bootstrap
tags: [harness, conformidade, catalogo, skills]
status: vivo
atualizado: 2026-10-14
fontes: []
---
<!-- kernel do MJRP Harness · versão 2026-10-14 · fonte d3f64f76 · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition

Uma **nota de migração** (`mjrp-scripts/migrations/CM-NNNN-*.md`, no projeto) é um passo de versão de um item do
**catálogo canônico** (`mjrp-scripts/canonical_catalog.json`): diz o que o projeto precisa ter para ficar conforme, por
quê, e os passos — cada um com a skill que o faz. O modo *conform* da `mjrp-pdlc-bootstrap` entrega as notas pendentes
uma a uma; o humano também pode entregar uma direto. A skill dona do item (`owner_skill`) tem uma tabela com os itens
dela; **esta página é o que vale para todas**.

## Como a skill dona executa uma nota

1. **Leia a nota e o item.** `## O que o filho faz` é a ordem de serviço. O `check` do item no catálogo é o juiz:
   escreva o artefato na forma que ele lê, para passar na primeira rodada.
2. **O artefato é conteúdo do projeto.** Acrescente ou edite no lugar, mantenha o que já está certo e as palavras que
   já estão lá, nunca regenere por cima. Arquivo que muda de forma é copiado antes — nada sai sem cópia. **Quando o
   texto do projeto já cumpre o que a nota quer, não mexa nele para satisfazer um formato mais velho** (a nota pede o
   resultado, não uma grafia).
3. **Artefato novo nasce do modelo da skill dona**, não de memória.
4. **O que é do humano se pergunta, não se adivinha.** Uma aprovação, a escolha entre protótipos, um outcome e sua
   medida, uma dúvida sobre o sentido de um dado existente: pergunta com opções e recomendação. Um chute na forma
   certa passa no check e engana todo leitor depois. O que for ambíguo vai ao humano — nunca é "resolvido" por
   regra do agente.
5. **Devolva o que mudou.** No modo *conform*, a bootstrap roda o check, acrescenta a nota a `conformance.applied` e
   commita; a skill dona **não** escreve `conformance.applied` nem `waived`, e nunca os trailers do humano
   (`Conformance-waiver:`, `Catalog-editorial:`). Chamada direto pelo humano, a skill fecha o trabalho como sempre
   fecha; a próxima rodada do *conform* só registra a nota, porque o check já passa.
6. **Nota que não cabe no projeto** (a cláusula *Quando não se aplica* dela, ou algo que o script não sabe): diga por
   quê e não mude nada. Dispensar é do humano.

## Quem faz o quê

| Quem | O que faz |
|---|---|
| a skill dona | o conteúdo do artefato, pelo procedimento dela |
| o modo *conform* (bootstrap) | a ordem das notas, o check de cada uma, `conformance.applied`, o commit por pathspec, a parada em três rodadas |
| o humano | as decisões que são dele, `waived`, os trailers `Conformance-waiver:` e `Catalog-editorial:` |
| o script (`conformance_check.py`) | o juiz — `--pending`, `--gaps`, `--check-note CM-NNNN` |

**Item de várias donas.** Quando o artefato de um item é feito por várias skills, o dono é o próprio modo *conform*,
que roda o laço e roteia cada lacuna à skill dona dela. É o caso do `product-structure` (CM-0019): o
`product_structure_check.py` lista cada lacuna com a dona (`mjrp-coaching-pm`, `mjrp-writing-reqs`,
`mjrp-specifying-sdd-artifacts`); as decisões de produto vão ao humano em lotes, com recomendação; a parada é por falta de
progresso (duas rodadas sem a contagem cair), não por três rodadas — uma exceção ao § 2 da
ADR-0019, que a ADR aponta aqui no cabeçalho; e a saída é o script
em 0 **e** a tela conferida.

## History

- **2026-10-14 22:08** · **Nota publicada não se reescreve — agora um sensor vê** (P1-3 e P2-3 da verificação dos donos): a CM-0019 e a CM-0003 tinham sido reescritas num ramo depois de publicadas; voltaram aos bytes publicados. O portão do Learn passou a conferir, para toda nota que já está na `main`, que os bytes são os do commit em que ela chegou lá (`published_note_problems`; rascunho de ramo é livre; não há válvula). A mudança que a CM-0019 não podia dizer (a dona agora é a bootstrap; story em Backlog não precisa de release) foi dita pela **CM-0020** (`product-structure` 1→2). O § 2 da ADR-0019 aponta para a exceção da parada em duas rodadas (cabeçalho, nos dois sentidos).

- **2026-10-14 21:21** · O `product-structure` (CM-0019) passa a ser do modo *conform* da `mjrp-pdlc-bootstrap` (decisão
  do MJRP): a skill que rodava o laço sozinha é aposentada, e a regra do item de várias donas entra aqui.

- **2026-10-13** · Nasce da duplicação: o mesmo preâmbulo estava copiado, idêntico, nas oito `reference/conformance-notes.md`
  das skills donas (reconferência do EP-13). Vira uma página do kernel — as skills ficam com a tabela dos itens delas e
  apontam para cá — e ganha a regra do passo 2 (texto que já cumpre a nota não se reescreve) e a do passo 4 (o ambíguo
  vai ao humano).
