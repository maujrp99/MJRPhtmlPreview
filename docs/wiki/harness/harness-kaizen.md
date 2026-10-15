---
title: Harness kaizen
aliases: [harness-kaizen, lições, licoes, aprendizados, o que não funcionou, incidentes do harness]
summary: onde o harness falhou e o que se aprendeu com isso — o erro e a correção no mesmo lugar
tags: [harness, memoria, kaizen]
status: em formação
atualizado: 2026-10-12
fontes: [2026-claude-code-auto-memory]
---
<!-- kernel do MJRP Harness · versão 2026-10-14 · fonte b714d244 · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
O registro do que o harness **não pegou** e do que se aprendeu com isso. Achado e lição moram
juntos porque são o mesmo movimento — o erro e a correção; separados, viram duas metades inúteis.
É o `lessons.md` do transcript do Waldemar, com nome nosso (ADR-0008).

## What it is

Duas origens, o mesmo arquivo:

- **O agente escreve durante o trabalho** — quando descobre que uma checagem estava calada, que
  um sensor mentiu, que uma regra existia e ninguém verificava.
- **O `loop.py` escreve sozinho** — todo loop que esgota o teto sem convergir deixa aqui a lição,
  em vez de ela morrer no terminal. O estado bruto de cada passada fica em `.mjrp/loop-state.md`,
  que é memória de trabalho e se apaga; o que sobrevive é a linha daqui.

**O que não entra:** o que se deduz do repositório, e o que o `AGENTS.md` já diz. Memória que
repete o que se pode ler é custo sem informação.

## How MJRP uses it

Uma linha por achado, **com data e hora**, mais recente no topo. Quando um achado vira regra
permanente, ele **migra** para o `AGENTS.md` ou para uma checagem do `doctor` — e sai daqui,
deixando o ponteiro. Lição que só mora aqui é lição que ninguém aplica.

