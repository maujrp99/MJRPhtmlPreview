**MJRP Vibe Coding Framework**

v1.1 --- Greenfield Projects

Stack: Claude Code + Claude Cowork + Antigravity + Stitch + SDD
(SpecKit)

**1. Fluxo de Execução Passo a Passo**
======================================

O fluxo abaixo é sequencial na primeira passada. Após o setup inicial, o
ciclo de desenvolvimento (passo 8) itera via Agile/Scrum com sprints ou
Kanban por feature.

1.  **Visão e Charter:** Defina a Ideia e Visão do Produto. Preencha os
    > templates de VISION.md e CHARTER.md (seção 4).

2.  **Diretório e SCM:** Crie a pasta do projeto e inicialize o Git com
    > o padrão de branches (seção 3). Primeiro commit: estrutura vazia +
    > docs iniciais.

3.  **Folder Structure:** Aplique o template de pastas (seção 2) para
    > organizar o conhecimento da IA.

4.  **Baseline Docs:** Crie README.md, VISION.md e CHARTER.md na raiz.

5.  **Setup SDD (SpecKit):** Crie a pasta docs/specs/ e popule os
    > artefatos do SpecKit (seção 5). Commit de docs após cada estágio.

6.  **Design System:** Crie docs/specs/design-system.md com tokens
    > visuais, paleta de cores, tipografia e componentes (seção 6).

7.  **Ativação do Ambiente Multi-AI:** Configure cada ferramenta com seu
    > papel definido (seção 7).

8.  **Sincronização de Contexto:** Em cada ferramenta, carregue os
    > arquivos de visão: VISION.md, CHARTER.md, docs/specs/.

9.  **Ciclo de Desenvolvimento (Iterativo):** Sprints ou features
    > seguindo Specify → Plan → Tasks → Implement. Cada iteração produz
    > commits seguindo o padrão SCM.

10. **Context Handoff:** Ao final de cada sessão, atualize o
    > SESSION\_HISTORY.md (seção 8).

**2. Template: Folder Structure**
=================================

Estrutura que facilita a leitura por agentes AI e organiza o SpecKit
como cérebro do projeto.

> /meu-projeto
>
> ├── .github/ \# Workflows de CI/CD (GitHub Actions)
>
> ├── .claudeprompt \# System prompt persistente do Claude Code
>
> ├── .gemini/ \# Config do Antigravity (GEMINI.md)
>
> ├── docs/
>
> │ ├── specs/ \# SpecKit (a alma do projeto)
>
> │ │ ├── constitution.md \# Contrato mestre: stack, regras, padrões
>
> │ │ ├── story.md \# Requisitos funcionais e histórias
>
> │ │ ├── arch.md \# Blueprint da arquitetura
>
> │ │ ├── data-model.md \# Interfaces/modelos de dados
>
> │ │ ├── spec.md \# O que o sistema deve fazer
>
> │ │ ├── plan.md \# Mapeamento da experiência
>
> │ │ ├── tasks.md \# Backlog/checklist de progresso
>
> │ │ └── design-system.md \# Tokens visuais, cores, tipografia
>
> │ ├── architecture/ \# Diagramas e ADRs
>
> │ └── sessions/ \# Histórico de sessões AI
>
> │ └── SESSION\_HISTORY.md
>
> ├── src/ \# Código fonte
>
> ├── tests/ \# Testes
>
> ├── VISION.md \# A Vibe e o propósito
>
> ├── CHARTER.md \# Escopo, Limites e Stack
>
> ├── README.md \# Overview do projeto
>
> └── .gitignore

**3. Template: SCM & Governance (Git)**
=======================================

**3.1 Padrão de Branching**
---------------------------

-   **main:** Código estável e pronto para deploy.

-   **dev:** Integração de novas funcionalidades.

-   **feat/\[nome\]-\[timestamp\]:** Branches curtas para tarefas
    > específicas.

**3.2 Padrão de Commits (Conventional Commits)**
------------------------------------------------

-   **feat:** Nova funcionalidade.

-   **fix:** Correção de bug.

-   **docs:** Alteração em documentação/specs.

-   **refactor:** Mudança no código sem alterar comportamento.

-   **vibe:** Ajustes de UI/UX baseados em feedback estético.

-   **chore:** Tarefas de manutenção (deps, configs).

**3.3 Regra: Commits vinculados ao SpecKit**
--------------------------------------------

Cada transição de estágio do SpecKit gera um commit de docs, criando um
snapshot auditável:

