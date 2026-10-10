---
title: Grafo de requisitos — nós, arestas tipadas e releases
aliases: [requirements-graph, grafo de requisitos, knowledge graph, rastreabilidade, arestas tipadas, cardinalidade feature requisito, release, planned_for]
summary: como requisitos e artefatos do PDLC viram nós com ID estável e arestas tipadas, legíveis no Obsidian e por script; a cardinalidade feature × requisito; como a release agrupa requisitos e épicos
tags: [kernel, sdd, requisitos, grafo, release]
status: em formação
atualizado: 2026-10-09
fontes: [design/proposals/requirements-knowledge-graph-proposal.md, kernel/architecture/knowledge-graph-concept, kernel/architecture/linked-notes-concept, kernel/architecture/graph-engineering-concept, kernel/ways-of-working/spec-kit]
---
<!-- kernel do MJRP Harness · versão 2026-10-09 · fonte b065d73 · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
O **grafo de requisitos** é a documentação do PDLC tratada como grafo de conhecimento: cada requisito, épico,
release, feature, REQ do spec, task, estado observável e teste é um **nó com ID estável**, e cada relação entre eles é
uma **aresta tipada** — com nome, direção, origem e destino permitidos e cardinalidade. Os conceitos (knowledge
graph, ontologia, tripla, validação por formas) estão em [[knowledge-graph-concept]]; o modelo de notas ligadas que
o humano usa para navegar, em [[linked-notes-concept]]. Um grafo, duas leituras: o
humano navega no Obsidian (wikilink, backlink, graph view); o agente e o sensor leem o mesmo grafo por script.
Não é *graph engineering*: no sentido do [[graph-engineering-concept]], aquele é o grafo de **comportamento**
dos agentes; este é o grafo de **dados** que o comportamento lê como estado.

## Details

> A S-63 fechou; o desenho e as alternativas estão em `design/proposals/requirements-knowledge-graph-proposal.md`.

### Nós e onde moram
- **Requisito:** um arquivo por nó, `docs/specs/requirements/<pasta do épico>/<ID>-<slug>.md`. O nome começa pelo ID
  (`S-07`, `UC-04`, `EA-11`, `NFR-03` — o próximo número livre do prefixo, nunca reusado) e segue com o slug: o título
  em inglês (a linha em negrito que abre `## en`), em kebab-case ASCII minúsculo, até 50 caracteres, encurtado com juízo
  para um humano ainda entender (`S-07-import-the-card-statement.md`). O slug nasce com o nó e não segue edições do
  título; a identidade é o ID (`id: S-07` e `aliases: [S-07]` no frontmatter). Renomear é operação explícita
  (`req_file_names.py --reslug <ID>`): move o arquivo e reescreve os links. Link e embed levam o nome inteiro do
  arquivo, com o ID como texto — `S-07`, `!S-07-import-the-card-statement` —,
  porque o Obsidian resolve nome de arquivo, não alias; o sensor acusa link com ID solto ou slug velho (`link_stem`) e
  nome fora da forma (`node_slug`). Status e arestas no frontmatter. A pasta é a que o épico declara
  (`folder:: ep-NN-<slug-em-inglês>`); NFR em `nfr/`. No subprojeto do harness, sem épico, o nó mora direto em
  `requirements/`. Regra `node_folder` no sensor, dormente enquanto nenhum épico declara `folder::`. O corpo vem em cada língua declarada — por padrão `## pt-BR` e `## en`, no mesmo arquivo, com um ID e um frontmatter só (regra `bilingual`; o contrato muda a lista em `mjrp_harness.requirements.languages`, `[]` desliga). É o nó mais ligado do grafo, por isso tem a âncora mais estável.
- **Feature:** uma pasta por ciclo SDD, `docs/specs/features/<F-ID>-<slug>/` com `spec.md`, `plan.md`, `tasks.md`.
  Dentro da pasta, `REQ-` e `TASK-` são IDs locais, resolvidos pelo script dentro dela.
- **Épico:** no `prd.md`, com as arestas dele numa linha logo abaixo do heading (`serves:: ROADMAP#^OUT-01`).
  **Resultado e release:** no `ROADMAP.md`, com block ID (`^OUT-01`, `^REL-01`). A direção é do ROADMAP
  para o PRD: o ROADMAP define os resultados, e o épico **serve** a um deles (`serves`). O ROADMAP não deriva dos
  requisitos do PRD — decisão do MJRP, 2026-10-04 12:15.
