**MJRP Vibe Coding Framework**

v1.2 --- Brownfield Projects

*Para projetos já existentes com código, dados e histórico*

Stack: Claude Code + Claude Cowork + Antigravity + Stitch + SDD
(SpecKit)

**Introdução: Greenfield vs. Brownfield**
=========================================

A V1.1 (Greenfield) assume um projeto iniciado do zero. Este documento
(V1.2) adapta o framework para **projetos existentes** --- aqueles que
já possuem código, dados, configurações, histórico Git e possivelmente
sessões AI anteriores.

A diferença fundamental: em vez de criar artefatos do zero, o Brownfield
começa com um **Audit & Bootstrap** que mapeia o que já existe e o gap
em relação ao framework.

O documento segue a mesma estrutura da V1.1, mas com adições específicas
para a adaptação. Seções marcadas com ▶ são idênticas à V1.1. Seções
marcadas com ◆ são novas ou adaptadas para Brownfield.

**◆ 0. Step Zero: Audit & Bootstrap**
=====================================

Antes de qualquer outra ação, faça um levantamento completo do estado
atual do projeto. Este passo substitui os passos 1-4 do Greenfield.

**0.1 Inventário de Artefatos**
-------------------------------

Mapeie tudo que já existe no projeto:

  **Categoria**        **O que verificar**                           **Onde procurar**                             **Status**
  -------------------- --------------------------------------------- --------------------------------------------- ------------
  Código               Linguagens, frameworks, estrutura de pastas   src/, package.json, requirements.txt          ☐ Mapeado
  Dados                Schemas, modelos, conteúdo existente          DB, vault, APIs, arquivos                     ☐ Mapeado
  Git                  Branches, commits, histórico                  git log, git branch -a                        ☐ Mapeado
  Documentação         Specs, docs, READMEs existentes               docs/, README.md, \*.md                       ☐ Mapeado
  Ferramentas AI       Configs, históricos, prompts                  .gemini/, .mcp.json, .claudeprompt, skills/   ☐ Mapeado
  Design               Prototipos, wireframes, UI existente          Stitch, Figma, screenshots                    ☐ Mapeado
  Sessões anteriores   Contexto de sessões AI passadas               SESSION\_HISTORY.md, chats salvos             ☐ Mapeado

**0.2 Gap Analysis**
--------------------

Com o inventário feito, identifique o que falta em relação ao framework:

  **Artefato do Framework**   **Já existe?**              **Ação necessária**         **Prioridade**
  --------------------------- --------------------------- --------------------------- ----------------
  VISION.md                   ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Alta
  CHARTER.md                  ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Alta
  constitution.md             ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Crítica
  story.md + spec.md          ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Alta
  arch.md + data-model.md     ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Alta
  design-system.md            ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Média
  tasks.md                    ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Alta
  SESSION\_HISTORY.md         ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Alta
  .claudeprompt               ☐ Sim / ☐ Parcial / ☐ Não   Criar / Extrair / Adaptar   Média
  Folder structure            ☐ Sim / ☐ Parcial / ☐ Não   Reorganizar / Manter        Média

> **DICA BROWNFIELD:** *Não reorganize tudo de uma vez. Priorize
> constitution.md e VISION.md primeiro --- são os arquivos que os
> agentes AI consultam antes de qualquer ação.*

**0.3 Bootstrap: Extrair vs. Criar**
------------------------------------

Para cada artefato faltante, decida entre **Extrair** (derivar de
material existente) ou **Criar** (escrever do zero). A regra é simples:

-   **Extrair** quando já existe conteúdo equivalente em outro formato
    > (ex: spec no Google Docs, decisões em chat do Stitch, stack
    > definida no package.json).

-   **Criar** quando não há material equivalente.

-   **Adaptar** quando o artefato existe mas está incompleto ou em
    > formato diferente.

> **DICA BROWNFIELD:** *Use o Cowork para fazer a extração. Ele pode ler
> Google Docs, vault files, chats do Stitch e gerar os artefatos no
> formato correto.*