-   Specify concluído → **docs: complete specify stage for \[feature\]**

-   Plan concluído → **docs: complete plan stage for \[feature\]**

-   Tasks gerados → **docs: generate tasks for \[feature\]**

-   Implement concluído → **feat: implement \[feature\]** (com ref à
    > task)

**4. Templates de Definição**
=============================

**4.1 VISION.md (A Vibe)**
--------------------------

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

**4.2 CHARTER.md (As Fronteiras)**
----------------------------------

Elementos essenciais conforme PMI e Asana:

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

**5. SpecKit: Os 4 Estágios**
=============================

O SpecKit é o Input de Contexto para agentes AI. O fluxo é iterativo:
cada sprint ou feature percorre os 4 estágios. Artefatos existentes
(designs do Stitch, protótipos, dados) são inputs válidos para Specify e
Plan.

**5.1 SPECIFY (O Que e Por Que)**
---------------------------------

Defina intenções. Forneça uma ideia ou requisito e a AI gera
especificação detalhada.

-   **Foco:** Regras de negócio, casos de uso, critérios de aceitação.

-   **Input:** Ideia vaga, designs existentes (Stitch), dados reais,
    > feedback de usuário.

-   **Output:** story.md e spec.md atualizados.

-   **Checkpoint:** Revisão humana antes de prosseguir.

-   **Commit:** docs: complete specify stage for \[feature\]

**5.2 PLAN (O Como)**
---------------------

Com a spec aprovada, a AI propõe a arquitetura técnica.

-   **Foco:** Bibliotecas, schemas, estrutura de arquivos, design de
    > sistema.

-   **Output:** arch.md, data-model.md e plan.md atualizados.

-   **Checkpoint:** Revisão humana.

-   **Commit:** docs: complete plan stage for \[feature\]

**5.3 TASKS (Decomposição)**
----------------------------

O plano técnico é quebrado em unidades atômicas de trabalho.

-   **Foco:** Tarefas pequenas o suficiente para codificar sem estourar
    > tokens.

-   **Output:** tasks.md com checklist de progresso.

-   **Commit:** docs: generate tasks for \[feature\]

**5.4 IMPLEMENT (Execução)**
----------------------------

A AI pega as tarefas uma a uma e escreve código, testes e docs.

-   **Foco:** Código limpo que adere à spec e ao constitution.md.

-   **Output:** Código em src/, testes em tests/.

-   **Commit:** feat/fix: \[descrição\] (ref task)

**5.5 Gates de Aprovação (Obrigatório)**

Cada transição entre estágios exige aprovação humana explícita. O agente
AI não pode avançar sem validação:

-   Specify → Plan: Spec deve estar APPROVED pelo usuário

-   Plan → Tasks: Plan deve estar APPROVED pelo usuário

-   Tasks → Implement: Task list deve estar APPROVED pelo usuário

O agente deve solicitar revisão ao final de cada estágio e aguardar
confirmação antes de prosseguir. Nenhum estágio pode ser pulado ou
combinado --- é um estágio por vez.

**5.6 Regra de Interrupção de Fluxo**

Se durante qualquer estágio o usuário alterar requisitos que impactam um
estágio anterior, o fluxo deve retroceder:

-   Mudança de requisito durante Plan → voltar ao Specify

-   Mudança de arquitetura durante Tasks → voltar ao Plan

-   Mudança de escopo durante Implement → voltar ao estágio apropriado
    > (Specify ou Plan)

O retrocesso gera um novo commit de docs registrando a mudança: docs:
revise \[stage\] for \[feature\] --- requirement change

**5.**7 **O Constitution.md**
-----------------------------

O artefato mais importante. Funciona como as Leis da Robótica do
projeto. A AI consulta este arquivo antes de cada decisão.

> \# Project Constitution
>
> \#\# 1. Technical Stack
>
> \- Frontend: \[Ex: Next.js 15 + TypeScript\]
>
> \- Styling: \[Ex: Tailwind CSS --- Vibe: Organic Blueprint\]
>
> \- Backend: \[Ex: Firebase / Supabase\]
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
> \- Branching: main (estável), dev (integração)
>
> \- Commits: Conventional Commits (feat, fix, docs, refactor, vibe)
>
> \- Review: Toda implementação validada contra story.md
>
> \#\# 4. AI Orchestration
>
> \- Regras de orquestração multi-AI (ver seção 7)
>
> \- Sempre verificar este arquivo antes de sugerir pacotes/padrões
>
> \#\# 5. Design System Reference
>
> \- Consultar design-system.md para decisões visuais
>
> \- Nunca desviar da paleta/tipografia definida