> **Em formação.** Nasce vazio junto com o `loop.py` (BACKLOG #19) porque o loop precisa de um
> destino que já exista. O **28a** o preenche com o que hoje está em `MEMORY.md ## Sobre o
> próprio harness`.

## Findings

- **2026-10-14 20:19** · **A "cópia descartável" de um filho era um link para o filho real, e o teste escreveu nele.** No teste
  da `mjrp-organizing-product-structure` o agente criou a cópia do fin-control com `mkdir -p <scratchpad>/portfolio && rsync
  … <scratchpad>/portfolio/mjrp-fin-control-2026-27/`: a pasta `portfolio/` do scratchpad (que é da sessão inteira, não do
  agente) já existia, criada por outro agente às 15:24, com **links simbólicos** para os projetos reais. O `rsync` foi para
  o próprio repositório e as três rodadas (ROADMAP, 70 `planned_for`, dois `tasks.md`, uma entrada no log) caíram no
  fin-control real. Percebido no `ls` do portfólio do Control Center; desfeito em minutos, linha por linha, conferindo cada
  arquivo contra a cópia feita antes de cada edição (`git status` do filho igual ao de antes; nada commitado). **Por quê:**
  `mkdir -p` aceita pasta que já existe, e o nome "cópia" não prova nada. **Lição:** cópia de projeto real nasce numa pasta
  **nova** (`mkdir` sem `-p`), e o script que escreve nela recusa o caminho cujo `realpath` cai na pasta dos projetos —
  a mesma conferência vale para qualquer teste "numa cópia" (o protocolo dos evals da skill a cita).

- **2026-10-11 12:09** · **O Delivery entregou tela que não bate com o protótipo aprovado, com todos os sensores verdes.** No UAT
  do Control Center 1.0 o MJRP abriu a tela e achou, de cara: os componentes de UI padronizados do protótipo ausentes, o
  minimizar e expandir que valia para todos os cards em todas as telas, a marca "MJRP" no topo, a ordem do menu — "muitos
  detalhes de UI falhando". **Por quê:** (1) nenhuma feature comparou a tela com o protótipo. A conferência no navegador
  (`PRINCIPLES.md` I.12) foi lida como "vista rodando" e conferiu os critérios de aceite do `spec.md`, um por um, por
  texto e DOM (`read_page`, `get_page_text`), quase sempre com o painel oculto e sem captura. Só a F10 escreveu "comparado
  com o protótipo v4.1", e mesmo assim por leitura. (2) Nenhum Playwright, nenhuma captura lado a lado, nenhuma diferença
  visual. (3) A `mjrp-ensuring-quality` não foi invocada em nenhuma feature: as skills usadas foram a
  `mjrp-specifying-sdd-artifacts` e a `mjrp-implementing-tasks`, cujo passo 5.2 aceita "screenshot, snapshot ou assert
  datado" sem exigir o protótipo como referência. (4) Os critérios de aceite apontam para estados (`points_to`), não para o
  que é transversal no protótipo — o padrão de componente, o comportamento de todos os cards, a ordem do menu, a marca —, e
  por isso nenhum spec os importou. **Lição:** "a tela bate com o protótipo aprovado" tem que ser um critério com
  mecanismo (captura das mesmas telas e estados no protótipo e no produto, lado a lado, por Playwright, julgada por quem
  não implementou), não um passo de "ver rodando" que o próprio implementador cumpre lendo o DOM.
  **Fechado em 2026-10-12 15:55** (Learn aprovado pelo MJRP às 15:41) — o que mudou e onde: (L1) a `mjrp-implementing-tasks` (passo
  5.2, o item *Screen* do check e o PR) compara a tela com o protótipo aprovado pelo sensor de paridade visual e pelos
  olhos nos pares, e não mergeia feature de tela sem a reconferência; (L2) a `mjrp-specifying-sdd-artifacts` e os modelos
  (`spec.md`, `plan.md`, `tasks.md`, o cross-check, a `constitution` da `mjrp-pdlc-bootstrap`): toda feature de tela importa
  a camada transversal do protótipo, a primeira feature de tela porta o CSS, as fontes e os componentes do design system,
  a última task é a paridade visual, e cortar algo do design system exige decisão registrada (o `theme.css` cortou as
  webfonts sozinho); (L3) a etapa **reconferência visual independente** no Delivery ([[pdlc-loops]] § 5), o modo
  *visual parity* da `mjrp-ensuring-quality`, apontada pela tabela da `mjrp-pdlc`; (L4) o juiz do Control Center virou o
  kit do kernel `mjrp-scripts/visual_parity/` (o Control Center o consome; mesma saída, byte a byte, nas três passadas
  guardadas), o contrato ganhou `sensors.visual` e o doctor a checagem **A2** ([[doctor]], ADR-0017 *Proposed*); (L5) a
  `mjrp-debugging` e a `mjrp-ensuring-quality` registram a divergência confirmada como issue no `uat.md` na hora, e o
  cartão no quadro quando o projeto tem um.

- **2026-10-11 02:40** · **A conferência no navegador achou defeito real em quase toda feature do Delivery.** No Control Center 1.0, os
  sensores (lint, tipos, testes, schema, contraste) passaram em todas as features antes da conferência, e ela ainda achou: o
  git vazio mostrado como "não lido" (F01), a marca da última visita apagada por um F5 (F02), a história parada zerada pela
  renomeação dos arquivos (F03), o plural errado (F04, F05), "Sem release" sem status e a frase da história com metadados
  (F05), "de esta máquina" (F08) — além do harness mostrado "sem kernel" contra o `data-model.md` (F04, achado ao ler o
  modelo). **Lição:** a última task de tela (o navegador, `PRINCIPLES.md` I.12) não é cerimônia; e o contrato aprovado
  (o `data-model.md`) precisa ser relido pelo orquestrador na revisão, porque o subagente implementa o plano, não o modelo.
- **2026-10-11 02:40** · **Subagente com o mesmo roteiro de commit erra igual.** Dois subagentes Sonnet escreveram a mensagem de commit
  com `-m` de várias linhas e um deles saiu truncado (F05, `7721591`); outro commitou com o lint vermelho porque o roteiro
  não barrava (F03). **Correção:** os briefs passaram a pedir `git commit -F <arquivo>` com a conferência `git log -1`, e o
  auxiliar do orquestrador roda os seis sensores antes de commitar. **Lição:** o que se repete em todo brief vira ferramenta
  — candidato no Intake ("o commit não espera os sensores").

- **2026-10-10 22:01** · **O template da feature produzia link que o doctor reprovava.** O `plan.md` e o `tasks.md` da
  `mjrp-specifying-sdd-artifacts` abrem com `spec` e `plan`, o arquivo ao lado. O I3 do doctor (a checagem de
  links) só conhecia páginas da wiki, aliases e ADRs. Então a primeira feature feita pelo template, a F01 do Control Center,
  saiu vermelha sem erro de quem a escreveu. **Correção:** o I3 resolve o arquivo irmão; caso no selftest. **Lição:** o
  template e o sensor que julga o que ele gera precisam de um teste juntos. O selftest do I3 nunca rodou sobre um arquivo
  saído do template.
- **2026-10-10 22:01** · **Instalar uma ferramenta pelo Homebrew quebrou outra.** O `brew install uv node@22` atualizou `simdjson` e
  `simdutf` como dependências e deixou o Node padrão sem as bibliotecas que ele ligava. O sensor da tela do Control Center
  falhou com exit -6, e o subagente teve de contornar com um wrapper. **Correção:** `brew reinstall node`. **Lição:**
  depois de um `brew install` numa máquina de trabalho, rodar de novo os sensores que dependem do que já estava instalado.

- **2026-10-10 21:38** · **O hook de uso de skill criou uma pasta que a própria estrutura não conhecia.** Na primeira skill
  invocada numa sessão local, o `session_journal.py skill` (o hook que conta uso de skill) gravou
  `data/raw/skill-usage.csv`. A pasta `data/` não estava declarada no `structure.yml`, então o sensor de estrutura reprovou e
  deixou o doctor vermelho na sessão seguinte, sem nada de errado no trabalho. Achado ao abrir o Delivery do Control Center 1.0.
  **Correção:** `data/` e `data/raw/` declaradas no `structure.yml`; `STRUCTURE.md` regenerado. **Lição:** um hook que cria
  arquivo precisa da casa declarada na mesma mudança. O teste do hook rodou num repositório descartável, que não tem o sensor
  de estrutura, e por isso não pegou.

- **2026-10-09 22:02** · **Registrei como decisão o que era só herança.** Ao extrair o `design-system.md` do Control
  Center do protótipo aprovado, escrevi "Padrão: L2 Navy & Gold" — mas a L2 só estava no protótipo porque veio dos
  primeiros rascunhos; ninguém a escolheu. O MJRP perguntou quem definiu, e decidiu: L8 Organic Blueprint no claro, D4
  Zen Dark no escuro. **Correção:** `design-system.md` e protótipo v3.7 com o padrão dele. **Lição:** ao extrair de um
  protótipo, separar o que o humano aprovou do que só sobreviveu; o que só sobreviveu entra como proposta, com a
  pergunta.
- **2026-10-09 21:45** · **Um teste tocou a produção outra vez — a quarta da mesma classe.** O teste ponta a ponta da guarda do
  protótipo (o hook que exige wireframe e `info-arch.md` quando o protótipo muda) rodou num repositório descartável com os hooks
  do harness, e o `post-commit` (o hook que faz o backup do repositório a cada commit) gravou bundles desse repositório no
  iCloud Drive (`mjrp-backups/e2e-psc2/`). A cópia de teste herdou um efeito que só a produção devia ter. **Correção:**
  `backup_repo.py` pula repositório sem remote — um teste nunca tem, todo projeto real com esse hook tem `origin`; caso 8 no
  selftest (`f8a8d0d`). Os bundles foram para `_to_delete/` na raiz do iCloud Drive, para o MJRP apagar. **Lição:** o
  efeito colateral de um hook se desliga pela natureza do alvo, não pela lembrança de quem roda o teste.
- **2026-10-09 21:41** · **O relógio do host não é o relógio do harness.** A ponte para o Mac e a nuvem rodam em UTC; depois
  das 21:00 de Brasília, `date.today()` já era amanhã. O refresh do kernel carimbou a versão `2026-10-10` no Control Center e
  no health-control, e o `doctor_selftest.py` passou a reprovar o caso F1 (o que confere as linhas do `## Ways of Working`
  do dia) — com isso o sensor A1 do harness (o doctor rodando o próprio selftest) ficou vermelho. **Correção:** todo script
  que carimba data ou hora usa o fuso de Brasília (`new_project.py`, `doctor.py` e o selftest, `charter_to_prd.py`, os
  `gen_*`, `loop.py`, `push.py`, `_safe.py` — `ebdf6e5`, `bab1d49`); os carimbos errados foram refeitos no refresh seguinte.
- **2026-10-09 21:32** · **O tipo da entrada do log não tinha sensor — e um leitor do log quebrou.** Às 14:01 o fin-control e
  o pedroso tinham cabeçalhos com tipo de commit (`fix`, `perf`, `feat`, `docs`) e foram corrigidos à mão; às 21:26 o próprio
  agente gravou uma entrada `decisão`, e o protótipo do Control Center, que lê o log com um mapa fechado de tipos, parou de
  desenhar a Overview. Na mesma checagem, a segunda entrada do mesmo minuto não contava ("sem entrada nova") e o commit
  esperava o relógio virar. **Correção:** `log_entry_check.py` (o hook que exige uma entrada nova no log a cada commit)
  recusa tipo fora de `session · decision · inventory · ingest · harness-feedback` e vê a entrada pela linha inteira do
  título (`c9de575`); o protótipo v3.6 mostra um tipo desconhecido sem quebrar.
- **2026-10-09 21:30** · **O gerador da Wiki do protótipo nunca entrou no repositório — e a Wiki ficou quatro dias velha.**
  A aba Wiki do Control Center mostrava a leitura de 2026-10-05 17:43: o script que a gerou morreu com a sessão daquele dia,
  e o build do v3.5 (que relia Tracking e System Monitor) não tinha como reler a wiki. A auditoria de UX tinha apontado (P2,
  aberto). É a mesma classe de 2026-09-07 (o gerador do PDF do VISION fora do repositório). **Correção:** `wiki_gen.py`
  versionado na pasta do build do v3.6; a Wiki relida a cada build (36 páginas). **Lição:** todo dado que um protótipo
  mostra sai de um script versionado ao lado dele, ou o protótipo diz que o dado é congelado.
- **2026-10-09 21:16** · **Decisão gravada no kernel não chega sozinha às skills.** A revisão geral pedida pelo MJRP achou
  cerca de 45 trechos desatualizados e 9 contradições entre as 23 skills da fábrica — a regra do subprojeto sem épico
  (15:16) não tinha chegado à `mjrp-designing-ui`, ao `mjrp-pdlc`, à `mjrp-writing-reqs` nem à `mjrp-coaching-pm`; "a
  arquitetura está sã?" tinha dois donos. O kernel estava certo; quem executa lia a versão velha. **Correção:** as skills
  corrigidas na revisão (auditoria por um agente, correção por outro) e reempacotadas. **Lição:** uma decisão de processo
  termina com a busca pelo termo nas skills e no kernel, no mesmo commit — não na revisão seguinte.
- **2026-10-09 20:35** · **O Control Center chegou a requisitos Ready sem `design-system.md`.** O MJRP perguntou se o design
  system já não devia existir; devia — o passo visual do Desenhar não tinha porta, e a identidade morava só no código do
  protótipo. **Correção:** a regra `design_system_exists` do sensor do grafo (requisito Ready que aponta para um estado de
  tela exige `docs/specs/design-system.md`), o critério de saída da Discovery, e a `mjrp-defining-design-systems` extrai a
  identidade do protótipo aprovado; o `design-system.md` do Control Center foi escrito e espera a aprovação do MJRP. O
  design system do MJRP em camadas (tokens, temas, componentes) ficou como candidato no PRD, para depois da revisão.
- **2026-10-09 20:23** · **O arquivo do requisito tinha só o número — o MJRP abria um por um.** **Correção:** o nome é
  `<ID>-<slug>.md` (o slug é o título em inglês, encurtado por julgamento até 50 caracteres), links com o nome inteiro e o ID
  como texto, `aliases: [<ID>]`; regras `node_slug` e `link_stem` no sensor do grafo; `req_file_names.py` renomeou 121 no
  harness, 22 no Control Center e 167 em cinco filhos. **Lição:** nome de arquivo é interface para o humano antes de ser
  chave para o script.
- **2026-10-09 20:05** · **A primeira passada do crítico novo achou defeitos nele mesmo.** A `mjrp-critiquing-architecture`
  rodou na ADR-0002 (a arquitetura da 1.0 do Control Center) e devolveu, além dos achados, doze problemas da skill: o exemplo
  de achado era a própria ADR-0002 (prima o juiz); as restrições do dono do produto (o *Do Not Forget* do `MEMORY.md`) não
  estavam na ordem de leitura; critérios apontavam para páginas sem o conteúdo; nada cobria falha silenciosa. **Correção:**
  o handbook de Architecture Review do MJRP virou a página `architecture-review` do kernel, com IDs estáveis por regra, e a
  skill foi refeita sobre ela (vetos quando aplicáveis). **Lição:** juiz novo roda num artefato real antes de ser confiado,
  e o exemplo dele é neutro.
- **2026-10-09 19:51** · **Quem desenhou a arquitetura também a julgou.** A auditoria da ADR-0002 (16:45) foi feita pela
  mesma skill e na mesma sessão que a desenharam — a `mjrp-designing-architecture` tinha a Architecture Review dentro. O
  MJRP sentiu falta de um crítico como o de UX. **Correção:** a `mjrp-critiquing-architecture` (Reviewer) com a revisão que
  saiu da designer; os dois críticos, UX e arquitetura, seguem a mesma separação — troca de chapéu declarada ou agente
  separado, e a auditoria diz qual.
- **2026-10-09 19:40** · **O código do protótipo não seguia a definição do data-model.** Na conferência dos wireframes o
  MJRP achou dois defeitos que o build não pegou: "apaga as 1 edições" (plural fixo) e toda story em curso aparecia
  "parada" — o `track_gen.py` marcava parado o que estava em curso, mas o `data-model.md` define parada como em curso e sem
  commit na story há 14 dias ou mais. **Correção:** a chave `ad.reset.ask1` para o singular; o `track_gen.py` lê o commit
  mais novo do arquivo da story. **Lição:** código que implementa um termo definido cita a definição e tem um caso que a
  prova.
- **2026-10-09 19:36** · **O protótipo mudou e o wireframe e o `info-arch.md` não — a regra só existia em prosa.** O MJRP
  teve de pedir os dois depois de aprovar o v3.5. O `structure_check` conferia nome e pasta; nada conferia o vínculo.
  **Correção:** `prototype_sync_check.py` no hook `commit-msg` (o protótipo `<nome>-vN.html` só entra com o `info-arch.md` e
  o wireframe de toda tela no mesmo commit; a saída do humano é o trailer `Prototype-sync: skip — <motivo>`) e o check W14
  do doctor para o que escapar; distribuído ao Control Center e aos 8 filhos.
- **2026-10-09 11:54** · **O processo mandava todo item do protótipo servir a um resultado — e separava o info-arch da tela.** No inventário do v3.3 do Control Center, o agente quis cortar ou forçar um resultado para o que é só informação (o mapa do harness, a wiki), e tratou o info-arch como etapa depois do protótipo, herança das fases em cascata. O MJRP corrigiu: um control center informa, ajuda a decidir e age — informação é produto, não resultado; e o info-arch mora junto com o desenho da tela. Decisões dele: cada item do inventário termina numa função do produto (da Visão) ou num resultado, ou é cortado; `design/wireframes/` anda com o inventário; o kernel ganha temas; a biblioteca de paletas vai para o kernel (tema design). Brief e plano no `docs/log.md` desta data.
  **Correção (fechada em 2026-10-09 13:51):** (1) a `VISION.md` do Control Center declara as três funções — informar, ajudar a
  decidir, agir; (2–3) as quatro skills de tela viraram a `mjrp-designing-ui` — a tela e a descrição dela (texto,
  inventário com wireframe, `info-arch.md`) numa rodada só, cada item do inventário com destino na coluna *Serve a*
  (função do produto, `^OUT-xx` ou corte), e a leitura da reação como PM foi para a `mjrp-coaching-pm`; (4)
  `design/wireframes/` declarada, conferida pelo sensor de estrutura e criada em todo projeto novo; (5) o kernel por
  tema na fonte (ways-of-working, skills, architecture, roadmap, design), o filho achatado com o índice por tema; (6) a
  biblioteca de paletas no kernel, tema design. Os temas são refinados depois da revisão dos grupos da wiki no v3.4.
- **2026-10-09 11:10** · **Eu pus um passo que o plano não pedia na frente da tag.** Listei "rodar os cenários de eval das
  ondas A–D" como condição da tag `v0.0` (a marca do fim da migração para o PDLC em loops); o plano só exige o cenário
  **escrito** por skill. O MJRP já esperava a tag. **Correção:** a tag saiu; rodar os cenários foi para fora do caminho
  crítico. **Lição:** a porta de um marco é a que o plano aprovado declara — o que o agente acha prudente vira proposta, não
  condição.
- **2026-10-07 18:40** · **A Discovery não usou o protótipo aprovado nem o inventário** — #harness-kaizen do MJRP. Na saída da
  Discovery do Control Center, o coach partiu das 7 perguntas do MJRP e a `mjrp-writing-reqs` ia escrever requisitos
  sem o inventário do protótipo v3.3: abas aprovadas (Wiki, harness em camadas, ciclo de vida, memória × contexto) ficavam
  sem resultado nem requisito. Causa: o inventário só nascia na 2a (`mjrp-designing-information-architecture`), depois da
  Discovery; nenhuma skill da 1b o pedia. **Correção:** o inventário vira a entrada principal da Discovery — a
  `mjrp-coaching-pm` o monta antes do passo 1, os resultados o cobrem, a `mjrp-writing-reqs` não escreve sem ele, a 2a o
  completa; [[product-discovery]] ganha o item 8 do checklist. E a falha abriu o redesenho do processo: [[pdlc-loops]]
  (Intake + Discovery · Delivery · Learn), em que o "pronto" da Discovery é todo item do inventário com destino —
  checável por sensor.
- **2026-10-07 11:07** · **O coach perguntava os quatro riscos como "baixo, médio ou alto" — risco sem teste é chute.** Na 1b do
  Control Center, a `mjrp-coaching-pm` só nomeava os riscos; não tinha procedimento para transformá-los em teste. O MJRP
  corrigiu (*"como vc ajuda o PM a pensar nessas 4 dimensões ... pra testar valor, usabilidade e viabilidade técnica?"*) e
  pediu que o processo da Discovery fosse estruturado e escrito no harness, com o handbook dele como fonte (#harness_kaizen).
  **Correção:** página do kernel [[product-discovery]] — a v2 do Handbook MJRP de Product Discovery: Rapid em 5 passos, Full
  com catálogo de 12 técnicas, cada risco com "o que precisa ser verdade · evidência · teste mais barato", decisão matar ·
  iterar · avançar. Falta o `reference/` da skill, depois da leitura do MJRP. **Lição:** quando a skill só nomeia um
  conceito, o agente preenche o vazio com a pergunta mais fácil; o processo tem de dizer o que se pergunta e o que se produz.
- **2026-10-06 16:06** · **Resultado e épico não tinham categoria — o filtro por tema dependia de alguém ler o título.** Ao
  definir os dois resultados do Control Center (ver e governar), o MJRP notou que ambos são "Gestão Visual Virtual" e
  pediu que todo resultado do ROADMAP e todo épico venham com uma tag que os classifique (#harness_kaizen).
  **Correção:** campo `tags::` — resultado com 1 a 3, épico herda e soma até 3 próprias, vocabulário livre (formato e
  quantidade); regra `tags` no sensor do grafo e no selftest, `--tags` lista com a herança; página
  [[requirements-graph]], verbetes no [[terms]], modelos da `mjrp-pdlc-bootstrap` e a `mjrp-coaching-pm` escrevem o
  campo. **Lição:** categoria que mora só na cabeça do humano não aparece na tela; se vai ser filtro, é campo com
  sensor.
- **2026-10-05 17:37** · **Uma proposta só caía em `design/proposals/` se o agente acertasse.** A proposta de entrada da
  aba Wiki do Control Center se chamava `wiki-entry-options.html`: a regra de nome do `structure_rules.json`
  (`proposal` → `design/proposals`) só valia dentro de `docs/`, e o nome nem dizia "proposal". O MJRP perguntou
  como garantir que toda proposta, HTML ou PNG, vá para lá. **Correção:** regra nova `name_decides` — o arquivo
  cujo nome termina em `-proposal` só mora em `design/proposals/`, julgado na raiz, em `design/` e em
  `reports/` (código fica de fora); vale no hook de escrita, no pre-commit e no W9 (estrutura fora da
  natureza); as duas skills que propõem em três níveis nomeiam `<eixo>-proposal.<ext>`. Primeiro achado: dois
  diagramas `*-skill-roles-proposal` em `design/diagrams/`. **Lição:** lugar garantido é o que o nome do
  arquivo carrega; instrução na skill sem sensor é esperança.
- **2026-10-04 14:21** · **Uma compactação de contexto quase apagou decisões do MJRP — o registro dependia de hábito.**
  As respostas do passo 10 da S-63 só sobreviveram no resumo automático da AI Platform; o log e o `## Now`
  não as tinham, e o F1 passava porque media a data do `MEMORY.md`, não o conteúdo. O MJRP perguntou se a
  solução contra perda de contexto tinha rodado: não — a S-61 estava em Backlog. **Correção:** a S-61
  implementada no mesmo dia (`commit-msg` com entrada obrigatória no log, `## Now` julgado pelo conteúdo,
  hooks de diário e retomada, regra na `mjrp-onboarding` para a sessão remota) — [[memory-architecture]].
  **Lição:** regra que depende de o agente lembrar falha justamente quando o contexto some; ela tem que
  morar onde roda sempre — aqui, no git.
- **2026-10-02 18:53** · **O git pela ponte da AI Platform não apaga as próprias travas — a causa das travas órfãs
  em todos os filhos.** Sem a permissão de apagar concedida na sessão, o git commita, mas não consegue
  remover `HEAD.lock`, `index.lock`, `next-index-*.lock`, `objects/maintenance.lock` nem os
  `tmp_obj_*` que cria: o harness tinha 1.626 temporários acumulados e um `index.lock` de 29/09 que
  impediu as duas passadas agendadas do inventário de commitarem. O W10 (28/09) mostrava a trava e o
  `mv` que sara, mas tratava o sintoma. **A lição:** sessão que vai operar git pela ponte pede a
  permissão de apagar no começo (era a proposta 4 do parecer do fin-control, de 27/09, aceita só como
  higiene) — e o onboarding precisa dizer isso, não o handoff. **Corrigido (2026-10-02 19:01):** a `mjrp-onboarding`
  pede a permissão no começo, o `AGENTS.md` e o template do `new_project.py` dizem o mesmo.
- **2026-10-02 18:53** · **O harness tinha a ida do protótipo, não a volta.** A Inception (21/09) ensinou o harness a
  ver antes de definir; nada levava o que o humano aprovou no protótipo até o build — o `info-arch.md`
  era escrito como se a tela não existisse, e item aprovado podia sumir sem ninguém decidir. Parecer
  vindo do brainstorming do YouTube Control Center; o titular corrigiu a leitura do agente duas vezes:
  não é achar o que falta (isso é o IN-09/IN-10), é **não perder o que existe** — e o protótipo é
  **baseline, não molde**. Virou o mapeamento reverso: inventário com destino por item, W11 no doctor.
- **2026-09-28 09:21** · **O harness não tinha catálogo de componentes de interface — cada protótipo
  reinventa tabela, caixa recolhível e filtro, e nada garante que o build use o mesmo que o protótipo.**
  Levantado pelo MJRP como kaizen: elementos básicos (tabela com ordenação e filtro, caixa
  expansível/recolhível, card, abas, barra de filtro, estado vazio…) deveriam nascer como artefatos
  iniciais do projeto e ser reaproveitados em protótipo e interface. Evidência no próprio harness: o
  Control Center reinventou cards recolhíveis e abas a cada versão (v1 → v3.1); o [[design-canon]] diz
  *como* uma tela deve ser, mas nenhum artefato diz *o que já existe* para reaproveitar. **A lição:**
  uso garantido não vem de regra na skill (é o vazio de verificação registrado em 16/09 no `MEMORY.md`),
  vem de duas coisas — o componente ser o **caminho mais fácil antes** de a tela existir, e um **sensor
  que acusa o desvio depois**, com rigor crescente por fase: protótipo rápido (kit pronto embutido,
  só aviso — tem de continuar rápido); protótipo no gate de protótipo de UI (princípio I.13: verificação
  com ID no `mjrp-ux-critic`, P1 bloqueia; desvio justificado vira candidato ao catálogo, não dívida);
  build (sensor de marca no doctor e no pre-commit, frescor da cópia vendorizada, testes de contrato de
  teclado/ARIA/celular na suíte do filho). A base comum: **um único código** do protótipo ao build,
  vindo do kernel — sem tradução entre fases — e uma **marca estável** por componente
  (`data-mjrp="…"`) que torna o uso contável. **Limite:** o sensor garante presença, não bom uso; se a
  tabela era a escolha certa segue com o critic e o humano. Estado (2026-09-28 09:40): o MJRP encaixou no escopo do
  EP-07 (Discovery & Prototipação), depois do EP-08 1b — `docs/specs/prd.md`. **Correção do MJRP (2026-09-28 09:42):**
  a regra "reaproveitar antes de criar" com P1 bloqueando no gate foi rejeitada — *"mata
  criatividade, não pode ser diretiva"*. Vira **lembrete**: verificar também a alternativa de
  reaproveitar, e criar componente novo segue legítimo. A critic lembra, nunca bloqueia por isso.
  É a segunda vez do mesmo vício (ver o achado de 2026-09-21 19:00): em fase de design a skill
  **oferece** a opção, não impõe — o que se garante é que o reaproveitamento seja *considerado*,
  não que seja *usado* No build (2026-09-28 09:51), o MJRP decidiu: o sensor reprova só **infidelidade ao
  protótipo** — quando o protótipo aprovado usou um componente do catálogo e o build reescreveu a
  peça em vez de importar o mesmo código. Reaproveitamento nunca é cobrado; fidelidade ao aprovado, sim.
- **2026-09-21 19:00** · **O harness não tinha caminho de "ideia → tela para reagir → requisito", e o agente
  escreveu regra onde devia oferecer.** O EP-08 (Control Center) nasceu de uma ideia em alto
  nível; ao pedido "quero um protótipo", o agente renderizou sem enquadrar — sem info-arch, sem
  pergunta de teste, sem chamar ux-ui-designer/interface-designer — e a `mjrp-ux-critic` reprovou
  (4 P0: CP-02, DE-01, DE-06, IN-06; `apps/control-center/docs/specs/ux-audit.md`). Diagnóstico
  do MJRP: o achado não era da tela, era do processo — o lifecycle assumia "definir → renderizar",
  e um humano visual descobre "vendo → reagindo → definindo". Nasceram a **FASE 1a Inception** e
  a **`mjrp-inception`** (interface designer + PM com questionamento SVPG, fundidos). Na
  primeira redação, o agente repetiu o vício em outra forma: "≤1 rodada", "lo-fi", "2–3
  rodadas", "quem julga é o humano, a critic não", "vai ao 2c" — regra fixa numa fase que existe
  para descobrir. O MJRP reescreveu: *"pode… conforme a preferência do usuário"*, *"fica a
  critério do humano"*, *"o humano ajuda a decidir"* — e rejeitou "sonda" (jargão do agente, não
  do processo humano). **A lição, em três camadas:** (1) Discovery e Inception são o diamante
  abrindo — a skill dessas fases **oferece, recomenda e pergunta**; regra fixa ali mata o que a
  fase deveria produzir; (2) a regra ainda cabe, **restringindo o agente**, nunca o humano ou o
  processo — "não inventar dado como real" fica; "para quando…" sai; (3) o vocabulário é o do
  humano. A regra de escrita entrou na `mjrp-crafting-skills` (é ela que escreve as skills) e no
  Ways of Working; a inspeção semântica com esse critério achou 11 ajustes em svpg,
  ux-ui-designer, prompt e lifecycle — todos troca de modal, não reescrita. **Mecanismo:** o
  parecer veio de um subprojeto aninhado (`apps/control-center/docs/harness-feedback/`), que o
  `harness_feedback_check.py` não varria — passou a varrer. Loop inteiro (campo → juiz → parecer
  → cânone/skill) numa sessão. Fonte: Buxton, [[sketch-vs-prototype]].
- **2026-09-19 09:37** · **Scheduled task com `requires_local_device` que trava em `get_device_info().connectedFolders`
  vazio é auto-sabotagem — o campo vem vazio nas sessões agendadas frias mesmo com o Mac alcançável; o
  caminho certo é `device_bash` direto no path absoluto.** O sensor #62 (sincronia Repo↔Cowork) falhou em
  18 e 19/09: a execução agendada abortava em ~7s com "connectedFolders is empty" e notificava sem rodar. A
  "correção" de 18/09 (deletar e recriar o trigger com `folders` explícito) tratou o sintoma errado — o
  trigger passou a ter `folders_state: PRESENT` e mesmo assim a sessão agendada seguiu com `connectedFolders`
  vazio. A prova de que o gate era a causa veio do trigger vizinho: o **inventory** roda todo dia com
  `folders_state: NONE` (nenhuma pasta declarada) e funciona — 11 min de trabalho real em 19/09 — porque o
  prompt dele vai direto em `device_bash /Users/maujrp/mjrp/projects/mjrp-harness` sem checar `connectedFolders`.
  Declarar a pasta no trigger não popula o `connectedFolders` da sessão agendada, e não declarar não impede o
  `device_bash` com caminho absoluto. **A lição:** num prompt de scheduled task que precisa do Mac, nunca
  usar `connectedFolders` como gate de "posso continuar?" — ir direto no `device_bash` com path absoluto e só
  parar se a chamada `device_bash` em si falhar (transitório "disconnected/closing" → 1 retry; qualquer outro
  → parar e reportar). Prompt do #62 reescrito assim em 19/09 (re-assinado pelo Mac, pois o trigger exige o
  computador). Ver também `docs/log.md` [2026-09-18 12:25]. Corolário: `last_run: SUCCEEDED` de um scheduled
  task só diz que a sessão subiu e encerrou, não que o trabalho foi feito — o #62 "teve sucesso" abortando. **Desdobramento (10:35):** tirar o gate não bastou — o `device_bash` no path absoluto foi RECUSADO na sessão agendada ("No folders are connected to this device for the current session"), enquanto o inventory, sem pasta declarada (`folders_state: NONE`), escreve no Mac todo dia. A causa real: **declarar `folders` no trigger quebra o `device_bash` da sessão agendada** — o grant daquela pasta foi concedido numa sessão interativa e não persiste para runs agendados; a sessão então tenta montar a pasta declarada, falha, e recusa todo acesso. Sem pasta declarada, o bridge concede acesso à árvore normalmente e o `device_bash` com path absoluto funciona. Como `update_trigger` não remove `folders`, o #62 foi recriado sem pasta (`trig_013Q…` → `trig_01Gq48WfUC8zkmQHDqev6sxD`). **A lição final:** scheduled task que precisa do Mac roda com `requires_local_device: true` e **sem** `folders` declarado, indo direto no `device_bash` com path absoluto — declarar a pasta é contraproducente para runs não-supervisionados. **Correção (11:02):** a hipótese acima foi REFUTADA no run frio seguinte — sem pasta declarada o `device_bash` também é recusado ("No folders are connected to this device for the current session"). O run de 82s que parecia validar rodou quente (disparado pela criação numa conversa ligada ao Mac), não frio — erro de validação (ver Ways of Working 15/09). Verdade atual, sem hipótese: numa sessão agendada fria o `device_bash` não recebe pasta conectada, com ou sem `folders` declarado; só `get_device_info` responde. O inventory (agendado, sem pasta, 11 UTC) acessa o Mac e o #62 (10 UTC) não — a única variável isolada é o horário, não a config do trigger. Ação tomada: mover o #62 para 11:30 UTC (após o inventory) como teste de horário, não como causa provada. **Lição de método:** não declarar "resolvido" a partir de um disparo manual/quente — só um run agendado frio valida um fix de scheduled task; e desconfiar de hipótese que "explica" mas não foi testada no cenário real que quebrava.
- **2026-09-18 10:14** · **`rm` nos `.git/*.lock` órfãos falha mesmo com `device_request_delete_permission`
  confirmado — `mv` no mesmo arquivo funciona; o achado já tinha se repetido em silêncio em 11/09, 16/09 e
  17/09.** Toda vez que um `git commit`/`add` foi interrompido (sessão anterior encerrada, timeout), sobra
  um `index.lock`/`HEAD.lock` de 0 bytes que bloqueia o próximo `git` com `File exists`. A resposta óbvia —
  pedir a permissão de delete pro `device_request_delete_permission` e rodar `rm` — não funciona: a ponte
  remote-devices confirma a concessão ("File deletion is now enabled...") mas o `rm`/`os.remove()` seguinte
  continua batendo em `Operation not permitted`, inclusive em arquivo novo fora do `.git/`. Sessões
  anteriores já tinham topado com isso (os `.lock.stale.*` de 11/09, 16/09 e 17/09 encontrados no repo são
  a marca de outras tentativas) mas nenhuma registrou a lição — cada uma resolveu na mão e seguiu. O que
  resolve: `mv .git/index.lock .git/index.lock.orphan` (ou qualquer nome fora do padrão `*.lock`) —
  renomear escapa do gate de delete-permission porque não é uma chamada de unlink, é rename; depois disso
  o `git` volta a funcionar normalmente (ele só olha o nome exato `index.lock`/`HEAD.lock`). **A lição:**
  quando `rm`/`unlink` falha com `Operation not permitted` na ponte remote-devices mesmo após a permissão
  confirmada, tentar `mv` para um nome fora do caminho antes de escalar para o humano — e registrar aqui
  na primeira vez que funcionar, não silenciosamente resolver e seguir, senão o harness reaprende o mesmo
  workaround a cada sessão nova.
- **2026-09-14 20:04** · **O template ensinou o erro, e nenhum sensor olhava a metade episódica da
  memória.** O `mjrp-fin-control-2026-27` nasceu às 13:28 pelos **dez passos manuais** da
  `mjrp-project-bootstrap` — quarenta minutos antes de ela passar a rodar o `new_project.py` —
  numa sessão Cowork com a skill instalada defasada e sem hook nenhum. Resultado: `docs/log.md`
  batizado *"Histórico de Decisões do Projeto"* e `## Ways of Working` com **12 marcos de
  entrega num dia** ("parametrizado", "aprovado", "gerada"). O outro agente diagnosticou certo a
  instância e errou a causa ("viés de chat"); a raiz estava **aqui**: o `new_project.py` escrevia
  *"uma linha datada por decisão"* no cabeçalho de todo log novo, e a árvore da bootstrap dizia o
  mesmo — o harness ensinava a confusão que depois reprovava. E o F1 só media o tamanho de
  `Ways of Working`; **nada abria o `log.md`**. Três correções: template do `new_project.py` e
  linha da bootstrap copiados do cabeçalho canônico (não inventados — a correção do outro agente
  criou *"Registro Episódico do Projeto"*, um terceiro nome, e o sensor novo já a reprova);
  `f1_log_shape` (cabeçalho canônico + prefixo `## [AAAA-MM-DD HH:MM] tipo — título`, falha) e
  `f1_wow_growth` (mais de 4 linhas datadas de hoje em `Ways of Working`, aviso — correção de
  conduta não vem em lote; e é **aviso** porque 07/09 teve seis correções legítimas). Quatro casos
  no `doctor_selftest`. O sensor, rodado na instância, acusou o cabeçalho inventado e 5 linhas do
  dia. **Lição de mecanismo:** os dois incidentes de 14/09 (Gemini de manhã, fin-control à noite)
  têm a mesma raiz — nascimento fora do script + skill instalada defasada + sem hook fora do
  Claude Code. Guide viola-se; sensor não. O que ainda **não** tem mecanismo é o *write* da
  memória em plataforma sem hook — a `save-context-handoff` continua sendo pedido, não regra.
- **2026-09-12 12:20** · **Nem toda skill que nomeia uma plataforma está violando a regra
  plataforma-agnóstica — a `mjrp-adr` já era exceção ao critério (d), e a varredura do #40 achou
  a mesma forma no critério (a).** A `mjrp-crafting-skills` nomeia Cowork, Claude Code e Antigravity
  de propósito: o assunto dela **é** empacotar skills para cada uma dessas plataformas
  especificamente — trocar por "AI Platform" quebraria a instrução, não a tornaria mais genérica.
  A mesma varredura também achou dois sentidos diferentes para a palavra "Gemini": a plataforma
  de codificação (violação, trocada por "AI Platform") e um produto do Google citado como fonte de
  dado — Gemini Notes do Gmail (`mjrp-meeting-notes-batch`), a API de um app implantado
  (`mjrp-deployer`). **A lição:** o critério "sem nome de plataforma" não é lexical — é "esta skill
  descreve o harness assumindo qual ferramenta o executa?". Quando o nome da plataforma É o assunto
  (empacotamento) ou nomeia outra coisa (um produto de terceiro que a skill consome), a exceção é
  correta, e generalizar o texto às cegas troca precisão por conformidade de forma.
- **2026-09-12 10:07** · **Citação conferida a olho não é citação conferida.** O playbook dos cinco
  conceitos é feito de citação literal — e, ao rodar um script que compara cada trecho entre aspas
  com as páginas da wiki, **15 de 214 não batiam**. Nenhuma era invenção: um "do que" engolido, um
  ponto final que migrou para dentro das aspas, duas frases da mesma fonte fundidas numa só, um
  travessão que virou parte da citação. Erros invisíveis na releitura e fatais numa página que se
  vende como "na letra do campo". O `check_quotes.py` nasceu como critério de saída do brief e
  achou todos em três segundos; hoje roda dentro do `gen_agentic_concepts.py --check`. **A lição:**
  o II.3 — *o agente não é o juiz* — vale para **prosa**, não só para código. Toda vez que um
  entregável afirma fidelidade a uma fonte que existe em arquivo, a fidelidade é **verificável por
  mecanismo**, e verificar é barato; o caro é descobrir depois que o deck citava errado. Onde houver
  fonte em disco, o critério de saída não é "reli e está bom", é um script com exit code.
- **2026-09-11 11:05** · **A `mjrp-project-bootstrap` estava atrasada em 14 pontos — e o pior
  deles era estrutural: ela não criava o contrato.** A revisão nasceu de um achado pequeno (o
  guia do `VISION.md` de lá não tinha campo de visão) e a suspeita do MJRP de que o resto
  estivesse igual se confirmou. Os três que importam: (1) nenhum dos 10 passos criava o
  `.mjrp-project.yml` — todo projeto bootstrapado nascia **invisível** para `onboarding`,
  `lifecycle` e `doctor`, que leem o contrato primeiro, e a sessão seguinte caía na heurística;
  (2) a camada de memória inteira faltava — sem `MEMORY.md`, sem `wiki/`, com `docs/sessions/`
  aposentado desde 09/09 ainda na árvore; (3) **nenhum critério de saída** — o bootstrap
  terminava sem rodar sensor nenhum, num harness cuja tese é que erro se pega por mecanismo.
  Lição: **skill de setup envelhece calada.** Ela roda uma vez por projeto, no começo, quando
  ninguém tem repertório para desconfiar do que ela manda fazer — e o custo de estar errada é
  pago em todas as sessões seguintes daquele projeto, não na sessão em que ela rodou. Isso a põe
  na mesma classe da `mjrp-onboarding`: skill de fronteira, que merece varredura por calendário e
  não por sintoma. Achado de tabela: 9 "Related Templates" citados no cabeçalho, **nenhum existe
  no repositório**.
- **2026-09-11 10:28** · **O teste da `mjrp-onboarding` (cenário Album Blender V1) passou na
  substância e falhou na forma — e a culpa era do template, não do agente.** A síntese abriu com
  *"reescrita técnica do V0 (Vanilla JS) em Vue 3 + Pinia + TypeScript"* e só depois disse o
  propósito. No segundo turno, perguntado *"o que é este projeto?"*, o agente respondeu pelo
  produto e citou `VISION.md` + `CHARTER.md` — carregado na Phase 1, antes da pergunta. Ou seja: o
  contexto certo **estava** na cabeça dele; o formato de saída é que o pôs em segundo lugar. A
  Phase 4 pedia *"[o que é e para quê, 1–2 frases]"* — dois pedidos numa lacuna só, com o *o que é*
  primeiro na frase. Num projeto cujo *o que é* literalmente **é** uma reescrita, o template
  autoriza exatamente a saída que o aviso logo abaixo proibia. Lição: **aviso não corrige o que a
  estrutura induz.** Quando a regra e o slot discordam, o slot vence — a correção é quebrar o slot
  em dois campos ordenados (*para quê* na primeira frase, *o que é* na segunda), nos dois modos.
  Segundo achado do mesmo run: o agente **apagou** um `.git/index.lock` órfão durante o
  carregamento. Onboarding é leitura; conserto durante o diagnóstico faz a sessão começar num
  estado que ninguém pediu, e deleção é do humano. Virou regra no cabeçalho da skill.
- **2026-09-11 10:25** · **O conserto do achado do big picture chega na skill — antes ele existia só no
  `AGENTS.md`.** Em 10/09 registramos que a `mjrp-onboarding` garante "onde mexer" e não "para que
  serve o todo", e corrigimos o `AGENTS.md` (VISION virou leitura incondicional, README saiu da
  lista). Mas o formato da síntese da própria skill continuou pedindo só mecânica —
  *"Contexto carregado: [arquivos]. Padrões chave: [...]. SDD status: [...]"* —, que é exatamente
  o formato que produziu o problema. Consequência que só apareceu ao planejar o teste: a correção
  valia apenas para sessões abertas **no harness**, porque em outro projeto quem manda é o arquivo
  de instrução daquele projeto. Agora a Phase 1 diz que ler o `VISION.md` **não é item de
  checklist** — é extrair a frase que responde "por que este projeto existe" —, a confirmação
  abre por ela nos dois modos, e entrou o teste: *se alguém lesse só a sua primeira frase, saberia
  o que este projeto é e para que serve?*. Com a regra explícita de **não deduzir o propósito** do
  README, do nome da pasta ou do que o código faz, e de **dizer em voz alta** quando o projeto não
  declara propósito em lugar nenhum. **A lição:** corrigir a regra no documento de instrução
  conserta um projeto; corrigir o **formato de saída da skill** conserta todos — e foi a diferença
  entre as duas que quase passou como "feito".
