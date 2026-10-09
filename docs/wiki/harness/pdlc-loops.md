---
title: PDLC em loops — Intake, Discovery, Delivery, Learn
aliases: [pdlc-loops, PDLC, ciclo de vida, lifecycle, loops do PDLC, Intake, triagem, trilhas, tracks, Full, Standard, Fast track, Fix, Discovery loop, Delivery loop, Learn loop, contrato, escalada, merge do agente]
summary: o ciclo de vida do produto no MJRP como uma fundação e três loops — Intake com quatro trilhas, Discovery (o que construir), Delivery (construir certo) e Learn (deu certo?) —, cada um com critério de saída, verificador e regras de parada; o humano na intenção e no risco de negócio
tags: [kernel, pdlc, loop, discovery, delivery, processo]
status: em formação
atualizado: 2026-10-09
fontes: [kernel/ways-of-working/product-discovery, kernel/ways-of-working/loop-engineering-concept, kernel/design/sketch-vs-prototype, kernel/roadmap/requirements-graph, wiki/sources/2026-10-07-mjrp-product-discovery-handbook.md, wiki/sources/2026-10-07-mjrp-loop-engineering-handbook.md, wiki/sources/2026-10-07-mjrp-agentic-ai-handbook.md]
---
<!-- kernel do MJRP Harness · versão 2026-10-09 · fonte 9e9312e · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

# PDLC em loops — Intake, Discovery, Delivery, Learn

> Kernel · página de processo · criada 2026-10-07 · nasce da proposta `design/proposals/pdlc-loop-engineering-proposal.md`
> (decisões do MJRP de 2026-10-07, 18:02 a 18:30) · diagrama oficial: `design/diagrams/ways-of-working/2026-10-09-1318-pdlc-loops-v4.png`
> (os loops no topo; o fluxo dos artefatos e das skills embaixo) · substitui a numeração de fases (0 · 1a · 1b · 2 · 2→3 · 3 · 4 · 5),
> que as skills ainda usam até migrarem — a §11 traduz.

## Definition

O **PDLC do MJRP** é uma **fundação** e **três loops** — **Discovery** (o que construir), **Delivery** (construir certo) e
**Learn** (deu certo?) — alimentados por uma porta de entrada única, o **Intake**, que põe cada demanda numa **trilha**
(Full · Standard · Fast track · Fix). Cada loop tem um critério de saída, um verificador e regras de parada; o humano
entra onde a intenção é definida e onde há risco de impacto financeiro ou de negócio. Cada papel é uma vaga: hoje uma
skill, amanhã um agente.

## 0. Como ler

- **Fase não é portão definitivo; é uma volta** (`PRINCIPLES.md` II.10). Qualquer loop pode devolver trabalho a outro.
- **Toda demanda entra pelo Intake** — inclusive o que volta do UAT, dos sensores e do Learn. Nenhum loop recebe
  trabalho por fora.
- **O que decide se um loop continua é o harness, não o auto-relato do agente** (II.3): o verificador passa ou não, e as
  regras de parada cortam o resto.
- **"A maioria das tarefas ainda não precisa de um loop"** (Garage Labs): o Discovery é interativo; o Delivery é
  goal-based; o Learn roda agendado. O processo não força autonomia onde não há verificador.

## 1. Fundação — o ambiente dos loops

Não é fase: é onde os loops rodam, montada uma vez (`mjrp-pdlc-bootstrap`) e revista quando muda.

| Peça | Onde mora |
|---|---|
| Contrato | `.mjrp-project.yml` (formato dos requisitos, `gates:`, sensores, stack) |
| Intenção | `VISION.md`, `PRINCIPLES.md`, `constitution.md` |
| Guias | kernel e skills |
| Sensores | `doctor.py`, sensores do contrato, `daily-checks/` |
| Arquitetura | `arch.md`, `data-model.md`, `design-system.md` — quando prontos, liberam o Fast track |

## 2. Intake — a porta de entrada e as trilhas