**◆ 1. Fluxo de Execução Brownfield**
=====================================

O fluxo Brownfield difere do Greenfield nos primeiros passos. Após o
bootstrap, o ciclo de desenvolvimento é idêntico.

1.  **Audit & Bootstrap (Step 0):** Execute o inventário e gap analysis
    > da seção anterior. Documente em BOOTSTRAP\_REPORT.md.

2.  **Extrair/Criar Visão:** Gere VISION.md e CHARTER.md a partir de
    > material existente (docs, chats, código). Commit: docs: bootstrap
    > vision and charter

3.  **Retratar o Estado Atual:** Crie constitution.md refletindo a stack
    > e padrões **já em uso**, não os ideais. Evolua gradualmente.

4.  **Adaptar Folder Structure:** Reorganize pastas apenas onde
    > necessário para acomodar docs/specs/. Não mova código existente
    > sem necessidade.

5.  **Retrofitting SpecKit:** Documente o estado atual das features já
    > implementadas em story.md e spec.md (veja seção 5).

6.  **Consolidar Design System:** Se já existe UI, extraia tokens
    > visuais para design-system.md (seção 6).

7.  **Ativar Ambiente Multi-AI:** Configure cada ferramenta com os
    > artefatos recém-criados (seção 7).

8.  **Migrar Contexto:** Consolide sessões anteriores em
    > SESSION\_HISTORY.md (seção 8).

9.  **Ciclo de Desenvolvimento (Iterativo):** Mesmo da V1.1 --- Specify
    > → Plan → Tasks → Implement.

10. **Context Handoff:** Mesmo da V1.1.

> **DICA BROWNFIELD:** *O passo 3 é crucial: o constitution.md deve
> refletir a REALIDADE, não o IDEAL. Se o projeto usa JavaScript puro,
> não escreva TypeScript no constitution só porque seria melhor.
> Evoluções entram como features futuras no backlog.*

**◆ 2. Template: Folder Structure (Adaptação)**
===============================================

Em projetos Brownfield, a regra é **adicionar sem quebrar**. A
estrutura-alvo é a mesma da V1.1, mas a migração é incremental.

**2.1 Princípios de Migração**
------------------------------

-   **Não mova código que funciona.** Se src/ está organizado diferente,
    > mantenha.

-   **Adicione docs/specs/ como camada.** Esta é a única pasta
    > obrigatória.

-   **Crie docs/sessions/ para contexto.** SESSION\_HISTORY.md vai aqui.

-   **Mantenha configs AI onde estão.** Se .gemini/ já existe na raiz,
    > não mova.

**2.2 Exemplo: Projeto existente com vault**
--------------------------------------------

Se o projeto já tem código, scripts e um vault Obsidian:

> /meu-projeto-existente
>
> ├── .gemini/ \# JÁ EXISTE --- manter
>
> ├── .mcp.json \# JÁ EXISTE --- manter
>
> ├── MJRPvault/ \# JÁ EXISTE --- manter (dados)
>
> ├── scripts/ \# JÁ EXISTE --- manter
>
> ├── skills/ \# JÁ EXISTE --- manter
>
> ├── docs/ \# EXISTENTE --- expandir
>
> │ ├── specs/ \# NOVO --- adicionar
>
> │ │ ├── constitution.md
>
> │ │ ├── story.md
>
> │ │ ├── arch.md
>
> │ │ ├── data-model.md
>
> │ │ ├── spec.md
>
> │ │ ├── plan.md
>
> │ │ ├── tasks.md
>
> │ │ └── design-system.md
>
> │ ├── sessions/ \# NOVO --- adicionar
>
> │ │ └── SESSION\_HISTORY.md
>
> │ └── \[docs existentes\] \# MANTER
>
> ├── src/ \# FUTURO --- quando web dev começar
>
> ├── .claudeprompt \# NOVO --- adicionar
>
> ├── VISION.md \# NOVO --- adicionar
>
> ├── CHARTER.md \# NOVO --- adicionar
>
> └── README.md \# EXISTENTE --- atualizar
>
> **DICA BROWNFIELD:** *Use um único commit para toda a reorganização:
> docs: bootstrap framework structure. Isso facilita reverter se algo
> quebrar.*