- **2026-09-10 21:58** · **O selftest achou um bug latente no parser YAML ao declarar as pastas do
  inventário.** Ao acrescentar `- mjrp-scripts/   # o inventário do código: um script por linha` ao
  contrato, o `doctor_selftest` acusou divergência entre o `_yaml_minimal` e o PyYAML: o parser
  procurava o `:` que decide **escalar ou mapa** no corpo do item **com o comentário junto**, então
  a linha virava um dicionário cuja chave era o caminho mais o comentário. O mesmo valia para
  `- "x: y"`. Nenhum contrato tinha exercitado o caso — é o mesmo tipo de cegueira registrada em
  09/09, quando a amostra comparada não exercitava a diferença e a lista em bloco passou anos
  quieta. Corrigido (o `:` se procura no corpo sem comentário e fora de aspas) e fixado como caso
  6 do selftest. **A lição:** o parser mínimo existe para a máquina sem PyYAML — ou seja, roda
  exatamente onde não há oráculo para conferi-lo. Toda sintaxe nova que entra no contrato tem que
  virar amostra do selftest **no mesmo commit**, senão o contrato é lido de um jeito na máquina do
  MJRP e de outro na máquina de quem clonar.
- **2026-09-10 21:45** · **Os dois arquivos que o agente lê primeiro estavam mandando fazer o que
  o sensor reprova.** Revisão do `AGENTS.md` e do `CLAUDE.md` contra as mudanças do dia achou 12
  incoerências; duas passavam de defasagem: (1) o `CLAUDE.md` mandava gravar decisão de meio de
  sessão em `## Decidido` — seção que a ADR-0008 esvaziou e que o `doctor` (F1, linha 599)
  **reprova** se reaparecer, ou seja, quem obedecesse a instrução deixava o repo vermelho; (2) os
  dois mandavam `TZ` cru (`rode date`), que é exatamente o bug de três horas corrigido hoje de
  manhã — certo no `MEMORY.md`, errado nos dois arquivos que são lidos antes dele. As outras dez:
  a tabela "Onde mora cada memória" estava **partida ao meio** por um blockquote inserido entre as
  linhas 7 e 8 (as seis linhas seguintes não renderizavam como tabela); o mapa da memória apontava
  para a **ADR-0008** quando o próprio arquivo diz três parágrafos depois que "ADR não é onde regra
  operante mora" — agora aponta para [[memory-architecture]] e [[context-vs-memory]]; `PRINCIPLES`
  ainda descrito como "como se decide aqui"; `log.md` descrito como "onde a última sessão parou",
  que é o `## Now`; um caminho que não existe (`docs/sources/harness-evolution-proposal.md`); oito
  diagramas que são nove; "~900 linhas" que são 2.858; a tensão entre o cabeçalho "sob demanda" e
  dois itens marcados "sempre"; e a linha **Semântica** sem `docs/wiki/`, que é onde a semântica
  mora. **A lição:** o arquivo de instrução é o último a ser revisado porque não é entregável de
  nenhuma tarefa — e é o primeiro que todo agente lê. Toda mudança de regra tem que voltar para
  ele no mesmo dia, ou ele vira o lugar onde a versão antiga sobrevive com autoridade.
  **De passagem:** o aviso sobre o caminho do Mac anterior (`/Users/mpedroso/…`) saiu do topo do
  `AGENTS.md` — decisão do MJRP: caminho que não existe é trabalho de sensor (I2 resolve todo
  caminho absoluto), não de prosa que custa token em toda sessão.