- **Tags de categoria:** todo resultado leva **de 1 a 3 tags** numa linha `tags:: #a #b` na sua seção do ROADMAP (logo
  abaixo do heading); todo épico **herda** as tags do resultado que serve e pode declarar **até 3 próprias** (`tags::` abaixo
  do heading, no PRD). Vocabulário livre, em inglês e kebab-case (`#visual-management`): o sensor confere só formato e
  quantidade (regra `tags`); `--tags` lista as de cada nó, com a herança calculada. Para quê: classificar e filtrar os
  resultados por categoria na gestão visual — a primeira é a GVV (Gestão Visual Virtual) do Control Center. Decisão do
  MJRP, 2026-10-06.
- **NFR (requisito não funcional transversal):** um nó próprio em `requirements/nfr/` (`NFR-01-<slug>.md`), como restrição que
  vale para todas as features; não é importado por nenhuma. O prefixo `REQ-` fica só para os REQ locais da feature.
  Decisão do MJRP, 2026-10-04 12:15, reversível: ele pode voltar atrás.
- **Estado observável:** uma situação da superfície do sistema que o humano vê e julga — alvo do `points_to`, com block
  ID por estado. Um tipo de nó, dois documentos: o **estado de tela** no `info-arch.md` (superfície visual, do protótipo
  julgado) e o **estado de comportamento** no `behavior.md` (superfície não visual: saída de comando, código de saída,
  arquivo gerado, hook que bloqueia, resposta de API, o que um agente faz). Sem tela, o que o humano julga são os
  exemplos. Link com caminho (`apps/<app>/docs/specs/info-arch#^x`) resolve no projeto aninhado. Decisão do MJRP,
  2026-10-04 14:41: uma regra só para todo requisito, sem isenção por tipo de projeto nem por data.

### A declaração única
As regras abaixo, em forma que o script lê, estão em `mjrp-scripts/requirements_graph_rules.json`: tipos de nó
(com o padrão de ID e onde mora), arestas (origem, destino, mínimo, máximo, a partir de que status são cobradas),
restrições e a sintaxe de cada forma de nó. Mudou a regra, muda o arquivo — e esta página explica o porquê.
Os status seguem o ciclo `Backlog → Prioritized → Ready → In progress → Done → Accepted`; uma aresta cobrada "a
partir de Ready" vale de Ready em diante. **Ready é o contrato** ([[pdlc-loops]] §4): o requisito vai a Ready com o OK do
humano, registrado no log; **Accepted** é o aceite dele no UAT. `Deferred` é válido mas fica **fora do ciclo**: requisito adiado não é
cobrado como Ready nem conta como aberto (decisão do MJRP, 2026-10-04 14:28).

### Arestas da primeira versão
Escreve-se **só uma direção**; a inversa é calculada (backlink no Obsidian, script para o agente).

| Aresta | De → para | O sensor exige |
|---|---|---|
| `serves` | épico → resultado do ROADMAP | todo épico tem exatamente 1 |
| `epic` | requisito → épico | todo requisito tem exatamente 1 — exceto no subprojeto do harness, onde é proibida (o épico vem de `parent_epic` no contrato) |
| `planned_for` | requisito (ou épico, como atalho) → release | opcional — release é opcional por projeto; exceto no subprojeto do harness, onde é obrigatória a partir de `Prioritized` |
| `points_to` | requisito → estado observável (de tela ou de comportamento) | requisito Ready tem pelo menos 1; o alvo existe |
| `imports` | feature → requisito | ver *Cardinalidade* |
| `implements` | TASK → REQ local | toda TASK tem pelo menos 1; todo REQ tem pelo menos uma TASK |
| `verified_by` | REQ → teste ou entrada do `uat.md` | REQ Done tem pelo menos 1 |
| `supersedes` | requisito novo → requisito entregue | obrigatória quando um requisito Done muda |
| `delivered_by` | requisito → commit | evidência de Done quando nenhuma feature Done o importa (trabalho meta, ou entregue antes do grafo) |
| `accepted_in` | requisito → aceite do humano (`uat#^UAT-xx` ou `log AAAA-MM-DD HH:MM`) | requisito Accepted tem 1, e ele resolve |