**◆ 3. SCM & Governance (Adaptação)**
=====================================

Se o projeto já tem histórico Git, não altere o passado. Aplique as
convenções daqui para frente.

**3.1 Lidando com Histórico Existente**
---------------------------------------

-   **Não faça rebase ou squash do histórico.** O passado é o passado.

-   **A partir do bootstrap, siga Conventional Commits** (mesmas regras
    > da V1.1).

-   **Crie uma tag** marcando o início do framework: git tag -a
    > v0-framework-bootstrap -m \"Start of MJRP Framework\"

-   **Se branches já existem,** mantenha-as até merge natural. Não force
    > o modelo main/dev se não existia.

**3.2 Commit de Bootstrap**
---------------------------

O primeiro commit do framework deve incluir todos os novos artefatos:

> docs: bootstrap MJRP Framework v1.2
>
> \- Add VISION.md, CHARTER.md
>
> \- Add docs/specs/ with constitution, story, spec, arch, data-model,
> plan, tasks
>
> \- Add docs/sessions/SESSION\_HISTORY.md
>
> \- Add .claudeprompt
>
> \- Tag: v0-framework-bootstrap

**3.3 Padrão de Commits (mesmo da V1.1)**
-----------------------------------------

-   **feat:** Nova funcionalidade.

-   **fix:** Correção de bug.

-   **docs:** Alteração em documentação/specs.

-   **refactor:** Mudança no código sem alterar comportamento.

-   **vibe:** Ajustes de UI/UX baseados em feedback estético.

-   **chore:** Tarefas de manutenção (deps, configs).

**3.4 Regra: Commits vinculados ao SpecKit (mesmo da V1.1)**
------------------------------------------------------------

Cada transição de estágio do SpecKit gera um commit de docs:

-   Specify concluído → **docs: complete specify stage for \[feature\]**

-   Plan concluído → **docs: complete plan stage for \[feature\]**

-   Tasks gerados → **docs: generate tasks for \[feature\]**

-   Implement concluído → **feat: implement \[feature\]** (com ref à
    > task)

**◆ 4. Templates de Definição (com Guia de Extração)**
======================================================

Templates idênticos à V1.1. A diferença é que no Brownfield você
provavelmente **extrai** informações de material existente em vez de
criar do zero.

**4.1 VISION.md (mesma da V1.1)**
---------------------------------

> \# \[Project Name\]
>
> \#\# Core Objective
>
> \[Uma frase curta que define o sucesso\]
>
> \#\# The Vibe
>
> \[ex: Organic Blueprint --- creme, verde floresta, tipografia
> serifada\]
>
> \#\# User Empathy
>
> \[Qual a dor principal que estamos aliviando?\]
>
> \#\# Design DNA
>
> \[Referência visual --- screenshot, link Stitch, ou descrição\]
>
> **DICA BROWNFIELD:** *Fontes comuns para extrair a visão: Google Docs
> de documentação, chats do Stitch com decisões de design, README
> existente, conversas de sessões AI anteriores.*

**4.2 CHARTER.md (mesma da V1.1)**
----------------------------------

Elementos essenciais:

-   **Title and Description:** Nome e visão geral do que será feito.

-   **Justification (Business Case):** O motivo --- problema ou
    > oportunidade.

-   **Main Goals and Success Metrics:** O que se espera, de forma
    > mensurável.

-   **High-Level Scope:** O que está incluído e o que está fora.

-   **Main Stakeholders:** Sponsor, PM e partes interessadas.

-   **Roadmap (Milestones):** Datas e entregas principais.

-   **Risks and Constraints:** Problemas potenciais e limitações.