\n
- **2026-09-10 21:20** · **Dois documentos de entrada disputando o mesmo chão — e o sensor cobria
  só um.** O `README.md` e o `HOWTO.md` ensinavam instalação por caminhos diferentes: o HOWTO via
  `build_plugin.py` + `/plugin marketplace add ./dist`; o README § 6.2 mandando copiar pastas para
  `.claude/skills/`, que o próprio HOWTO chamava de fallback. O `entry_check.py` só lia o HOWTO,
  então a versão divergente do README nunca foi testada. Cada um se declarava a porta: o HOWTO
  dizia "o que ler antes: nada", o README se dizia "guia operacional" — e mandavam o leitor um
  para o outro. **Resolvido pela decisão do MJRP:** se dois arquivos se sobrepõem, deve haver
  **um**. O HOWTO foi absorvido pelo README (que o GitHub renderiza e onde o catálogo gerado já
  morava) e aposentado em `_archive/root-docs-2026-09/`; o `entry_check.py` passou a ler o README.
  **A lição:** a duplicação não foi pega por um sensor porque o sensor *fazia parte* da
  duplicação — ele validava um dos dois documentos e por isso dava verde enquanto o outro
  prometia coisa diferente. Sensor que cobre só metade de uma duplicidade atesta a metade certa.
