---
title: Harness elements
aliases: [as onze peças, onze elementos, componentes do harness, harness-elements]
summary: os harness elements — as onze peças de um sistema agêntico, o domínio de cada uma, e onde o MJRP está
tags: [harness, fundamento, mapa]
status: firme
atualizado: 2026-09-14
fontes: [pasquadev-loop-engineering, anthropic-context-engineering, ibm-skills-mcp-rag-memory, fowler-guides-sensors]
---
<!-- kernel do MJRP Harness · versão 2026-10-09 · fonte 4c7593e · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
As **onze peças** que compõem o entorno de um modelo de linguagem para que ele produza trabalho
confiável. Nem todas são nossas: cada peça pertence a um dos [[terms|quatro domínios]], e o domínio
muda o que dá para fazer com ela.

> **Validado pelo MJRP em 2026-09-14** — *"por ora, se precisar evoluímos e modificamos no futuro"*.
> É a primeira descrição elemento a elemento que o harness tem; mudança de peça, domínio ou estado
> entra datada no `## History`.

## What it is

Uma tabela para ver de relance, e depois cada uma com detalhe.

| # | Peça | Domínio hoje | Estado no MJRP |
|---|---|---|---|
| 1 | Loop de execução | Plataforma | emprestado — o da tarefa ainda não existe |
| 2 | Ferramentas | Instância | catálogo pendente; `tools:` não implementado |
| 3 | Guides | Harness | é o que mais temos — as skills |
| 4 | Context engineering | Harness | `onboarding` faz o *select*; falta medir |
| 5 | Memória | Harness + Instância | seis tipos, com casa (ADR-0001, 0005, 0006) |
| 6 | Ambiente de execução | Plataforma → Harness | EP-04 do PRD (Next do roadmap) |
| 7 | Sensores | Harness | `doctor` + 4 sensores rodando |
| 8 | Governança | Harness | escrita, não mecanizada |
| 9 | Guardrails | Plataforma | emprestado; nada nosso |
| 10 | Observabilidade | — | não existe |
| 11 | Orquestração | Harness | em prosa, na `mjrp-pdlc` |

---

### 1 · Loop de execução
**O que é.** O ciclo que faz o agente avançar sozinho: observa, decide o próximo passo, age, lê o
resultado, repete. Sem ele não há agente — há chat.

**A divisão que importa.** O **loop do turno** é da Plataforma: o modelo chama uma ferramenta, lê
o resultado, chama de novo, e para quando *ele mesmo* emite texto sem chamar nada. A condição de
parada padrão é uma **opinião do modelo**, não um fato verificado. O **loop da tarefa** é nosso:
repetir o turno até um critério verificável passar, com o estado viajando por arquivo.

**No MJRP.** Só o primeiro existe, emprestado. O segundo é o `loop.py` planejado, e é o que o
invariante nº 12 exige — nenhum loop começa sem critério de saída declarado e verificável.

### 2 · Ferramentas
**O que é.** Tudo o que o agente pode **chamar para agir**. Ver tools para os três
sentidos da palavra e as três camadas.

**No MJRP.** É a peça que mais falta. Skill é o guia que ensina a usar uma ferramenta; guia
apontando para nada é conselho. O campo `tools:` do contrato e o catálogo de categorias não
existem ainda.

**Cuidado documentado.** A Vercel removeu 80% das ferramentas de um agente e a performance
**melhorou**. Ferramenta não usada não é neutra: come contexto e cria caminho errado. O catálogo
precisa de regra de entrada, como as checagens do `doctor` têm.

### 3 · Guides
**O que é.** O que orienta **antes** da ação (feedforward): specs, regras, skills, `AGENTS.md`.
É sempre um **pedido** — o agente pode não seguir.

**No MJRP.** É onde estamos mais fortes e é o risco: guide é inferencial, custa token e atenção a
cada sessão. Trocar guide por sensor é o que baixa a conta.

### 4 · Context engineering
**O que é.** Decidir o que entra na janela, quando e em que forma. Quatro operações: *write*
(mesa → arquivo), *select* (arquivo → mesa), *compress* (encolher), *isolate* (dividir entre
agentes).

**No MJRP.** A `mjrp-pdlc-onboarding` é o *select*; o handoff é o *write*; o *compress* é da
Plataforma; o *isolate* é a fábrica, que ainda não existe. **Ninguém mede** quanto custa o
carregamento — e por *context rot*, excesso não é só caro, é pior.

### 5 · Memória
**O que é.** O que persiste **fora** da janela e precisa ser recuperado para virar contexto.
Memória é fonte de contexto, não a mesma coisa.

**No MJRP.** Seis tipos com casa: instruções (`AGENTS.md`), contrato, semântica, decisória
(`docs/decisions/`), episódica (`log.md`) e **aprendida + ativa** (`MEMORY.md`).
Cinco são escritas por humano; só a aprendida é escrita pelo agente.