**Intake** é a triagem: receber a demanda, qualificar (vale a pena? serve a qual resultado do `ROADMAP.md`?), escolher a
trilha — ou rejeitar com motivo. Entra: pedido ou mudança do MJRP, requisito novo, bug do UAT, achado de sensor,
aprendizado do Learn. Mora no `prd.md` de cada projeto (§ *Candidatos*) e na entrada do log da triagem. No sentido amplo,
Intake é a pré-venda (captar a oportunidade, estimar, mandar proposta) — vale quando houver cliente; hoje é a triagem.

| Trilha | Quando | Caminho |
|---|---|---|
| **Full** | resultado novo ou produto novo | Discovery inteira |
| **Standard** | feature nova num resultado que já existe | explorar (ligado por padrão, pode pular) → enquadrar leve → desenhar |
| **Fast track** | arquitetura e design system prontos, sem risco novo | protótipo rápido → requisitos Ready tirados do inventário → Delivery |
| **Fix** | bug ou ajuste dentro do contrato | direto ao Delivery |

A elegibilidade do Fast track se confere por máquina (arquitetura aprovada, design system existe, resultado no ROADMAP);
o sensor diz se cabe, o humano escolhe.

## 3. Loop Discovery — o que construir

Interativo; o avaliador é o humano, com o juiz de UX. Pelas fontes de produto (Cagan, Torres, Perri, Olsen), **design é
Discovery**: as três estações são uma só volta.

1. **Explorar** — prototipação rápida, ligada por padrão, pode pular (sketch-vs-prototype). Saída: `design/inception/`
   vN, `inception-notes.md` e, na mesma rodada, a descrição da tela (texto, inventário com o wireframe em
   `design/wireframes/`, `info-arch.md`). **A tela e a descrição dela são uma atividade só**, de uma dona só
   (`mjrp-designing-ui`) — não etapas em sequência.
2. **Enquadrar** — Rapid × Full ([[product-discovery]]): problema, resultado e medida, os quatro riscos como teste, a
   premissa mais arriscada, matar · iterar · avançar. **A entrada principal é o protótipo aprovado e o seu inventário**; cada item termina numa **função do produto**
   (declarada no `VISION.md`: informar, ajudar a decidir, agir…) ou num **resultado** — informação é produto mesmo sem
   mover resultado —, ou é cortado com motivo.
3. **Desenhar** — a tela e a descrição dela convergem juntas (`info-arch.md`, com o inventário completo e as lacunas) ·
   o sistema visual (`design-system.md`), aplicado quando a estrutura assentou · o protótipo julgado
   (`design/prototypes/` + auditoria de UX sem P0).

**Saída:** requisitos Ready que cobrem o inventário do protótipo — todo item com destino (coberto, evoluído, cortado com
motivo). **Verificador:** o humano e o juiz de UX (LLM de apoio, nunca juiz único) + os sensores do inventário e do grafo.

## 4. O contrato

O ponto único entre Discovery e Delivery: os requisitos Ready, com os critérios apontando para estados julgados. É a
decisão de intenção do humano — um erro aqui o loop repete dezenas de vezes antes de alguém ver. Aprovar a spec e as
tasks é **opção do contrato** (`gates:`), não padrão.

## 5. Loop Delivery — construir certo, por feature

Goal-based (nível 2 da escada da Anthropic); o verificador é determinístico.

- **Estações:** especificar (`spec.md`) → planejar (`plan.md`) → quebrar (`tasks.md`) → executar ⇄ verificar (testes,
  sensores, grafo).
- **Pronto** = o verificador passa (exit 0); nunca o auto-relato do agente.
- **Parada:** teto de voltas, orçamento de tokens, sem progresso (o diff zerou por duas voltas) → escala.
- **Escalada em três níveis:** o código falhou → corrige e verifica de novo · a spec está errada → para e volta ao
  contrato (emenda com o humano; requisito entregue não se edita — nó novo com `supersedes`) · a premissa caiu → volta à
  Discovery.