Cada aresta é checada só no trecho do ciclo em que faz sentido (lição do `SDD_chain_artifacts_check`: checar tudo
em todo par gerou 366 falsos positivos).

### Cardinalidade feature × requisito
Decisão do MJRP, 2026-10-04, nas palavras dele — **limitar:**
- **Feature → requisito: 1..n.** Uma feature entrega um ou mais requisitos. Por exemplo, a F01 entrega a S-08 e a
  S-09 juntas porque compartilham a mesma tela.
- **Requisito → feature: 0..1 aberta por vez.** Um requisito em andamento está numa única feature.
- **Se um requisito precisa de duas features, ele é grande demais.** A saída é fatiar o requisito, que já é um
  procedimento da `mjrp-writing-reqs`, e não permitir n:m.
- **Exceção: os NFR transversais.** Eles não são importados por nenhuma feature. Valem como restrição para todas e
  são conferidos na revisão, junto com a `constitution.md`.
- **Mudar um requisito já entregue gera um requisito novo, que substitui o antigo.** É aí que a aresta
  `supersedes` deixa de ser opcional.

### Release, épico e requisito
- **Release é opcional por projeto** — no subprojeto do harness é a unidade de organização — e mora numa seção do `ROADMAP.md` (decisão de 2026-10-02). Wave, milestone e
  release são o mesmo nó, com um campo `kind` se o projeto quiser nomear diferente; milestone é release com data.
- **A unidade planejada é o requisito** (`planned_for`); a feature herda a release dos requisitos que importa, e o
  sensor acusa feature que importa requisitos de releases diferentes.
- **Uma release pode conter épicos inteiros** — o épico não atravessa necessariamente a release. `planned_for` no
  épico é atalho para todos os seus requisitos; o requisito sobrescreve quando precisa. A composição por épico é
  calculada: épico inteiro na release quando todos os seus requisitos estão nela, parcial quando só alguns.
  **MJRP (2026-10-04): é importante para o controle humano e a gestão visual no Control Center** — o roadmap tem de
  poder mostrar releases compostas por épicos.
- **Ficam fora:** *fase* é a fase do PDLC (discovery, design, SDD), outro eixo; *sprint* é caixa de tempo, não de
  conteúdo — quem usa declara como release de `kind: sprint`.

### Subprojeto do harness: o épico no contrato, as stories por release

Um **subprojeto** é um projeto aninhado dentro do repositório do harness (`apps/<app>/`), com contrato, sensores e
grafo próprios. Ele **não declara épicos**: épico só existe no `prd.md` do harness, e o subprojeto diz no contrato a
qual pertence — `parent_epic: EP-08` em `.mjrp-project.yml`. As stories do subprojeto **não levam `epic:`**; elas se
organizam **por release** (`planned_for`, cobrada a partir de `Prioritized` — uma story em Backlog pode estar sem
release) e o `prd.md` do subprojeto as embute por release, não por épico. O resto do grafo fica local: o requisito
aponta para o estado da tela do próprio subprojeto, a feature importa o requisito do próprio subprojeto, e o sensor
roda em cada um sem atravessar repositório. Só a ligação de cima — o épico — atravessa, e uma vez só, no contrato.
O épico do harness guarda as stories que já entregou como histórico; as novas e as abertas moram no subprojeto.
Projeto filho independente (repositório próprio: pedroso, fin-control, health-control) **não** é subprojeto: tem
épicos próprios. (Decisão do MJRP, 2026-10-09 15:13.)

### O status pede evidência
O status é declarado no frontmatter, e declarado sozinho ele mente: ninguém atualiza, ou atualiza errado, e quem lê o
grafo roteia com confiança para o lugar errado (risco R-01 do PRD do harness). Por isso o sensor confere o status
contra a realidade — **a mesma regra para todo projeto**, decidida pelo MJRP em 2026-10-04:

| Status | Evidência que o sensor exige |
|---|---|
| **In progress** | uma feature aberta que importa o requisito, **ou** atividade recente — commit no nó ou na feature, ou entrada do log que cita o ID, em até `requirements.stale_days` (14) |
| **Done** | uma feature Done que o importa (tarefas fechadas, REQ com `verified_by`), **ou** `delivered_by:` com o commit que entregou |
| **Accepted** | a de Done **e** `accepted_in:`, que aponta o aceite do humano |
| **Ready** | `points_to`; o estado de tela apontado aparece na linha `shows::` de um protótipo aprovado (registro em `info-arch.md` § *Protótipos aprovados*) — estado de comportamento fica isento, não tem tela; e o documento do estado observável não mudou depois do requisito — se mudou, o critério pode ter envelhecido; com estado de tela, o `docs/specs/design-system.md` do projeto existe (regra `design_system_exists`: a identidade se decide antes do contrato) |

Code-app entrega por feature; o trabalho meta, e o que foi entregue antes do grafo, por commit — as duas formas são
evidência conferível, nenhuma é isenção. Três mecanismos aplicam a regra: o `pre-commit` recusa o commit que deixa
contradição num nó que ele toca; o `Stop` faz o mesmo nas sessões locais; uma passada diária acusa o que apodreceu
sem edição (In progress parado, estado mudado depois do Ready).

### Reconciliação (Guardian)
Quando o sensor acusa contradição ou status apodrecido, quem lê o grafo **reconcilia antes de rotear**:

1. Leia o achado e o nó — só ele, não o documento inteiro.
2. Confira a realidade: o git (o commit existe? a feature foi tocada?), os testes do REQ, o `uat.md`, o log.
3. A realidade tem evidência que faltava no nó → escreva a evidência (`delivered_by`, `accepted_in`, a tarefa marcada).
4. O status está à frente da realidade → volte o status ao que a evidência sustenta e diga por quê no log.
5. **Accepted é decisão do humano** — sem aceite registrado, pergunte a ele; nunca o declare por ele.
6. Registre cada reconciliação no log (uma entrada por decisão) e rode o sensor de novo.

É procedimento de Guardian: a `mjrp-ensuring-sdd` o assume (S-66), e a `mjrp-pdlc` o chama antes de decidir a
próxima estação. A passada diária só **propõe** (relatório em `reports/audits/`); o status muda numa sessão. O agente
que executa a reconciliação por conta própria é do EP-03 (brief do MJRP).

### Quem faz o quê (arquétipos)
- **Escrevem as arestas:** `mjrp-writing-reqs` (`epic`, `points_to`, `planned_for`), `mjrp-specifying-sdd-artifacts`
  (`imports`, `implements`), quem escreve o teste ou o `uat.md` (`verified_by`).
- **Escrevem os estados observáveis:** o de tela, `mjrp-designing-ui` (block ID no
  `info-arch.md`, a partir do protótipo aprovado); o de comportamento, `mjrp-writing-reqs` no Example Mapping, com os
  exemplos julgados pelo humano antes do Ready (decisão D-04 do MJRP, 2026-10-04).
- **Confere o grafo:** `mjrp-ensuring-sdd` (Guardian), sobre o sensor determinístico
  (`requirements_graph_check.py`; o `SDD_chain_artifacts_check` foi aposentado em 05/10, S-77).
- **Percorre o grafo:** `mjrp-pdlc` (Orchestrator) decide a próxima estação pelo estado dos nós.
- **Julga o conteúdo:** `mjrp-ensuring-quality` (Reviewer) — a aresta existir não prova que o teste prova o REQ.