### 6 · Ambiente de execução
**O que é.** Onde o agente roda, e com que raio de explosão. Duas metades: o **sandbox** (o
ambiente do agente) e o **provisionamento** (o ambiente do produto).

**No MJRP.** Hoje os sensores rodam onde calha — Mac, ponte, container — e isso não é ambiente, é
acaso. O **EP-04** (ambiente do agente e do produto) traz o sandbox da Plataforma para o Harness, e é pré-requisito da autonomia:
agente autônomo sem isolamento tem a máquina inteira como raio de explosão.

### 7 · Sensores
**O que é.** O que detecta **depois** da ação que algo saiu errado, sem depender do agente
cooperar. Devolve 0 ou 1. Ver [[terms]].

**A hierarquia de força.** Compilador e sistema de tipos > teste e CI > linter e schema > segundo
modelo revisando > auto-relato do agente (que não é sensor nenhum). **A linguagem é um sensor**:
escolher stack tipada é escolher um verificador de força máxima que roda de graça.

**No MJRP.** `doctor` com contrato 0/1/2 e quatro sensores rodando. **O furo:** ele verifica a
conformidade da instância, não o trabalho entregue.

### 8 · Governança
**O que é.** Quem pode fazer o quê, e o que exige aprovação. No nível da chamada de ferramenta:
*always do / ask first / never do*.

**No MJRP.** Existe escrita — os gates, o `PRINCIPLES.md` — mas **não mecanizada**: nada intercepta
uma chamada. É pedido, não regra.

### 9 · Guardrails
**O que é.** O limite que **impede** a ação antes de acontecer — distinto do sensor, que detecta
depois. Permissão negada, caminho fora do sandbox, orçamento estourado.

**No MJRP.** Nada nosso. O que existe é o sistema de permissão da Plataforma. Migra junto com o
EP-04, pela mesma razão do sandbox.

### 10 · Observabilidade
**O que é.** Conseguir diagnosticar **sem fazer deploy novo** — distinta de monitoring, que só
avisa que quebrou. Que skill disparou, que ferramenta foi chamada, quanto custou.

**No MJRP.** Não existe como evals de skill (candidato no PRD); o que já existe é o rastro datado de `daily-checks/` e o verificador do entregável, EP-02 — é o que permite melhorar com dado em vez de impressão.

### 11 · Orquestração
**O que é.** Quem roteia entre as fases: passa o estado, escolhe o próximo papel, para nos gates.

**No MJRP.** Existe em **prosa**, na `mjrp-pdlc` — um orquestrador executado por
leitura, não por código. **Entre fases, grafo** (o fluxo é conhecido de antemão); **dentro de cada
fase, loop** (o trabalho do papel é exploratório).

## How MJRP uses it

- **O domínio de cada peça é campo do contrato**, não linha do documento de visão: num stack que
  entrega o loop, o loop passa a ser seu.
- **Cinco peças são computacionais** e custam ~zero quando passam; as outras são inferenciais, e
  inferencial é o caro. Trocar conselho por mecanismo é o que baixa a conta.
- **A peça que falta de verdade são as ferramentas** (2), e as que não existem são observabilidade
  (10) e guardrails (9).

## History

> A decisão mora na página do assunto que ela muda, com data (ADR-0008). As entradas abaixo
> vieram **inteiras** do `MEMORY.md` na migração do BACKLOG #28a (09/09/2026) — nada foi
> condensado na mudança.
- **2026-09-07** · As peças passaram a ser **onze** — entrou `guardrails` ao lado de governança.
- **2026-09-14 20:57** · **Os onze validados pelo MJRP** — *"validado por ora, se precisar evoluímos e
  modificamos no futuro"*. A página passa de *em formação* a **firme**; foi a última pendência de
  dono MJRP no fio da cadeia de intenção (BACKLOG #7). A página viaja no kernel de todo projeto.
- **2026-09-08 14:53** · As **onze peças** viram `docs/wiki/harness-elements.md`, com cada elemento
  detalhado — o Zé valida depois. Não é ponteiro para o nada.
- **2026-09-21 16:51** · **A peça #10 (Observabilidade) ganha corpo: o Harness Control Center (EP-08).** Brief
  aprovado pelo MJRP — escopo discovery + prototipação (entrega um protótipo das informações do
  cockpit, não o app). Casa: subprojeto aninhado `apps/control-center/`, porque o cockpit lê os
  arquivos do próprio harness e pertence ao repo. A seção "resultado dos sensores" do cockpit é a
  #10 de verdade; o resto (diagrama, docs por fase, Kernel, memory/log, roadmap) é um Docs Plane.
  Detalhe: `docs/log.md` [2026-09-21 16:51].

## Related
tools · [[terms]] · [[vision-document]] · ADR-0005 · ADR-0006
