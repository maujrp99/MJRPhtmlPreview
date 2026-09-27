---
title: Cânone de design
aliases: [design-canon, canone de design, cânone de UX, cânone de UI, ux canon, design canon]
summary: as fontes elevadas que fundamentam UX, UI e conteúdo explicativo no MJRP — organizadas em sete disciplinas com regras de ID estável que as skills citam em vez de recitar
tags: [harness, design, ux, kernel]
status: vivo
atualizado: 2026-09-19
fontes: [few-information-dashboard-design, tufte-visual-display, knaflic-storytelling-with-data, wexler-big-book-of-dashboards, shneiderman-the-eyes-have-it, nngroup-dashboards-preattentive, smashing-dashboard-decluttering, a11y-collective-accessible-charts, sigma-color-blindness, 925studios-whoop-breakdown, sahha-readiness-scores, nielsen-ten-heuristics, krug-dont-make-me-think, cooper-about-face, yablonski-laws-of-ux, google-apple-m3-hig, w3c-wcag-2-2, gigerenzer-risk-communication, case-calm-technology, cdc-clear-communication-index, andrews-info-we-trust]
---
<!-- kernel do MJRP Harness · versão 2026-09-27 · fonte d42894e · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
O **cânone de design** é o corpo de referência externo que fundamenta as regras de UX, UI e
conteúdo explicativo do MJRP — 21 fontes fichadas em `docs/sources/`, organizadas em sete
disciplinas, cada regra com um **ID estável** que as skills de design citam em vez de recitar.
A barra de qualidade não vem do gosto do agente: vem daqui. É **referência inicial, não teto** —
o cânone cresce com o que os projetos-filho descobrem (ver § *Como o cânone evolui*).

> **Por que existe (19/09/2026).** O MJRP, no `mjrp-health-control`: *"hoje acredito que as
> skills mjrp quanto a UX e UI são bem pobres"*. A auditoria de lá (`ux-audit.md`, 36 princípios
> contra as telas) provou que o julgamento é possível — e mostrou que recitar o princípio dentro
> da auditoria incha o documento. Os princípios moram aqui; a auditoria, a skill e o spec **citam
> o ID**.

## What it is

### Como ler as regras

Cada regra tem três partes: **ID** (estável — nunca se renumera; regra retirada fica marcada
*retirada*, o número não é reusado), **a regra** escrita como teste (pass/fail, não direção) e o
**tipo**:

- **produção** — a skill produtora aplica no momento de desenhar; teria mudado o código se
  existisse. É o que `mjrp-ux-ui-designer`, `mjrp-interface-designer`, `mjrp-design-system` e
  `mjrp-content-designer` carregam como checklist.
- **julgamento** — não dá para impor na produção; só se pega na crítica. É o que só a
  `mjrp-ux-critic` verifica.

A `mjrp-ux-critic` verifica os dois tipos. A fonte de cada regra é a ficha em `docs/sources/`;
o *porquê* mora lá e nesta página, nunca na skill.

### HI · Hierarquia

| ID | Regra (testável) | Tipo | Fonte |
|---|---|---|---|
| **HI-01** | O maior elemento da tela é o veredito ou a métrica principal — nunca o rótulo de categoria, a marca ou a navegação. Tamanho = importância. | produção | Few; Knaflic; 925 Studios |
| **HI-02** | Toda tela abre com a resposta (BLUF/answer-first): um veredito ou número no topo, antes de qualquer gráfico ou tile. | produção | Knaflic; Wexler; CDC (mensagem principal primeiro) |
| **HI-03** | Marca do produto e categoria têm posição fixa e discreta em todas as telas; não competem com o conteúdo. | produção | Krug (billboard, convenção); Cooper (postura) |
| **HI-04** | Só comprimento e posição 2D codificam quantidade com precisão; cor, área e ângulo são cue secundário — nunca o único canal de magnitude. | produção | NN/g preattentive; Tufte |
| **HI-05** | A atenção é dirigida com um atributo pré-atentivo por vez (cor de destaque única, tamanho ou posição); dois destaques competindo = nenhum destaque. | julgamento | Knaflic; NN/g; Few |
| **HI-06** | Há um elemento de destaque claro por tela (Von Restorff); se tudo é destaque, a regra falha. | julgamento | Yablonski |