- **Branch e PR por feature.** O PR leva a evidência (requisitos cobertos, verificador verde, link da spec); o CI roda o
  mesmo verificador, que o agente não altera. **O merge é do agente** quando o verificador passa; o que ele quebrar, ele
  corrige. O merge aparece no Control Center; o humano decide — não executa — só quando pede ou quando há risco de impacto
  financeiro ou de negócio (apagar ou quebrar algo e perder o cliente). **Pré-condição:** tudo versionado, rollback
  possível e backup recorrente do repositório.
- **Isolamento:** a trava de sessão basta com um agente por vez; o worktree por feature entra com agentes em paralelo.

## 6. UAT — a fronteira

O aceite do humano sobre o entregue rodando (`uat.md`): aceito → nó Accepted e operação; bug ou mudança → Intake (trilha
Fix ou Standard). Junto dele, a fronteira irreversível (publicar, deploy).

## 7. Loop Learn — deu certo?

Agendado ou por evento; roda sem o humano. Operar e observar (sensores diários, Control Center) → medir o resultado (a
medida do `ROADMAP.md` mexeu?) → kaizen ([[harness-kaizen]]: a lição vai para a fundação). O que aprende volta pelo Intake.

- **Documento que envelheceu:** a auditoria (`mjrp-auditing-docs`) marca quem decide cada achado. O agente aplica
  (`mjrp-syncing-docs`) o que a evidência prova e está fora do contrato; o humano decide só o que é dele — o contrato
  (PRD, `ROADMAP.md`, escopo ou critério de um requisito), o que pode ser defeito (o código talvez seja o lado errado) e
  o que não dá para decidir. Tudo fica no log e no Control Center.

## 8. Papéis — as vagas de agente

| Loop | Papéis (skill de hoje) |
|---|---|
| Intake | triador (`mjrp-structuring-requests`, `mjrp-pdlc`) |
| Discovery | designer de UI — a tela e a descrição dela, numa atividade só (`mjrp-designing-ui`) · coach de produto (`mjrp-coaching-pm`) · analista (`mjrp-writing-reqs`) · designer de identidade (`mjrp-defining-design-systems`) · juiz de UX (`mjrp-critiquing-ux`) · arquiteto (`mjrp-designing-architecture`) |
| Contrato | analista (`mjrp-writing-reqs`, Ready) · registro (`mjrp-recording-decisions`) · gate (`mjrp-ensuring-sdd`) |
| Delivery | especificador (`mjrp-specifying-sdd-artifacts`) · executor (`mjrp-implementing-tasks`, `mjrp-debugging`) · verificador (`mjrp-ensuring-sdd`, `mjrp-assessing-code-quality`) |
| UAT | QA (`mjrp-ensuring-quality`) · documentador (`mjrp-syncing-docs`) |
| Learn | auditor (`mjrp-auditing-docs`) · kaizen (`mjrp-crafting-skills`, `mjrp-recording-decisions`) |
| Sempre | orquestrador (`mjrp-pdlc`) · `mjrp-pdlc-onboarding` (lê o estado) · `mjrp-saving-context` (grava o estado) |

Plugar um agente é preencher a vaga, com a governança da IA agêntica:
identificador por agente, log de atividade, interrupção sem corromper o estado, humano no alto impacto.

## 9. Artefatos — o que cada etapa lê e escreve

| Etapa | Lê | Escreve |
|---|---|---|
| Intake | pedido do MJRP, `uat.md`, `daily-checks/`, lição do Learn | item triado com a trilha, `prd.md` § Candidatos, `docs/log.md` |
| Discovery | `VISION.md`, `PRINCIPLES.md`, `ROADMAP.md`, `prd.md`, `constitution.md`, `arch.md`, `design-system.md`, o item | `design/inception/`, `design/wireframes/`, `inception-notes.md`, `ROADMAP.md` (^OUT, medida, tags), `prd.md` (épicos, fora de escopo), `info-arch.md` (inventário, ^estados), `design-system.md`, `design/prototypes/` + auditoria, `requirements/` (Backlog → Ready), `arch.md` + `data-model.md` |
| Contrato | `requirements/` Ready, `info-arch.md`, inventário com destino | decisão no `docs/log.md`, `gates:` opcionais |
| Delivery | `requirements/` Ready, `arch.md`, `data-model.md`, `design-system.md`, `constitution.md` | `features/F-xx/spec.md`, `plan.md`, `tasks.md`, `src/` + `tests/`, evidência no nó (`delivered_by`), PR |
| UAT | o entregue rodando, `requirements/` | `uat.md`, nó Accepted |
| Learn | `daily-checks/`, `doctor`, `uat.md`, `ROADMAP.md`, `docs/log.md` | `ROADMAP.md` (medida atual), [[harness-kaizen]], kernel · skills · sensores, item novo no Intake |