- **2026-09-10 19:55** · **A correção do achado acima começou pelo `AGENTS.md`, não pela
  onboarding.** O agente do exemplo 2 leu o `README.md` antes do `VISION.md` porque o "O que ler"
  do `AGENTS.md` listava o README como "guia operacional" e o VISION com a cláusula *"leia antes
  de decisão estrutural"* — condição que o agente julga sozinho (`PRINCIPLES.md` #3: opção
  deixada ao agente desaparece sob pressão). E o README ainda carregava uma segunda explicação
  do harness (§1–§4), onde o agente achou "resposta" e parou. Feito: BACKLOG #31 executado
  (README sai do "O que ler"; VISION vira leitura incondicional, com o porquê); README §1–§4
  viraram ponteiros — o README **aponta**, não explica; §5–§8 ficam por serem de humano e sem
  outra casa. **Falta:** a mesma cláusula vive nas *instruções do Projeto Cowork* (citadas em
  external-locations) — fora do repo, só o MJRP alcança.
- **2026-09-10 19:43** · **Onboarding garante "onde mexer", não "pra que serve o todo" — e um
  agente que substitui um humano só é efetivo se souber as duas coisas.** Dois onboardings reais
  mostraram o mesmo padrão: no Album Blender V1, a "identidade do projeto" que saiu foi stack e
  constraints (Vue 3, Pinia, TS strict) — nunca por que o rewrite existe. No próprio harness (o
  caso mais grave, porque é o repo de casa), o agente respondeu "o que é este projeto?" com
  README+ROADMAP+contrato — mecânica — e só leu o `VISION.md` (leitura obrigatória da Phase 1,
  primeira da lista) quando cobrado duas vezes. A resposta mudou depois de ler: apareceu o
  propósito real (a família, não o software, é o fim) e uma consequência de arquitetura que a
  mecânica sozinha não explica — memória mora em arquivo no repo porque harness/plataforma/
  instância/usuário são domínios que se desacoplam, e ferramenta muda sem avisar. **A lição
  (MJRP, verbatim, 10/09):** *"se um agente for substituir um humano num projeto, essa
  substituição só é efetiva se, como o humano, o agente souber onde ele entrou e qual o objetivo
  final do que ele está fazendo... um humano nunca deveria trabalhar sem entender o contexto e
  por que e pra que."* Sem esse mínimo de big picture, mexer no específico arrisca quebrar o todo
  sem o agente perceber que quebrou — porque ele nunca soube que aquele invariante existia. Bug
  do harness por `PRINCIPLES.md` #4, não falha do agente: faltou o guia (uma síntese que carregue
  propósito antes de estado), não faltou capacidade de ler o `VISION.md`.