### DE · Densidade

| ID | Regra (testável) | Tipo | Fonte |
|---|---|---|---|
| **DE-01** | A visão de monitorar cabe em ~1 viewport, sem rolar; profundidade é *details-on-demand*, não scroll. | produção | Few (single screen, at a glance); Shneiderman |
| **DE-02** | Todo pixel que não é dado nem estrutura necessária é removido: gridlines pesadas, bordas, fundos, 3D, ícones decorativos. | produção | Tufte (data-ink); Few (non-data pixels); Smashing |
| **DE-03** | Decluttering não é simplificar o conteúdo: remove-se ruído, não informação. Uma tela pode ser densa e limpa. | julgamento | Smashing; Tufte (elegância) |
| **DE-04** | Nenhuma escolha com mais de ~7 opções visíveis sem agrupamento; nenhum menu ou conjunto de ações sem hierarquia (Hick, Miller). | produção | Yablonski; Krug |
| **DE-05** | Produto multi-domínio começa **overview-first**: uma tela de visão geral com um card por domínio (com sparkline/estado), depois zoom e filtro, depois detalhe. | produção | Shneiderman (mantra); Wexler |
| **DE-06** | Ao adicionar dado novo, abre-se uma porta nova (tela/aba) — não se empilha no mesmo tile. | produção | 925 Studios; Cooper (excise) |

### CO · Conteúdo explicativo

| ID | Regra (testável) | Tipo | Fonte |
|---|---|---|---|
| **CO-01** | Toda métrica não-óbvia tem definição de uma linha, em linguagem simples, ao lado da métrica — não em glossário separado. | produção | CDC (letramento é do emissor); Andrews |
| **CO-02** | Todo gráfico incomum tem um "como ler" de uma a duas linhas. | produção | Andrews (anotação como guia); Knaflic |
| **CO-03** | O conteúdo explicativo fica **acima** do gráfico ou do número que explica, nunca abaixo nem em tooltip apenas (regra do MJRP, 19/09). | produção | MJRP (health-control Wave 2); CDC (mensagem principal primeiro) |
| **CO-04** | Nenhum número sem referência: baseline, meta, Δ ou micro-tendência (sparkline) ao lado do valor. Número puro é achado. Sparkline é uma *forma* da referência, não regra própria (decisão 21/09, teste da `ux-critic`). | produção | Wexler (KPI com contexto); Few (bullet graph) |
| **CO-05** | Todo número diz o que fazer ou o que significa (CDC item 16): "X — abaixo da sua média; nada a fazer" vale; "X" sozinho não. | produção | CDC; Gigerenzer |
| **CO-06** | Voz ativa, uma ideia por frase, palavra do dia a dia; jargão só com definição inline. | produção | CDC; Krug (omit needless words) |
| **CO-07** | Anotação de insight (o que este gráfico mostra de relevante) aparece no próprio gráfico, não só no texto ao redor. | julgamento | Knaflic; Andrews |
| **CO-08** | O explicativo (CO-01/02/03) tem peso visual de **guia de leitura**, não de rodapé: rótulo/eyebrow, fundo ou borda, cor de texto plena (não *muted*) — o bastante para ser lido antes do gráfico, nunca maior que o veredito (HI-05/06). Explicativo em cor de nota, sem rótulo e sem separação do fundo é achado. | produção | Knaflic (anotação precisa de proeminência); NN/g (hierarquia dirige a leitura); MJRP (health-control R23c, 21/09) |

### CP · Composição