-   **AI Tooling:** Quais ferramentas AI serão usadas e com qual papel
    > (seção 7).

> **DICA BROWNFIELD:** *Para projetos existentes, adicione uma seção
> \'Current State\' ao CHARTER com: o que já foi feito, o que está
> funcionando, e o que precisa mudar.*

**◆ 5. SpecKit: Retrofitting em Projeto Existente**
===================================================

O maior desafio do Brownfield: documentar o que já existe antes de
avançar. Isto se chama **Retrofitting** e é essencial para que os
agentes AI entendam o contexto.

**5.1 Retrofitting: Os 3 Níveis**
---------------------------------

  **Nível**   **Quando usar**                      **O que documentar**                                   **Esforço**
  ----------- ------------------------------------ ------------------------------------------------------ -------------
  Minimal     Projeto peq., poucas features        constitution.md + story.md com lista de features       1-2 horas
  Standard    Projeto médio, próx. fase complexa   constitution + story + spec + arch + data-model        3-5 horas
  Full        Projeto grande, múltiplos devs/AI    Todos os artefatos + design-system + plan retroativo   1-2 dias

**5.2 Processo de Retrofitting**
--------------------------------

11. **Documente a Stack Atual** em constitution.md. Inclua versões,
    > deps, e padrões observados (não idealizados).

12. **Liste Features Existentes** em story.md. Para cada feature,
    > descreva o que já funciona em formato de user story.

13. **Documente a Arquitetura** em arch.md. Mapeie os componentes e suas
    > interações. Diagrams são bem-vindos (Mermaid no Markdown).

14. **Modelos de Dados** em data-model.md. Schemas, interfaces,
    > frontmatter conventions (ex: vault Obsidian).

15. **Crie o Backlog** em tasks.md. Combine dívidas técnicas, features
    > planejadas e melhorias.

> **DICA BROWNFIELD:** *O Cowork é excelente para retrofitting: ele pode
> ler a codebase, o vault, o histórico Git e gerar os artefatos
> automaticamente. Use-o.*

**5.3 Os 4 Estágios (mesmos da V1.1, aplicados daqui para frente)**
-------------------------------------------------------------------

Após o retrofitting, o fluxo é idêntico ao Greenfield:

-   **SPECIFY:** Defina intenções. Input: ideia, designs, dados. Output:
    > story.md e spec.md atualizados.

-   **PLAN:** Propõe a arquitetura técnica. Output: arch.md,
    > data-model.md e plan.md atualizados.

-   **TASKS:** Quebre em unidades atômicas. Output: tasks.md com
    > checklist.

-   **IMPLEMENT:** Execute tarefa por tarefa. Output: código em src/,
    > testes em tests/.

**5.4 Gates de Aprovação (Obrigatório)**

Cada transição entre estágios exige aprovação humana explícita. O agente
AI não pode avançar sem validação:

-   Specify → Plan: Spec deve estar APPROVED pelo usuário

-   Plan → Tasks: Plan deve estar APPROVED pelo usuário

-   Tasks → Implement: Task list deve estar APPROVED pelo usuário

O agente deve solicitar revisão ao final de cada estágio e aguardar
confirmação antes de prosseguir. Nenhum estágio pode ser pulado ou
combinado --- é um estágio por vez.

**5.5 Regra de Interrupção de Fluxo**

Se durante qualquer estágio o usuário alterar requisitos que impactam um
estágio anterior, o fluxo deve retroceder:

-   Mudança de requisito durante Plan → voltar ao Specify

-   Mudança de arquitetura durante Tasks → voltar ao Plan

-   Mudança de escopo durante Implement → voltar ao estágio apropriado
    > (Specify ou Plan)

O retrocesso gera um novo commit de docs registrando a mudança: docs:
revise \[stage\] for \[feature\] --- requirement change

**5.**6 **O Constitution.md (mesmo template da V1.1)**
------------------------------------------------------

Funciona como as Leis da Robótica do projeto:

> \# Project Constitution
>
> \#\# 1. Technical Stack
>
> \- Frontend: \[stack ATUAL, não a ideal\]
>
> \- Styling: \[o que está em uso AGORA\]
>
> \- Backend: \[serviços EXISTENTES\]
>
> \- Data: \[fontes de dados atuais\]
>
> \#\# 2. Development Methodology (SDD)
>
> \- Fluxo: Specify -\> Plan -\> Tasks -\> Implement
>
> \- Nenhuma implementação sem Task definida em tasks.md
>
> \- Iteração via \[Scrum sprints / Kanban features\]
>
> \#\# 3. SCM & Governance
>
> \- Branching: \[modelo ATUAL\] (migrar p/ main/dev se necessário)
>
> \- Commits: Conventional Commits a partir de \[data\]
>
> \#\# 4. AI Orchestration
>
> \- \[Ferramentas já configuradas e seus papéis\]
>
> \#\# 5. Legacy Notes
>
> \- \[Decisões passadas e dívida técnica conhecida\]
>
> \- \[Padrões inconsistentes a corrigir gradualmente\]
>
> **DICA BROWNFIELD:** *A seção \'Legacy Notes\' é exclusiva do
> Brownfield. Serve para que os agentes AI saibam onde estão os pontos
> de atenção.*

**◆ 6. Design System (Extração)**
=================================

Se o projeto já tem UI (protótipos no Stitch, CSS existente, ou
screenshots), extraia os tokens visuais em vez de definir do zero.

**6.1 Fontes para Extração**
----------------------------

-   **Stitch/Figma:** Exporte as cores, fontes e espaçamentos dos
    > protótipos.

-   **CSS existente:** Extraia variáveis CSS, classes de utilidade,
    > breakpoints.

-   **Screenshots:** Use como referência visual para documentar o
    > padrão.

-   **Chats de design:** Decisões estéticas registradas em conversas com
    > AI.

**6.2 Template (mesmo da V1.1)**
--------------------------------

> \# Design System: \[Nome da Vibe\]
>
> \#\# Paleta de Cores
>
> \- Primary: \[hex\] --- \[uso\]
>
> \- Secondary: \[hex\] --- \[uso\]
>
> \- Background: \[hex\] --- \[uso\]
>
> \- Text Primary/Secondary: \[hex cada\]
>
> \- Accent/Success/Warning/Error: \[hex cada\]
>
> \#\# Tipografia
>
> \- Heading Font: \[nome + estilo\]
>
> \- Body Font: \[nome + estilo\]
>
> \- Scale: \[H1, H2, H3, Body em rem\]
>
> \#\# Espaçamento e Grid
>
> \- Base unit: \[ex: 8px\]
>
> \- Grid: \[colunas, gap\]
>
> \- Border radius: \[valores\]
>
> \#\# Componentes-Chave
>
> \- \[Componente\]: \[descrição + referência\]
>
> \#\# Referência Visual
>
> \- Stitch Project: \[link ou ID\]
>
> \- Tela de Referência: \[tela mestre\]

**▶ 7. Orquestração Multi-AI (mesma da V1.1)**
==============================================

Seção idêntica à V1.1. Cada ferramenta tem um papel definido:

  **Ferramenta**   **Papel**                              **Quando Usar**                                            **Contexto**
  ---------------- -------------------------------------- ---------------------------------------------------------- --------------------------------------------
  Claude Cowork    Brainstorming, análise, planejamento   Sessões de pareamento, criação de specs, retrofitting      Lê workspace folder, Google Drive, browser
  Claude Code      Coding no terminal                     Implementação, refactoring, testes, git ops                Lê repo inteiro via .claudeprompt
  Antigravity      Builder: Coding + Git                  Implementação, refactoring, testes, code review, Git ops   Repo GitHub via integração nativa
  Stitch           Design com AI                          Prototipação, UI/UX, design system visual                  Projeto Stitch via MCP

**7.1 Fluxo de Contexto (mesmo da V1.1)**
-----------------------------------------