**6. Template: Design System**
==============================

Para projetos com interface visual, o design system é tão fundamental
quanto a tech stack. Este artefato garante consistência entre designers
(Stitch), desenvolvedores (Antigravity/Claude Code) e a UI final.

> \# Design System: \[Nome da Vibe\]
>
> \#\# Paleta de Cores
>
> \- Primary: \[hex\] --- \[uso: botões, links, acentos\]
>
> \- Secondary: \[hex\] --- \[uso: backgrounds, cards\]
>
> \- Background: \[hex\] --- \[uso: fundo principal\]
>
> \- Text Primary: \[hex\] --- \[uso: texto principal\]
>
> \- Text Secondary: \[hex\] --- \[uso: labels, meta\]
>
> \- Accent/Success/Warning/Error: \[hex cada\]
>
> \#\# Tipografia
>
> \- Heading Font: \[ex: Playfair Display --- serifada\]
>
> \- Body Font: \[ex: Inter --- sans-serif\]
>
> \- Code Font: \[ex: JetBrains Mono\]
>
> \- Scale: \[H1: 2.5rem, H2: 2rem, H3: 1.5rem, Body: 1rem\]
>
> \#\# Espaçamento
>
> \- Base unit: \[ex: 8px\]
>
> \- Grid: \[ex: 12 colunas, gap 24px\]
>
> \- Border radius: \[ex: 8px cards, 4px buttons\]
>
> \#\# Componentes-Chave
>
> \- Card: \[descrição + referência ao Stitch\]
>
> \- Nav Bar: \[descrição\]
>
> \- Book Cover Grid: \[descrição\]
>
> \#\# Referência Visual
>
> \- Stitch Project: \[link ou ID\]
>
> \- Tela de Referência: \[ID da tela mestre\]

**7. Orquestração Multi-AI**
============================

Cada ferramenta tem um papel definido. O contexto flui entre elas
através dos artefatos do SpecKit (que vivem no Git) e do
SESSION\_HISTORY.md.

  **Ferramenta**   **Papel**                              **Quando Usar**                                             **Contexto**
  ---------------- -------------------------------------- ----------------------------------------------------------- --------------------------------------------
  Claude Cowork    Brainstorming, análise, planejamento   Sessões de pareamento, criação de specs, análise de dados   Lê workspace folder, Google Drive, browser
  Claude Code      Coding no terminal                     Implementação, refactoring, testes, git ops                 Lê repo inteiro via .claudeprompt
  Antigravity      Builder: Coding + Git                  Implementação, refactoring, testes, code review, Git ops    Repo GitHub via integração nativa
  Stitch           Design com AI                          Prototipação, UI/UX, design system visual                   Projeto Stitch via MCP

**7.1 Fluxo de Contexto entre Ferramentas**
-------------------------------------------

O Git é o hub central. Todas as ferramentas lêem e escrevem no mesmo
repositório:

-   **Stitch → Git:** Designs exportados ou documentados em
    > design-system.md

-   **Cowork → Git:** Specs, análises, skills gerados salvos no repo

-   **Claude Code → Git:** Código commitado diretamente

-   **Antigravity → Git:** Código implementado e commitado via
    > integração GitHub

**7.2 .claudeprompt**
---------------------

System prompt persistente do Claude Code. Complementa o constitution.md
com instruções específicas para o Claude:

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

**8. Template: Context Handoff**
================================

Ao final de cada sessão de trabalho (especialmente no Cowork ou Claude
Code), atualize o SESSION\_HISTORY.md para preservar o contexto entre
sessões e entre ferramentas.

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

**Apêndice: Checklist de Setup Greenfield**
===========================================

  **\#**   **Ação**                                  **Commit**
  -------- ----------------------------------------- ----------------------------------
  1        Criar VISION.md e CHARTER.md              docs: initial vision and charter
  2        git init + .gitignore + primeiro commit   chore: project scaffold
  3        Criar folder structure completa           chore: folder structure
  4        Criar constitution.md                     docs: project constitution
  5        Criar design-system.md (se aplicável)     docs: design system
  6        Completar Specify para primeira feature   docs: specify \[feature\]
  7        Completar Plan                            docs: plan \[feature\]
  8        Gerar Tasks                               docs: tasks \[feature\]
  9        Configurar .claudeprompt e GEMINI.md      chore: AI config
  10       Iniciar Implement                         feat: \[feature\]