| ID | Regra (testável) | Tipo | Fonte |
|---|---|---|---|
| **CP-01** | Mesmo esqueleto para o mesmo tipo de tela: todos os domínios/seções do mesmo nível usam o mesmo template (zonas, ordem, componentes). | produção | Wexler (consistência entre views); Nielsen H4 |
| **CP-02** | Uma pergunta por tela: a tela responde a uma pergunta declarável em uma frase; se responde a duas, são duas telas. | produção | Wexler (scenario-driven); 925 Studios |
| **CP-03** | Sequência de leitura segue o olho (topo-esquerda → baixo-direita em LTR); o mais importante ocupa o quadrante de entrada. | produção | Few; Krug (scan) |
| **CP-04** | Elementos relacionados agrupados por proximidade e alinhamento; relação que precisa de linha ou caixa para existir é relação mal composta. | produção | Few; Tufte |
| **CP-05** | Small multiples para comparar séries do mesmo tipo — não um gráfico com 8 linhas. | produção | Tufte |
| **CP-06** | Convenção de plataforma antes de invenção: navegação, gestos, alvos e estados seguem Material/HIG; desvio é decisão registrada, não default. | produção | Google/Apple; Krug; Jakob's Law |
| **CP-07** | Fundo escuro ou claro é decisão com função declarada (contexto de uso, paleta), não estética; o design system registra o porquê. | julgamento | 925 Studios; palette-library |

### IN · Interação

| ID | Regra (testável) | Tipo | Fonte |
|---|---|---|---|
| **IN-01** | Overview → zoom & filter → details-on-demand: a interação segue o mantra; detalhe nunca esconde o contexto de onde veio. | produção | Shneiderman |
| **IN-02** | Período/tempo tem controle direto: presets + navegação ‹/› + range; nenhum filtro só por tooltip. | produção | Shneiderman (zoom e filtro como controle direto); Cooper (modeless) |
| **IN-03** | Alvo de toque ≥ 44×44 pt (HIG) / 48×48 dp (Material); WCAG 2.5.8 mínimo 24×24. | produção | Google/Apple; WCAG 2.2 |
| **IN-04** | Resposta < 400 ms ou feedback de progresso visível (Doherty); status do sistema sempre visível (Nielsen H1). | produção | Yablonski; Nielsen |
| **IN-05** | Toda ação destrutiva tem desfazer ou confirmação proporcional ao dano (Nielsen H3, H5); nenhum "delete" a um clique sem saída. | produção | Nielsen; Cooper (forgiveness) |
| **IN-06** | Estados vazio, carregando, erro e offline existem e dizem o que fazer — tela sem estado vazio desenhado é achado. | produção | Nielsen H1, H9; Cooper |
| **IN-07** | Interatividade custa acessibilidade: o estático é o default; interação é camada adicional que não remove o acesso ao dado. | julgamento | A11Y Collective |
| **IN-08** | O fim do fluxo é desenhado com cuidado (Peak-End): a última tela confirma, resume e aponta o próximo passo. | julgamento | Yablonski |

### AH · Acessibilidade e honestidade

| ID | Regra (testável) | Tipo | Fonte |
|---|---|---|---|
| **AH-01** | Contraste ≥ 4.5:1 texto normal, ≥ 3:1 texto grande e componentes de UI (WCAG 1.4.3, 1.4.11). | julgamento | WCAG 2.2; A11Y Collective |
| **AH-02** | Cor nunca é o único diferenciador: rótulo direto, padrão ou forma como redundância (WCAG 1.4.1). Paleta categórica testada para daltonismo. | julgamento | Sigma; A11Y Collective; WCAG |
| **AH-03** | Todo gráfico tem alternativa textual em três níveis: alt de uma frase, resumo do que mostra, tabela de dados acessível. | produção | A11Y Collective; WCAG 1.1.1 |
| **AH-04** | Tudo alcançável por teclado, foco visível, ordem de foco = ordem visual (WCAG 2.1.1, 2.4.7, 2.4.3). | julgamento | WCAG 2.2 |
| **AH-05** | Integridade gráfica: a variação visual é proporcional à variação do dado (lie factor ≈ 1); eixo começa em zero para barras; nenhum 3D. | julgamento | Tufte; NN/g |
| **AH-06** | Precisão honesta: casas decimais limitadas pela qualidade do dado, não pela planilha; incerteza declarada em palavras simples. | produção | Gigerenzer; Andrews |
| **AH-07** | Score composto mostra os fatores, não só a nota; janela, escala e pergunta que ele responde são explícitas. | produção | Sahha; Gigerenzer |
| **AH-08** | Uma cor, um conceito, em todo o produto (consistência semântica); a mesma cor não significa duas coisas. | produção | Sigma; Wexler |