## History
- **2026-10-09 20:55** · Revisão geral de 2026-10-09: nome do nó `<ID>-<slug>.md` (slug do título em inglês, até 50 caracteres, congelado ao nascer; `aliases: [<ID>]`; link com o nome inteiro e o ID como texto; renomear com `req_file_names.py --reslug`); exceções do subprojeto do harness nas arestas `epic` e `planned_for`; regra `design_system_exists` no Ready com tela; sensor `requirements_graph_check.py` no lugar do aposentado; S-63 fechada.
- **2026-10-09 15:13** · Subprojeto do harness (decisão do MJRP): épico só no harness; o subprojeto declara `parent_epic` no contrato e organiza as stories por release; o sensor reprova épico no subprojeto, `epic:` em story dele e story `Prioritized` sem release. O Control Center é o primeiro (EP-08).
- **2026-10-07 20:29** · Onda E do PDLC em loops: Ready é o contrato — vai a Ready com o OK do humano, registrado no log (decisão do MJRP; `mjrp-writing-reqs` atualizada na onda D).
- **2026-10-06** · **Tags de categoria em resultado e épico** (MJRP: "todos os elementos de outcome de roadmap e dos épicos do harness venham com uma tag que categorize"). Resultado com 1 a 3, épico herda e soma até 3 próprias, vocabulário livre; regra `tags` no sensor e no selftest, `--tags` lista; modelos de ROADMAP e PRD da `mjrp-pdlc-bootstrap` e a `mjrp-coaching-pm` escrevem o campo.
- **2026-10-05 13:46** · **Requisito em pt-BR e em inglês** (S-110; MJRP, 2026-10-05 09:39: "que isso fosse padrão, constitution"). Seções `## pt-BR` e `## en` no mesmo nó; regra `bilingual` no sensor, padrão `languages: [pt-BR, en]`; os 131 nós do harness traduzidos de uma vez (decisão dele: todos agora).
- **2026-10-05 10:53** · **Requisitos agrupados por épico** (S-123; MJRP: a lista longa de stories incomodava). Cada épico declara
  `folder:: ep-NN-<slug-em-inglês>` no PRD; os nós moram nessa pasta, NFR em `nfr/`. Regra `node_folder`; mover um nó não conta
  como atividade para `status_stale`.
- **2026-10-04 22:26** · **Dono do estado de comportamento** (decisão D-04 do MJRP): a `mjrp-writing-reqs` o escreve no Example
  Mapping quando não há tela, e o humano julga os exemplos antes do Ready.
- **2026-10-04 22:00** · **Estado de tela julgado** (decisão D-23 do MJRP, 2026-10-04). Requisito Ready que aponta para estado do
  `info-arch.md` (inclusive aninhado) precisa que um protótipo aprovado o mostre: o block ID está numa linha `shows::`
  do registro em § *Protótipos aprovados*. Regra `state_judged` no sensor; estado de comportamento isento.
- **2026-10-04 15:32** · **O status pede evidência** (S-67; MJRP, a partir da preocupação dele com a fragilidade do status
  declarado). Arestas `delivered_by` e `accepted_in`; regras de evidência no sensor; `pre-commit` e `Stop` recusam
  contradição nova; passada diária; procedimento de reconciliação do Guardian. Risco R-01 no PRD do harness.
- **2026-10-04 14:44** · **`points_to` aponta para estado observável** (decisão do MJRP, 2026-10-04 14:41). O sensor acusava 36
  requisitos do harness, um projeto sem tela; em vez de isentá-los, o alvo deixou de ser só estado de tela. Os 36
  ganharam o estado de comportamento do que existe hoje em `docs/specs/behavior.md` — descrição de onde se vê, não
  critério depois da entrega. Ficou um achado verdadeiro: a S-33 (Tracking do Control Center) está em andamento sem o
  `info-arch.md` do app. A S-63 substitui a S-48 (spec, plan e tasks planos → pasta por feature).
- **2026-10-04 14:29** · `Deferred` entra nas regras como status fora do ciclo (`off_track_statuses`): válido, nunca cobrado
  como Ready, nunca aberto — decisão do MJRP. O harness migrou o próprio backlog para o grafo (passo 10 da S-63):
  `^OUT-01` a `^OUT-06` no ROADMAP, `serves` em cada épico, 81 nós em `docs/specs/requirements/`.
- **2026-10-04 12:29** · Declaração única criada (`requirements_graph_rules.json`); IDs de resultado e release viram
  `OUT-01` e `REL-01` (antes `^R1`, por consistência com `EP-01`); arestas de nó dentro de documento (épico, release)
  em campo inline abaixo do heading.
- **2026-10-04 12:15** · Decididos pelo MJRP: a direção ROADMAP → épico (`serves`); NFR como nó próprio, e os requisitos de
  produto `REQ-` do harness viram requisitos no formato do projeto sob o épico que já os cita (reversível).
- **2026-10-04 11:26** · Página criada na S-63 com as decisões do MJRP: estrutura mista (arquivo por requisito,
  pasta por feature), arestas da primeira versão, cardinalidade feature × requisito (texto dele), releases com
  requisito como unidade e épico compondo release na gestão visual.