- **2026-09-10 19:22** · **Os achados do schema/`.claudeprompt` na `mjrp-onboarding` foram
  resolvidos no mesmo dia em que foram encontrados**, a pedido explícito do MJRP ("não gosto de
  tech debt, resolve agora"). Junto, apareceram mais 2 ocorrências do mesmo bug de schema
  (`type: content`/`path: content`) dentro do próprio `mjrp-project-lifecycle` que a revisão
  daquele arquivo, horas antes, não pegou — a busca original só olhava o bloco YAML completo
  (`mjrp_project:` sozinho numa linha), não as menções soltas em prosa. **A lição:** ao corrigir
  um schema, grep pelo valor errado (`type: content`), não só pela chave estrutural — prosa cita
  o valor sem repetir a estrutura do bloco.
- **2026-09-10 19:13** · **`.claudeprompt` sobrevivia como artefato a criar em 3 skills, mesmo
  morto.** `AGENTS.md` é canônico desde a reestruturação de 09/09 (`CLAUDE.md`/`GEMINI.md`
  importam ele) — mas `mjrp-project-lifecycle`, `mjrp-onboarding` e `mjrp-project-bootstrap`
  ainda mandavam configurar `.claudeprompt`/`.gemini/GEMINI.md` como se fossem os artefatos
  primários. Nenhum dos três apontava pra `AGENTS.md`. Corrigido nos três — `.claudeprompt` só
  sobra como sinal de detecção em inventário de projeto brownfield (pode existir num projeto
  antigo), nunca mais como algo a criar. **A lição:** um nome legado não morre sozinho quando o
  canônico muda em um lugar só — quem cita o legado em prosa continua citando até alguém ir atrás
  de cada ocorrência.
- **2026-09-10 18:44** · **O save deixou uma seção fantasma no `MEMORY.md`, e o F1 deu verde.** Ao
  reescrever o `## Now`, o corte foi no primeiro "`## Ways of Working`" do arquivo — que estava
  **dentro do texto antigo** (a frase "headers em inglês (`## Now`, `## Ways of Working`…)"), não no
  header. Sobrou meio `## Now` velho, com rótulos em português, colado numa linha que começava com
  "## Ways of Working`, `## History`…". O F1 comparava título por **prefixo** e aceitou a linha como
  a seção legítima; o `now_section` parava nela e contava 4/4 blocos. MJRP viu abrindo o arquivo.
  Lição dupla: (1) título de seção se compara pelo nome exato — prefixo é convite a fantasma;
  corrigido em `doctor`, `memory_check` e com caso de selftest; (2) script que fatia um arquivo por
  marcador tem que ancorar o marcador no **início de linha**, nunca em `str.index` solto — o mesmo
  texto pode aparecer citado no conteúdo.
- **2026-09-10** · **O mesmo bug do dia anterior, mas a causa já não era a mesma.**
  Um novo transcript apareceu em `transcripts/` na raiz de novo — hoje, 13:42, quase
  o mesmo horário do flagrante de 09/09. Mas a cópia instalada da
  `mjrp-youtube-transcript` já estava corrigida (verificado agora, byte a byte
  contra a fonte): as 5 menções a destino no `SKILL.md` apontam certo para
  `docs/raw/transcripts/`, sem sobra do caminho antigo. A skill estava certa e o
  arquivo saiu errado assim mesmo — instrução correta não é garantia de execução
  correta; foi outra sessão/superfície que não seguiu a skill, não uma cópia
  desatualizada. Dois achados diferentes com a mesma assinatura de sintoma ensinam a
  mesma lição duas vezes: o sensor de `estrutura` (arquivo fora do lugar) pega o
  efeito, não a causa — e a causa muda. Movido para `docs/raw/transcripts/`, campo
  `Destino:` interno corrigido no arquivo.
- **2026-09-10** · **Duas vistas do mesmo doc, mantidas à mão, saíram de sincronia — e uma
  delas ainda avisava um problema já resolvido.** O `roadmap.html` tem uma versão paisagem
  (slide) e uma retrato (Kindle) do mesmo conteúdo, alternadas por classe de `<body>`. Quando a
  fase D (Ambiente — sandbox + infra) nasceu para resolver "o furo" do roadmap, só a versão
  paisagem foi atualizada; a retrato ficou uma fase atrás — sem a fase D, e com o box final
  ainda alertando sobre um furo que o `ROADMAP.md` já registra como resolvido. É a mesma classe
  da duplicação prosa/gatilho da `mjrp-deployer` (skill-distribution): duas cópias do mesmo
  fato, mantidas por mão humana, e nada compara uma com a outra. Sincronizadas as duas com o
  `ROADMAP.md`, PDFs regenerados a partir do HTML corrigido.
- **2026-09-09 19:47** · **Um selftest de 8 casos achou dois defeitos que a leitura não achou** —
  o piso de 30% aprovava a entrada reduzida ao título, e a guarda da linha de base vazia matava o
  `--forma`, que não depende de linha de base nenhuma. Os dois estavam no código que eu tinha
  acabado de escrever *para corrigir* defeitos. A lição não é "escreva testes": é que **o caso que
  prova o sensor é o caso trivial** — a frase idêntica tem que casar, e a entrada gutted tem que
  reprovar. Sem esses dois, todo o resto que o script imprime é ruído.
- **2026-09-09 19:45** · **O verificador reprovava a frase idêntica a si mesma, e ninguém viu.**
  O `memory_check.py` tirava as *stopwords* da assinatura e **não** as tirava do texto de destino:
  procurava um alfabeto dentro de outro. A consequência não foi um falso verde — foi um falso
  vermelho, "99 de 100 sem destino", que eu apresentei como linha de base e usei para dimensionar
  o 28a. **Número de sensor quebrado não é número conservador; é número inventado**, e serve tanto
  para superestimar quanto para subestimar. Junto vinha o segundo furo: nada media *volume*, então
  uma entrada de 308 chars migrada como 85 passava por "encontrada". Corrigido com uma peneira só
  (`sieve()`) usada nos dois lados, retenção medida por palavra significativa em janela, e piso
  declarado (40% reprova, 40–70% fica registrado). A linha de base honesta é outra: **107 entradas,
  10 com destino, 6% do volume**. Quem pegou foi o Zé, perguntando o que o verificador media.
- **2026-09-09 19:30** · **Eu inventei a coluna "por onde volta" e travei o 28a nele com ela.** A
  pergunta dele era sobre truncamento e eficácia; eu respondi mudando a classificação, que é o que
  ele **não** questionou, e transformei isso em bloqueio do lado dele. O agrupamento está aprovado.
  O que está errado é o verificador, e o conserto é meu.
- **2026-09-09 18:55** · **Terceira vez no dia que um teste tocou a produção — e a cópia já
  estava lá.** O `hooks_selftest.py` monta um repositório falso e copia o `stop_gate.py` para
  dentro dele… e então roda o **caminho do original**, passando só `cwd=` o repo falso. Como o
  gate resolve a própria raiz por `__file__`, ele leu o repositório **real** o tempo todo: os
  casos 3, 4 e 5 passaram por coincidência (o repo real estava sujo) e o `--declare true` escreveu
  no `.mjrp/turn.json` **de verdade**. A lição não é "isolar o teste" — eu tinha isolado. É que
  **isolar o dado e não isolar o executável não isola nada**, e o sintoma é o teste passando por
  motivo errado. Tirei a constante com o caminho real do arquivo: guardá-la é convidar o erro de
  volta.
- **2026-09-09 18:55** · **Aposentar não é copiar — e eu chamei nos dois destinos reescrevendo um
  só.** O `gen_vision_pdf.py` chamava `retire_path` no HTML *e* no PDF antes de renderizar; numa
  máquina sem renderizador de PDF, ele escrevia só o HTML e o PDF anterior **sumia** (o
  `_safe.retire_path` **move**, não copia — está escrito na docstring dele). Recuperado do
  `_backups/`, que é justamente por isso que a regra existe. A regra corrigida: **aposente só o
  que você vai reescrever nesta execução** — aposentar o que não se reescreve é apagar com passos
  a mais. Quem pegou foi o `--until` do próprio item, que exige o PDF existir.
- **2026-09-09 18:05** · **Segundo item que estava feito e o backlog não sabia.** O #30 (tirar os
  ponteiros ao `CHARTER.md` de VISION e HOWTO) já estava cumprido — zero ocorrências nos dois
  arquivos. Descoberto do mesmo jeito que o #37: escrevendo o critério de saída, não lembrando.
  **Dois em dois dias.** O sintoma não é esquecimento — é que **escrever o `--until` virou o
  único momento em que alguém confere o estado real**. Enquanto o `BACKLOG.md` (hoje arquivado; o papel é do PRD) for a única fonte
  do que está aberto e ninguém o medir, ele erra para mais: acusa aberto o que está fechado, e o
  planejamento em cima dele custa tempo em item que não existe.