### RC · Comunicação de risco e calm technology

| ID | Regra (testável) | Tipo | Fonte |
|---|---|---|---|
| **RC-01** | Risco em frequência natural ("3 em cada 100"), com denominador fixo e explícito, antes de qualquer percentual. | produção | Gigerenzer |
| **RC-02** | Nunca variação relativa sem a base absoluta ao lado ("+30%" → "de 2 para 3 em cada 1.000"). | produção | Gigerenzer |
| **RC-03** | Classe de referência sempre visível: por pessoa, por dia, por medição — número sem classe é ambíguo por construção. | produção | Gigerenzer |
| **RC-04** | Nenhum resultado apresentado como certeza: margem de erro e falso positivo/negativo fazem parte do valor, não do rodapé. | julgamento | Gigerenzer (ilusão de certeza) |
| **RC-05** | Comparação de opções com trade-off usa o padrão *fact box*: benefícios e danos lado a lado, números absolutos, mesma escala. | produção | Gigerenzer / Harding Center |
| **RC-06** | A tecnologia pede a menor quantidade de atenção possível: o normal vive na periferia; só a exceção vem ao centro. | produção | Case (princípios I, III) |
| **RC-07** | Informar **e** acalmar: alerta é proporcional ao dano e reversível; nenhum alarme para o que não pede ação. Contra a sobrecarga de notificação. | julgamento | Case (princípio II); Gigerenzer |
| **RC-08** | Funciona mesmo quando falha: sem dado, a tela diz o que falta e o que ainda vale, em vez de tela vazia ou número zerado. | produção | Case (princípio VI); Nielsen H9 |
| **RC-09** | Tom não-clínico em dado de saúde: linguagem de bem-estar, sem vermelho/alarme por default; cor de alerta reservada ao que exige ação. | produção | Case; 925 Studios; palette-library (Zen/Calma) |

## O que é opinião de gênero ou de contexto

> **A regra de leitura:** o cânone vale para dashboard, formulário, fluxo e documento. O que só
> vale num gênero é regra de projeto — mora na `constitution.md` ou no `design-system.md` dele.

| O que a fonte diz | Por que não é universal |
|---|---|
| **"Cabe em 1 viewport"** (Few, DE-01) | é regra de *monitoramento*; exploração, leitura longa e formulário rolam por natureza |
| **Fundo escuro** (WHOOP) | opinião de produto; o gênero e a paleta decidem (CP-07) |
| **Um número resume tudo** (WHOOP, Sahha) | funciona em wearable; em finanças ou obra o composto esconde o fator que importa (AH-07 já corrige) |
| **Estático é o default** (A11Y Collective, IN-07) | vale para gráfico publicado; ferramenta de análise é interativa por definição — a regra vira "acessível *também* estático" |
| **Frequências naturais** (Gigerenzer, RC-01) | obrigatório em saúde e finanças; num dashboard de latência, "p95 = 240 ms" é a forma certa |
| **Convenções de 2000** (Krug: web desktop) | o *princípio* (não me faça pensar) é universal; os exemplos de navegação são datados |
| **Postura sovereign/transient** (Cooper) | pré-mobile; em app de bolso a postura muda por contexto, não por produto |

## Como o cânone evolui

O cânone é **referência inicial, não limitante** (MJRP, 19/09/2026). Três mecanismos:

1. **Busca antes de assumir.** Toda skill de design carrega a regra: *quando a necessidade do
   projeto não estiver coberta por um ID daqui, buscar na web se existe fonte elevada para ela
   antes de decidir por conta própria* — e registrar o que achou, inclusive o que decidiu não
   usar (mesma disciplina do tools-catalog). Fonte nova que sustenta regra nova vira ficha em
   `docs/sources/` e regra com ID aqui. **E a skill também muda** (emenda do MJRP, 19/09): se o
   contexto do projeto revelou conceitos ou regras que ajudam de verdade, a skill se refina com a
   `mjrp-skill-refiner` — o cânone guarda o *o que é*; a skill incorpora o *como* que o projeto
   ensinou. Skill viva aprende nos dois lugares.
2. **Retroalimentação dos projetos-filho.** Achado de UX/UI num projeto-filho entra pela pasta
   `docs/harness-feedback/` dele; o sensor do harness traz para o intake (EP-90 do `prd.md`);
   o que vira regra sobe com o antes/depois como evidência. As cinco primeiras regras assim
   (HI-01, HI-02, DE-05, CO-04, CO-01/CO-03) vieram do `mjrp-health-control`.
3. **Regra retirada não some.** Fica marcada *retirada*, com data e motivo, no `## History`; o
   ID não é reusado — a auditoria antiga que o citava continua legível.

## How MJRP uses it

- **Esta página é do kernel** — vai carimbada para dentro de todo projeto em
  `docs/wiki/harness/`, e o I5 do `doctor` confere que chegou e que o carimbo não envelheceu.
- **Lê-se sob demanda.** Quem vai desenhar uma tela, escrever o texto dela ou julgá-la abre;
  as skills de design citam o ID e mandam ler daqui. Nenhuma sessão carrega o cânone inteiro.
- **As skills que citam:** `mjrp-ux-ui-designer` (2a — HI, DE-05, CP, IN), `mjrp-design-system`
  (2b — AH-01/02/08, CP-07), `mjrp-interface-designer` (2c — HI, DE, CP, IN), `mjrp-content-designer`
  (CO, AH-06/07, RC), `mjrp-ux-critic` (tudo, os dois tipos), `mjrp-infographic-designer` (CO, HI,
  AH no toolkit).
- **Quando o cânone e o projeto discordarem, o projeto decide** — desde que a decisão esteja
  escrita na `constitution.md` ou no `design-system.md` dele, e desde que não contrarie um
  princípio do `PRINCIPLES.md`.

## History

> A decisão mora na página do assunto que ela muda, com data (ADR-0008).
- **2026-09-19 14:40** · **A página nasce do EP-07 (Discovery & Prototipação).** Brief aprovado
  pelo MJRP com três emendas: sem checkpoints (iterar depois); reescrever skill datada ou
  limitante está no escopo; o cânone é referência inicial — skills vivas, com regra de buscar na
  web o que não está aqui. 21 fontes fichadas em `docs/sources/` no mesmo turno; 51 regras em
  sete disciplinas; IDs estáveis. Entra no **kernel** por decisão dele (opção entre
  `docs/wiki/` e `docs/wiki/kernel/`). Fonte da estrutura: `design/proposals/design-skills-consolidation-proposal.md`
  v2 e o parecer do `mjrp-health-control` (`docs/harness-feedback/2026-09-19-design-skills.md`).

- **2026-09-21 15:49** · **Primeiro retorno do campo em 48 h.** Dois pareceres do `mjrp-health-control`
  (`docs/wiki/feedback-from-other-projects/2026-09-20-ux-critic-test-run.md` e
  `2026-09-21-co08-explicativo-peso-de-guia.md`): (1) a `mjrp-ux-critic`, rodada do zero por ID,
  redescobriu 12 dos 13 achados da auditoria manual — o cânone e o formato do juiz se sustentam;
  (2) **CO-08 entra** como regra de produção (explicativo com peso de guia) — o defeito só era pego
  no julgamento via HI-05/06, agora nasce certo; a alternativa "emendar CO-03" foi recusada porque
  CO-03 governa *onde* e CO-08 governa *quanto peso*. O gap do sparkline (A7) foi **subsumido em
  CO-04** (sparkline é forma da referência), sem ID novo — opção (a) do parecer.

## Related
[[engineering-canon]] · palette-library · [[harness-elements]] · [[terms]] · [[harness-kaizen]] · [[doctor]]