**Sempre:** `MEMORY.md ## Now` (o bastão), `docs/log.md` (uma entrada por decisão), o grafo de requisitos
([[requirements-graph]]).

## 10. Estado externo, Control Center e métricas

Os arquivos são o estado externo dos loops: nenhum passo depende da memória da conversa. O Control Center é a
observabilidade dos loops — o humano lê pouco e vê tudo. Métricas dos loops: **taxa de intervenção** (toques do humano por
unidade entregue), **captura do verificador** (falhas pegas por máquina × pelo humano), **retrabalho**, **custo por unidade
concluída**.

## 11. Da numeração antiga para os loops

| Antes | Agora |
|---|---|
| FASE 0 · Setup & bootstrap | Fundação |
| FASE 1a · Inception | Discovery · Explorar |
| FASE 1b · Discovery (ou "Consolidate") | Discovery · Enquadrar |
| FASE 2 · Design (2a · 2b · 2c) | Discovery · Desenhar |
| FASE 2→3 · Promote to Ready | o Contrato |
| FASE 3 · SDD | Delivery |
| FASE 4 · Quality | Delivery (verificador) + UAT |
| FASE 5 · Documentation & closure | UAT (documentador) + Learn |
| EP-90 · Intake (triagem do harness) | Intake, em todo projeto |

## History

- **2026-10-09 13:23** · Diagrama oficial passa à v4 (`2026-10-09-1318-pdlc-loops-v4`): a v3 com o kaizen do design — Desenhar = a tela e a descrição dela,
  `designing-ui` no lugar das quatro skills de tela, `design/wireframes/` entre o que a Discovery escreve. A v3 fica como histórico.
- **2026-10-09 13:04** · Kaizen do design (decisões do MJRP, 2026-10-09): a tela e a descrição dela (texto, inventário com wireframe,
  `info-arch.md`) são uma atividade só, de uma dona só — as quatro skills de tela se juntaram na `mjrp-designing-ui`;
  cada item do inventário termina numa função do produto ou num resultado; o wireframe mora em `design/wireframes/`.
- **2026-10-07 20:09** · Onda C (decisão do MJRP): no Learn, achado de documentação com evidência e fora do contrato é aplicado pelo
  agente sem esperar; o humano decide contrato, possível defeito e o indecidível (II.10).
- **2026-10-07 18:31** · Página criada a partir da proposta do PDLC em loops (#harness-kaizen). Origem: na saída da
  Discovery do Control Center o agente não usou o protótipo aprovado nem o inventário para os requisitos; o MJRP pediu um
  PDLC coerente, coeso e consistente, e depois redesenhado com loop engineering e agentic workflows. Decisões do MJRP: a
  v1 é a "v0 de loop engineering do PDLC"; escalada do Delivery ao contrato e à Discovery; UAT como fronteira; Intake com
  trilhas Full · Standard · Fast track · Fix; nomes Discovery · Delivery · Learn; prototipação rápida ligada por padrão e
  pode pular; aprovar spec e tasks vira opção do contrato; PR por feature com merge do agente, humano opcional no risco
  financeiro ou de negócio, com backup e rollback como pré-condição; Intake com dois sentidos (triagem agora, pré-venda
  depois).

## Related

[[product-discovery]] · sketch-vs-prototype · [[loop-engineering-concept]] · [[requirements-graph]] ·
[[harness-elements]] · [[harness-kaizen]] · [[git-governance]]