- **2026-09-09 17:30** · **Regex em código é a mesma classe do rename cego da manhã.** A
  tradução dos identificadores dos 16 scripts começou por substituição regex e quebrou três
  coisas de uma vez: renomeou dentro de *string literal* (`harness-kaizen.md` virou
  `harness-kaizen_path.md`) e **deixou de renomear** acesso a atributo (`rep.erros`), porque o
  lookbehind que eu pus para não tocar em objeto alheio também pulava o nosso. O certo é
  **tokenizar** — `tokenize` distingue NAME de STRING por construção. Segunda armadilha, já com
  o tokenizador: antes do Python 3.12 a f-string é **um token STRING só**, então nome dentro de
  `{...}` não chega como NAME. E terceira: reescrever dentro de f-string por regex renomeia
  também o que está entre aspas lá dentro (`m['total']` virou `m['total_']`). A regra que fica:
  **para código, a ferramenta é o parser da linguagem, não o casamento de texto** — e o que salva
  em todo caso é rodar os verificadores depois de cada passada.
- **2026-09-09 17:30** · **O cache do A1 serviu o resultado do estado quebrado.** Durante a
  tradução, o `loop_selftest` reprovou; consertado, o `loop_selftest` passava sozinho e o
  **doctor continuava vermelho** — porque o `.mjrp/sensors.json` guardava o `code: 1` de dois
  minutos antes. É o `BACKLOG.md` #10 (arquivado em 17/09) (*"resultado de sensor guardado em cache mente com o
  tempo"*) acontecendo ao vivo, com hora. Não consertei: é a vez dele, não a minha — one-piece
  flow. Cache invalidado à mão, cópia em `_backups/`.
- **2026-09-09 14:55** · **A cópia instalada no Cowork É alcançável — de dentro do Cowork.** A
  ADR-0002 §7 afirma que nada no harness alcança a skill instalada, e por isso o
  `skills_status.py` responde por *proxy* (diff do git contra um marco de subida). A afirmação vale
  para o shell do Mac; **não vale para uma sessão do Cowork**, que recebe as skills da conta
  sincronizadas em disco e pode compará-las byte a byte com `mjrp-skills/`. Feito hoje: das 53
  skills, **52 batem e 1 diverge** — a `mjrp-debug`, cuja cópia instalada ainda manda escrever ADR
  em `docs/architecture/` enquanto a fonte diz `docs/decisions/`. O proxy tinha respondido "20
  skills desde 01/09": **19 falsos positivos**. Sensor por proxy, quando a medida direta existe,
  é ruído com cara de rigor. Ressalva honesta: o que a sessão vê é um instantâneo, que pode ficar
  atrás de uma subida muito recente — é evidência, não oráculo. Mudar a regra da 0002 exige ADR
  nova; aqui fica o fato.
- **2026-09-09 14:35** · **O drift de três vias apanhado em flagrante, com hora.** Às 13:42 de
  hoje um transcript novo foi gravado em `transcripts/` na raiz — pasta aposentada pelo 26b. A
  fonte da `mjrp-youtube-transcript` aponta para `docs/raw/transcripts/` desde 09/09, e o `dist/`
  também. Quem escreveu no lugar errado foi a **cópia instalada no Cowork**, que ninguém
  atualizou. Não é hipótese da ADR-0002 §7 — é o caso, datado. E o sensor que acusou foi o
  `estrutura`, não um sensor de skill: nada no harness compara a cópia do Cowork com a fonte,
  porque nada a alcança. O `skills_status.py` é o mais perto que dá — e ele só sabe responder
  depois que alguém rodar `--marcar` uma primeira vez.
- **2026-09-09 14:05** · O `harness-kaizen.md` tinha **161 linhas idênticas** escritas pelo
  `loop_selftest.py` — 35% do arquivo. O selftest guardava e restaurava o arquivo, mas capturava
  o estado **depois** dos primeiros casos já terem escrito. Corrigido: `MJRP_LOOP_KAIZEN` desvia o
  destino, e o caso 5c prova que o real não mudou. Condensadas em 1 linha, cópia em `_backups/`.
- **2026-09-09 14:05** · **Guarda na linha errada é guarda que não existe.** O
  `loop_selftest.py` *sabia* que não devia sujar a memória — guardava o `harness-kaizen.md` e
  restaurava no fim. Só que capturava o estado **depois** de os casos 1–4 já terem escrito: o
  guarda protegia o único caso em que alguém pensou e deixava vazar todos os anteriores. 161
  linhas idênticas, 35% do arquivo, ao longo de um dia. Corrigido na raiz: `loop.py` lê
  `MJRP_LOOP_KAIZEN` (como já lia `MJRP_LOOP_AGENT`), o selftest desvia a corrida inteira para um
  temporário, e o caso **5c** — que faltava — prova que o arquivo real não mudou um byte.
  A lição geral: **um teste que protege a produção precisa de um caso que verifique a proteção.**
  Sem o 5c, o guarda quebrado passaria verde para sempre.
- **2026-09-09 13:45** · O `entry_check.py` ganhou a **c7**: clona o próprio repositório num
  diretório temporário e roda ali o caminho do HOWTO. As checagens 1–6 liam o disco **desta**
  máquina, onde `dist/` já existe porque alguém rodou o build um dia — quem chega novo não tem
  isso. É a mesma cegueira do I2 vista de outro ângulo: **o sensor validava o desenvolvedor, não
  a porta**. E a c7 provou-se na primeira execução, reprovando o estado real (`dist/` ainda no
  HEAD) enquanto o desrastreio estava só no índice.
- **2026-09-09 13:20** · **Comentário no fim da linha do `.gitignore` desliga a regra.** Só o `#` no
  **começo** da linha é comentário; no resto da linha ele vira parte do padrão. As duas linhas de
  build do harness estavam assim desde 05/09 — o padrão real era `mjrp-skills-packages/   # pacotes
  .skill para o Cowork`, que não casa com nada. Resultado: **94 arquivos de `dist/` (1,2 MB) e 23
  `.skill` (252 KB) versionados**, em 14 commits, sob um comentário que diz *"nunca commitado"*.
  A lição maior é a forma do erro: **o comentário que documenta a intenção foi o que a desligou** —
  e o arquivo continuou parecendo certo para quem lê. Achado da sessão do Claude Code do Zé, que
  viu `main` sujo com três `.skill` ao criar os worktrees.