-   **Stitch → Git:** Designs exportados ou documentados em
    > design-system.md

-   **Cowork → Git:** Specs, análises, skills gerados salvos no repo

-   **Claude Code → Git:** Código commitado diretamente

-   **Antigravity → Git:** Código implementado e commitado via
    > integração GitHub

**7.2 .claudeprompt (mesmo da V1.1)**
-------------------------------------

> Você é um desenvolvedor trabalhando no projeto \[Nome\].
>
> Antes de qualquer implementação, leia:
>
> \- VISION.md (propósito)
>
> \- CHARTER.md (escopo e limites)
>
> \- docs/specs/constitution.md (regras técnicas)
>
> \- docs/specs/design-system.md (padrões visuais)
>
> \- docs/specs/tasks.md (backlog atual)
>
> Regras:
>
> \- Siga Conventional Commits
>
> \- Nunca implemente sem task em tasks.md
>
> \- Consulte constitution.md antes de sugerir deps

**◆ 8. Context Handoff & Migração**
===================================

No Brownfield, além do handoff entre sessões futuras, há o desafio de
**migrar contexto de sessões passadas** que não seguiam o framework.

**8.1 Migração de Sessões Anteriores**
--------------------------------------

Se houve sessões AI antes da adoção do framework:

16. **Localize históricos:** Busque em
    > .gemini/antigravity/conversations/, chats do Cowork,
    > SESSION\_HISTORY.md existente.

17. **Extraia decisões-chave:** Leia os históricos e liste as decisões
    > que impactam o projeto (stack, padrões, exclusões de escopo).

18. **Consolide em SESSION\_HISTORY.md:** Use o template abaixo para
    > criar um entry retroativo.

19. **Alimente os artefatos:** Decisões encontradas devem ir para
    > constitution.md, story.md, ou arch.md conforme aplicável.

> **DICA BROWNFIELD:** *O Cowork é ideal para esta tarefa: pode ler
> múltiplas fontes e consolidar num único SESSION\_HISTORY.md.*

**8.2 Template SESSION\_HISTORY.md (mesmo da V1.1)**
----------------------------------------------------

> \# \[Projeto\] --- Histórico de Sessão
>
> \> Data: \[data\]
>
> \> Participantes: \[humano\] + \[AI tool\]
>
> \> Branch: \[branch ativa\]
>
> \#\# Resumo Executivo
>
> \[2-3 frases do que foi feito\]
>
> \#\# Decisões Tomadas
>
> \[Lista de decisões com contexto\]
>
> \#\# Artefatos Gerados/Modificados
>
> \[Tabela: arquivo \| descrição \| versão\]
>
> \#\# Pendências para Próxima Sessão
>
> \[Lista ordenada por prioridade\]
>
> \#\# Dados-Chave para Referência
>
> \[Métricas, contagens, valores importantes\]

**8.3 Entry Retroativo (específico Brownfield)**
------------------------------------------------

Para sessões que aconteceram antes do framework, use este formato
adicional:

> \#\# \[RETROATIVO\] Sessão Consolidada: \[período\]
>
> \> Fontes: \[Antigravity chats, Cowork sessions, commits\]
>
> \> Consolidado por: \[ferramenta\] em \[data\]
>
> \#\#\# O que foi feito
>
> \[Resumo das atividades do período\]
>
> \#\#\# Decisões que impactam o projeto
>
> \[Apenas decisões relevantes para o futuro\]
>
> \#\#\# Estado ao final
>
> \[Snapshot: o que existia ao final deste período\]

**9. Skills, Workflows e Setup das Ferramentas AI**
===================================================

O framework inclui um conjunto de Skills e Workflows prontos para uso,
além de um Guia de Setup que detalha como instalá-los em cada ferramenta
AI.

**9.1 Skills (12)**
-------------------

Skills ensinam ao agente AI como fazer algo bem. São conhecimento
especializado ativado automaticamente quando relevante. O framework
inclui:

**Temáticas (7):** SDD SpecKit, Context Handoff, Project Bootstrap,
Multi-AI Orchestration, Design System, Conventional Commits, Code
Quality.

**Role-based (5):** UX/UI Designer, Frontend Developer, Backend
Developer, Mobile Developer, QA Engineer.

**9.2 Workflows (14 ativos)**
-----------------------------

Workflows definem processos passo a passo que o agente executa. Incluem:

**SDD (4):** sdd\_protocol, sdd\_specify\_protocol, sdd\_plan\_protocol,
sdd\_task\_protocol.

**Contexto (2):** onboarding\_protocol, developer\_protocol.

**Qualidade (4):** debug\_protocol, regression\_protocol,
documentation\_protocol, check\_documentation\_protocol.

**Audit & Governança (4):** architecture\_decision\_protocol,
documentation\_audit\_protocol, test\_suite\_audit\_protocol,
code\_quality\_assessment\_protocol.

**9.3 Setup por Ferramenta**
----------------------------

O arquivo SETUP\_GUIDE\_AI\_Tools.md (incluído no framework) detalha
como instalar skills e workflows em cada ferramenta:

**Claude Code + Cowork:** Workflows como slash commands em
.claude/commands/. Skills referenciadas em .claudeprompt (Code) ou
detectadas automaticamente em skills/ (Cowork).

**Antigravity:** Skills em .agent/skills/ com SKILL.md (auto-descoberta
via Progressive Disclosure). Workflows em .agent/workflows/. Rules em
.agent/rules/.

**9.4 Nota sobre Antigravity como Builder**
-------------------------------------------

Antigravity e Claude Code são ambos Builders. A escolha entre eles
depende de preferência pessoal: Claude Code é terminal-first (ideal para
quem vive no terminal), Antigravity é visual-first (ideal para quem
prefere UI e integração direta com GitHub). Ambos podem executar
tasks.md com a mesma qualidade.

**9.5 Templates (10)**
----------------------

O framework inclui 10 templates prontos em 3.MJRP-Templates/ para
documentação recorrente do projeto:

**Onboarding (4):** onboarding\_developer, onboarding\_qa,
onboarding\_ux\_ui, onboarding\_devops.

**Governança (3):** adr\_template (Architecture Decision Records),
technical\_debt (registro de dívida técnica), agent\_rules\_template
(guia de regras para agentes).

**Operacionais (3):** reference\_guide\_index (índice numerado do
manual), implementation\_walkthrough (documentação de implementação),
roadmap (roadmap evolutivo do projeto --- complementa a seção de
Milestones do CHARTER.md).

**Apêndice: Checklist de Bootstrap Brownfield**
===============================================

  **\#**   **Ação**                                     **Método**        **Commit**
  -------- -------------------------------------------- ----------------- --------------------------
  1        Executar Audit & Inventário                  Cowork + manual   ---
  2        Executar Gap Analysis                        Cowork            ---
  3        Criar/Extrair VISION.md                      Extrair de docs   docs: bootstrap vision
  4        Criar/Extrair CHARTER.md                     Extrair de docs   docs: bootstrap charter
  5        Criar constitution.md (stack ATUAL)          Extrair de code   docs: constitution
  6        Criar docs/specs/ folder structure           Manual            chore: speckit structure
  7        Retrofitting: story.md + spec.md             Cowork + code     docs: retrofit specs
  8        Retrofitting: arch.md + data-model.md        Cowork + code     docs: retrofit arch
  9        Extrair design-system.md (se UI existe)      Stitch + CSS      docs: design system
  10       Criar tasks.md (backlog consolidado)         Cowork            docs: initial backlog
  11       Criar .claudeprompt                          Manual            chore: AI config
  12       Migrar sessões anteriores                    Cowork            docs: session history
  13       Tag: v0-framework-bootstrap                  Git               tag only
  14       Iniciar ciclo Specify para próxima feature   Normal flow       docs: specify \[feat\]