- **2026-09-09 13:20** · `git add -A` num commit meu levou junto três `.skill` que a mensagem não
  mencionava. A mensagem descrevia critérios de saída e mapa de faixas; o commit também carregava
  binário de build. Não corrompeu nada, mas quebra a regra que o próprio repo cobra dos outros: o
  commit tem que dizer o que ele contém. `add -A` é conveniente e mente.
- **2026-09-09 12:05** · O `BACKLOG.md` listava o **#37** (cabeçalho do `PRINCIPLES`) como aberto.
  Ele estava feito. Eu não descobri por lembrar — descobri por `grep`, ao escrever o critério de
  saída dele. O Zé nomeou na hora: *"não é surpresa, é o uso do memory ainda não funcionando"*.
  É o argumento da ADR-0008 em estado puro — trabalho aconteceu, ninguém registrou, e o arquivo
  de estado passou a mentir. A cada item assim, o backlog vale um pouco menos como fonte. O sintoma
  não é esquecer: é **planejar em cima de estado falso**.
- **2026-09-09 12:00** · O **I3** confere link markdown **dentro de bloco de código**. A
  ADR-0007 §1 diz que "trechos em código (cercado ou inline) ficam fora", e o `doctor.py`
  aplica isso **só à metade dos wikilinks**: `sem_codigo` é calculado depois do laço dos links
  markdown, então um `grep` de exemplo cujo padrão seja um link markdown reprova como se fosse
  referência quebrada. **Esta entrada provou o defeito ao ser escrita**: a primeira versão citava o
  padrão literal e o doctor ficou vermelho por causa dela. É a mesma classe do I2 que não distinguia
  gabarito de caminho — o padrão citado num comando não é ponteiro. Achado, não corrigido:
  `doctor.py` é território do
  28c e dos itens 5/9b/10, e mexer nele agora é o atropelo que as faixas existem para impedir.
  Decisão pendente do Zé.
- **2026-09-09 00:55** · **O parser que eu escrevi perdia dado em silêncio, e o F2 ficou verde por silêncio.**
  O `_yaml_min` não lia **lista em bloco** (`- item`) nem convertia data: o `gates_open` virava um mapa
  solto, o F2 não via gate aberto nenhum e o relatório dizia "0 gates abertos" — verdade acidental.
  Só apareceu porque o **selftest rodou na máquina do Zé**, que não tem PyYAML: aqui o PyYAML mascarava
  o fallback, que era código morto. **Três lições:** (1) o parser agora levanta `YamlNaoSuportado` no que
  não sabe ler, e o doctor sai 2 — *sensor que inventa é pior que sensor que falta*; (2) a comparação que
  eu mesmo pus no selftest **passou** porque comparava no contrato do harness, onde `gates_open` está
  vazio — *teste que compara duas implementações numa amostra que não exercita a diferença não prova
  nada*; (3) o caminho de fallback só roda onde a dependência falta, então o teste dele precisa de
  **expectativa escrita à mão**, que vale sem oráculo. Agora são 5 amostras + frontmatter + 1 caso sem
  oráculo, e o selftest acusa **8** checagens na instância quebrada, não 7.
- **2026-09-09 00:47** · **O `entry_check` reprovou por não enxergar, e isso é erro de sensor.** Ele acusou o
  `marketplace add ~/mjrp/projects/.../dist` do HOWTO porque o `~` daqui não é o `~` do Mac. Caminho
  escrito para **outra máquina** verifica-se pela cauda, não pelo prefixo — é a mesma disciplina que a
  I2 já tinha ("não avaliável ≠ reprovado") e que eu não apliquei ao escrever a checagem nova. Sensor
  que reprova o que não consegue ver ensina a ignorar vermelho.
- **2026-09-09 00:44** · **O `entry_check.py` achou algo na primeira execução** — o `README` mandava invocar
  `mjrp-env-setup`, skill que **não existe** em `mjrp-skills/`. Documento citando skill aposentada é
  a mesma classe de falha do caminho quebrado, e nada olhava para isso. **E ele não pode ser sensor
  declarado no contrato:** o `entry_check` roda o `doctor`, e o `doctor` executa os sensores — seria
  recursão. Fica avulso, e entra pelo hook `SessionStart` do A4.
- **2026-09-09 00:39** · **A I2 não distingue molde de caminho.** Dos seis erros do primeiro A3, três eram
  *template* — `Books/<Título>`, `Meeting-Notes/{category}/…`, `_logs/{ISO-timestamp}.json` — e não
  caminho quebrado. A checagem resolve tudo que parece caminho absoluto, e um molde nunca existe.
  Virou convenção no `AGENTS.md`: **prefixo fixo dentro das crases, parte variável fora**. Alternativa
  descartada por ora: ensinar a I2 a ignorar `{...}` e `<...>` — mas aí ela deixaria passar caminho
  de verdade com chave no nome. A convenção custa menos e não cria ponto cego.
- **2026-09-08 23:28** · **A porta de entrada não tem sensor, e é onde ele mais falta.** O Zé rodou o harness
  numa máquina limpa e gastou **seis intervenções manuais** antes do primeiro comando útil:
  (1) o `environment.setup` do contrato manda `pip install --user pyyaml`, que o Homebrew
  *externally-managed* recusa; (2) o `doctor` exigia PyYAML para rodar; (3) `doctor.py .` apontou
  para a pasta-mãe, que não é instância; (4) seis caminhos de skills quebrados que ninguém sabia;
  (5) dois contratos-filhos num schema que o `README` **ainda ensina**; (6) `marketplace add ./dist`
  com o caminho errado no documento. **O `HOWTO.md` abre dizendo "o que ler antes: nada" e trava no
  primeiro comando.** O harness verifica a instância (`doctor`), os links (`check_docs`) e o build
  (`build_plugin`) — e **não verifica que as próprias instruções funcionam**. É a dor 4 na porta de
  entrada, e contradiz a métrica do roadmap ("~20 intervenções → 1"). Frase dele: *"imagina que eu
  sou um novo funcionário da MJRP; isso que eu estou passando é justamente o que o harness deve
  prevenir"*. Candidato a checagem com incidente documentado, pela regra da ADR-0002.
- **2026-09-08 22:32** · **Eu estava devendo o `log.md`.** A última entrada era da manhã: seis horas de
  trabalho existiam só no `MEMORY.md`, e a `mjrp-onboarding` **não lê o MEMORY** — uma sessão nova no
  Claude Code começaria sem nada disso. O protocolo diz "checkpoint ao fechar um bloco", e eu deixei
  para o fim. É o argumento do 28d em estado puro, e apareceu porque o Zé perguntou sobre a onboarding.
- **2026-09-08 22:28** · **O `ESTADO.unlink()` do `loop.py` mascarou três falhas do selftest de uma vez.** O mount
  da ponte proíbe apagar, então o loop.py morria em silêncio na 2ª chamada em diante e os casos 3, 4b e
  5b reprovavam por motivos inventados. A regra do repo — *nada se apaga, sobrescreve* — não estava no
  código que eu mesmo escrevi. Corrigido: `write_text` em vez de `unlink`, no loop e no selftest.
- **2026-09-08 20:06** · **BACKLOG #13 estava meio feito e meio errado.** `mjrp-adr` já grava em `docs/decisions/`
  desde `6351e6e`; `mjrp-onboarding` nunca leu `CURRENT.md` — lê `log.md` e SpecKit. O furo
  real: **a onboarding não lê o `MEMORY.md`**, que o `AGENTS.md` manda ler primeiro. A ADR-0006
  registrou o pendente errado. Inventário completo em `_archive/docs-2026-09-16/duplication-inventory.md`.
- **2026-09-08 18:26** · **Perda encontrada e revertida:** o invariante do critério de saída (antigo nº 12 dos
  Princípios de governo) tinha saído do VISION como "governança" e não entrou no PRINCIPLES —
  sobrevivia só no AGENTS.md. É o II.4 agora.
- **2026-09-08 14:30** · **Segunda vez que aponto para o que não existe.** Propus "as onze peças vira
  ponteiro para `docs/wiki/`" sem a página existir — o Zé pegou de novo: *"vc vai construir
  o md lá? senão não adianta apontar para o nada e remover o conteúdo"*. **Regra: remoção com
  ponteiro só depois que o destino existe, no mesmo commit.**
- **2026-09-08 14:24** · **Primeiro incidente de `MEMORY.md` parado:** o Zé tomou seis decisões e eu as
  escrevi num brief em vez do arquivo — ele teve que perguntar. A ADR-0005 previu o custo ("não
  há sensor que detecte um MEMORY parado"); agora existe o incidente que, pela regra da ADR-0002,
  justifica a checagem.
- **2026-09-08 14:24** · Fronteira borrada por mim: eu venho pondo *o que aconteceu* no "Foco agora" do
  `CURRENT.md`. Relato é do `log.md`; decisão é do `MEMORY`. O CURRENT devia ter ~15
  linhas, não 34.
- **2026-09-07** · O gerador do PDF do VISION **não está no repositório**; enquanto estiver fora,
  nada que o Zé marcar na capa é encontrável por busca no repo.

## Lições do loop

- **2026-09-09 13:24** · **161 execuções do `loop_selftest.py`** entre 2026-09-08 19:30 e 2026-09-09 13:24 escreveram esta mesma lição (`loop.py` esgotou o teto sem que `false` passasse). Não é histórico — é o defeito descrito acima: o selftest guardava o `harness-kaizen.md` e restaurava no fim, mas capturava o estado **depois** dos primeiros casos já terem escrito. As 160 linhas ocupavam 35% do arquivo. Condensadas aqui em 09/09 (cópia integral em `_backups/`), com a origem corrigida no mesmo dia: `MJRP_LOOP_KAIZEN` desvia o destino, e o caso **5c** prova que o teste não tocou no arquivo real.

## Related
[[memory-architecture]] · [[context-vs-memory]] · recurring-pains · ADR-0008
