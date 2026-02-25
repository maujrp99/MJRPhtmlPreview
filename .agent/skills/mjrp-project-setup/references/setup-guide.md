# Guia de Setup: Como Carregar Skills e Workflows nas Ferramentas AI

> Este guia mostra como instalar os artefatos do MJRP Vibe Coding Framework (skills, workflows, rules e templates) em cada ferramenta AI do ecossistema.
>
> **Inventário do Framework:**
> - **12 Skills** (7 temáticas + 5 role-based) — em `1.MJRP-AgentsSkills/`
> - **14 Workflows** (4 SDD + 2 Context + 4 Quality + 4 Audit/Governance) — em `2.MJRP-AgentsWorkflows/`
> - **10 Templates** (onboarding, ADR, tech debt, roadmap, reference guide, etc.) — em `3.MJRP-Templates/`

---

## 1. Claude Code + Claude Cowork

Claude Code e Cowork compartilham a mesma estrutura de configuração. A diferença é que Claude Code roda no terminal e Cowork roda no desktop app com acesso a browser e Google Drive.

### 1.1 Onde colocar os arquivos

```
/meu-projeto
├── .claude/
│   └── commands/          ← SLASH COMMANDS (workflows como /speckit.specify)
├── .claudeprompt          ← SYSTEM PROMPT (instruções persistentes)
├── CLAUDE.md              ← CONTEXT FILE (Claude lê automaticamente)
├── skills/                ← SKILLS (Cowork Skills format)
│   └── minha-skill/
│       └── minha-skill/
│           ├── SKILL.md
│           ├── references/
│           └── scripts/
└── docs/specs/            ← SPECKIT (o agente lê via .claudeprompt)
```

### 1.2 Carregar Workflows como Slash Commands

Os workflows viram **slash commands** no Claude Code. Cada `.md` dentro de `.claude/commands/` se torna um comando invocável com `/nome`.

**Para instalar nossos workflows:**

```bash
# Criar a pasta de commands no projeto
mkdir -p .claude/commands

# Copiar workflows adaptados para commands (14 workflows)
# SDD (4)
cp 2.MJRP-AgentsWorkflows/sdd_protocol.md              .claude/commands/sdd.md
cp 2.MJRP-AgentsWorkflows/sdd_specify_protocol.md       .claude/commands/sdd.specify.md
cp 2.MJRP-AgentsWorkflows/sdd_plan_protocol.md          .claude/commands/sdd.plan.md
cp 2.MJRP-AgentsWorkflows/sdd_task_protocol.md          .claude/commands/sdd.task.md
# Context (2)
cp 2.MJRP-AgentsWorkflows/onboarding_protocol.md        .claude/commands/onboard.md
cp 2.MJRP-AgentsWorkflows/developer_protocol.md         .claude/commands/developer.md
# Quality (4)
cp 2.MJRP-AgentsWorkflows/debug_protocol.md             .claude/commands/debug.md
cp 2.MJRP-AgentsWorkflows/regression_protocol.md        .claude/commands/regression.md
cp 2.MJRP-AgentsWorkflows/documentation_protocol.md     .claude/commands/docs.checklist.md
cp 2.MJRP-AgentsWorkflows/check_documentation_protocol.md .claude/commands/docs.check.md
# Audit & Governance (4)
cp 2.MJRP-AgentsWorkflows/architecture_decision_protocol.md    .claude/commands/adr.md
cp 2.MJRP-AgentsWorkflows/documentation_audit_protocol.md      .claude/commands/docs.audit.md
cp 2.MJRP-AgentsWorkflows/test_suite_audit_protocol.md         .claude/commands/test.audit.md
cp 2.MJRP-AgentsWorkflows/code_quality_assessment_protocol.md  .claude/commands/quality.md
```

**Formato do command file:**

```markdown
---
description: Breve descrição do que o command faz
---

[Conteúdo do workflow aqui — o Claude executa como instruções]
```

**Uso no Claude Code:**
```
> /sdd.specify Quero adicionar uma página de bookshelf com filtros
> /onboard
> /debug O botão de filtro não funciona
```

### 1.3 Carregar Skills no Claude Code

Para Claude Code (terminal), skills são carregadas como **contexto** — o agente lê os .md quando precisa. Há duas formas:

**Opção A — Via .claudeprompt (recomendado):**

Adicione referências às skills no `.claudeprompt` do projeto:

```
Você é um desenvolvedor trabalhando no projeto [Nome].

Antes de qualquer implementação, leia:
- VISION.md (propósito)
- CHARTER.md (escopo)
- docs/specs/constitution.md (regras técnicas)

Skills disponíveis (leia quando relevante):
- skills/sdd-speckit/SKILL.md — Como escrever specs de alta qualidade
- skills/context-handoff/SKILL.md — Como preservar contexto entre sessões
- skills/design-system/SKILL.md — Como manter o design system
- skills/conventional-commits/SKILL.md — Padrões de commit e branching

Regras:
- Siga Conventional Commits
- Nunca implemente sem task em tasks.md
- Consulte constitution.md antes de sugerir dependências
```

**Opção B — Via CLAUDE.md (carregado automaticamente):**

Crie um `CLAUDE.md` na raiz do projeto. O Claude Code lê este arquivo automaticamente no início de cada sessão:

```markdown
# Project: [Nome]

## Skills
Quando trabalhar com specs, leia: skills/sdd-speckit/SKILL.md
Quando precisar de handoff, leia: skills/context-handoff/SKILL.md
[etc.]

## Workflows
Para desenvolvimento: execute /sdd.specify, /sdd.plan, /sdd.task
Para debug: execute /debug
Para documentação: execute /docs.checklist
```

### 1.4 Carregar Skills no Cowork

No Cowork (desktop app), skills usam o formato **SKILL.md** dentro do diretório de skills:

```bash
# Estrutura para Cowork Skills
# Temáticas (7)
cp 1.MJRP-AgentsSkills/skill_sdd_speckit.md           skills/sdd-speckit/sdd-speckit/SKILL.md
cp 1.MJRP-AgentsSkills/skill_context_handoff.md        skills/context-handoff/context-handoff/SKILL.md
cp 1.MJRP-AgentsSkills/skill_project_bootstrap.md      skills/project-bootstrap/project-bootstrap/SKILL.md
cp 1.MJRP-AgentsSkills/skill_multi_ai_orchestration.md skills/multi-ai/multi-ai/SKILL.md
cp 1.MJRP-AgentsSkills/skill_design_system.md          skills/design-system/design-system/SKILL.md
cp 1.MJRP-AgentsSkills/skill_conventional_commits.md   skills/conventional-commits/conventional-commits/SKILL.md
cp 1.MJRP-AgentsSkills/skill_code_quality.md           skills/code-quality/code-quality/SKILL.md

# Role-based (5)
cp 1.MJRP-AgentsSkills/skill_ux_ui_designer.md         skills/ux-ui-designer/ux-ui-designer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_frontend_developer.md     skills/frontend-developer/frontend-developer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_backend_developer.md      skills/backend-developer/backend-developer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_mobile_developer.md       skills/mobile-developer/mobile-developer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_qa_engineer.md            skills/qa-engineer/qa-engineer/SKILL.md
```

O Cowork detecta automaticamente skills no diretório `skills/` do projeto montado.

### 1.5 Copiar Templates para o Projeto

Os templates fornecem modelos prontos para documentação recorrente (onboarding, ADRs, tech debt, etc.):

```bash
# Copiar templates para o projeto (adaptar paths ao projeto)
cp 3.MJRP-Templates/onboarding_developer.md   docs/onboarding/DEVELOPER.md
cp 3.MJRP-Templates/onboarding_qa.md          docs/onboarding/QA_ENGINEER.md
cp 3.MJRP-Templates/onboarding_ux_ui.md       docs/onboarding/UX_UI.md
cp 3.MJRP-Templates/onboarding_devops.md      docs/onboarding/DEVOPS.md
cp 3.MJRP-Templates/reference_guide_index.md  docs/manual/00_INDEX.md
cp 3.MJRP-Templates/adr_template.md           docs/architecture/ADR_TEMPLATE.md
cp 3.MJRP-Templates/technical_debt.md         docs/TECHNICAL_DEBT.md
cp 3.MJRP-Templates/implementation_walkthrough.md  docs/manual/WALKTHROUGH_TEMPLATE.md
cp 3.MJRP-Templates/roadmap.md                docs/ROADMAP.md
cp 3.MJRP-Templates/agent_rules_template.md   .agent/rules/RULES_GUIDE.md
```

> **Nota**: Após copiar, preencha os templates com os dados específicos do projeto. Eles contêm placeholders `[...]` para facilitar o preenchimento.

### 1.6 Resumo Claude Code + Cowork

| Artefato | Onde colocar | Como o agente acessa |
|----------|-------------|---------------------|
| Workflows | `.claude/commands/*.md` | Via `/slash-command` |
| Skills | `skills/<nome>/<nome>/SKILL.md` (Cowork) | Cowork detecta automaticamente |
| Skills | Referenciadas em `.claudeprompt` (Code) | Agente lê quando instruído |
| Templates | `docs/` (várias subpastas) | Referenciados por skills e workflows |
| System prompt | `.claudeprompt` na raiz | Carregado a cada sessão |
| Context file | `CLAUDE.md` na raiz | Carregado automaticamente |
| SpecKit | `docs/specs/*.md` | Referenciado via .claudeprompt |

---

## 2. Google Antigravity (Jules)

O Antigravity lê contexto do repositório GitHub e usa configuração na pasta `.agent/`. Suporta nativamente **workflows**, **skills** e **rules**.

### 2.1 Onde colocar os arquivos

```
/meu-projeto
├── .agent/
│   ├── workflows/              ← WORKFLOWS (Antigravity lê estes)
│   ├── skills/                 ← SKILLS (formato nativo do Antigravity)
│   │   ├── sdd-speckit/
│   │   │   └── SKILL.md        ← Cada skill tem seu folder + SKILL.md
│   │   ├── context-handoff/
│   │   │   └── SKILL.md
│   │   └── ...
│   └── rules/                  ← RULES (regras de comportamento)
├── GEMINI.md                   ← SYSTEM INSTRUCTIONS (raiz)
└── docs/specs/                 ← SPECKIT (o agente lê via instructions)
```

### 2.2 Carregar Workflows no Antigravity

O Antigravity reconhece workflows na pasta `.agent/workflows/`. Basta copiar:

```bash
# Criar a pasta de workflows no projeto
mkdir -p .agent/workflows

# Copiar workflows diretamente
cp 2.MJRP-AgentsWorkflows/*.md .agent/workflows/
```

**Para invocar no Antigravity:**

Basta pedir ao agente para executar um workflow pelo nome:
```
"Execute o sdd_specify_protocol para a feature de bookshelf"
"Siga o debug_protocol para investigar o bug no filtro"
"Rode o onboarding_protocol para carregar contexto"
```

Ou referenciar diretamente:
```
"Leia .agent/workflows/sdd_protocol.md e siga o fluxo completo"
```

### 2.3 Carregar Skills no Antigravity

O Antigravity possui um **formato nativo de skills**. Skills são detectadas automaticamente e ativadas quando relevantes ao contexto da conversa.

**Formato obrigatório:**

Cada skill fica em `.agent/skills/<skill-folder>/SKILL.md` com **frontmatter YAML**:

```markdown
---
name: Nome da Skill
description: >
  Descrição concisa do que a skill ensina ao agente.
  O Antigravity usa esta descrição para decidir quando ativar a skill.
---

# Conteúdo da Skill
[Instruções detalhadas aqui]
```

**Campos do frontmatter:**
- `name` (opcional): Nome de exibição da skill
- `description` (obrigatório): Explica o propósito da skill. O Antigravity usa este campo para decidir quando a skill é relevante — escreva de forma clara e descritiva.

**Subpastas opcionais:**
- `scripts/` — Scripts auxiliares que a skill pode invocar
- `examples/` — Exemplos de uso e output esperado
- `resources/` — Arquivos de referência (templates, schemas, etc.)

**Para instalar nossas skills:**

```bash
# Criar a estrutura de skills no formato Antigravity (12 skills)
for skill in sdd-speckit context-handoff project-bootstrap multi-ai-orchestration \
  design-system conventional-commits code-quality ux-ui-designer frontend-developer \
  backend-developer mobile-developer qa-engineer; do
  mkdir -p .agent/skills/$skill
done

# Temáticas (7)
cp 1.MJRP-AgentsSkills/skill_sdd_speckit.md           .agent/skills/sdd-speckit/SKILL.md
cp 1.MJRP-AgentsSkills/skill_context_handoff.md        .agent/skills/context-handoff/SKILL.md
cp 1.MJRP-AgentsSkills/skill_project_bootstrap.md      .agent/skills/project-bootstrap/SKILL.md
cp 1.MJRP-AgentsSkills/skill_multi_ai_orchestration.md .agent/skills/multi-ai-orchestration/SKILL.md
cp 1.MJRP-AgentsSkills/skill_design_system.md          .agent/skills/design-system/SKILL.md
cp 1.MJRP-AgentsSkills/skill_conventional_commits.md   .agent/skills/conventional-commits/SKILL.md
cp 1.MJRP-AgentsSkills/skill_code_quality.md           .agent/skills/code-quality/SKILL.md

# Role-based (5)
cp 1.MJRP-AgentsSkills/skill_ux_ui_designer.md         .agent/skills/ux-ui-designer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_frontend_developer.md     .agent/skills/frontend-developer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_backend_developer.md      .agent/skills/backend-developer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_mobile_developer.md       .agent/skills/mobile-developer/SKILL.md
cp 1.MJRP-AgentsSkills/skill_qa_engineer.md            .agent/skills/qa-engineer/SKILL.md
```

**Como funciona a ativação:**

O Antigravity segue um ciclo de Progressive Disclosure:
1. **Discovery** — Ao iniciar a sessão, o agente lê o `description` de todas as skills disponíveis
2. **Activation** — Quando o contexto da conversa é relevante, o agente carrega o SKILL.md completo
3. **Execution** — O agente segue as instruções da skill durante a tarefa

Isso significa que, ao contrário do Cowork, você **não precisa pedir ao agente para ler uma skill** — ele identifica e ativa automaticamente a skill correta com base na conversa.

**Skills globais (para todos os projetos):**

Se quiser que uma skill esteja disponível em todos os seus projetos:
```bash
# Skills globais ficam em ~/.gemini/antigravity/skills/
mkdir -p ~/.gemini/antigravity/skills/conventional-commits
cp 1.MJRP-AgentsSkills/skill_conventional_commits.md \
   ~/.gemini/antigravity/skills/conventional-commits/SKILL.md
```

### 2.4 Configurar GEMINI.md (System Instructions)

Crie um `GEMINI.md` na raiz do projeto para instruções persistentes:

```markdown
# Instruções do Projeto [Nome]

## Contexto Obrigatório
Antes de qualquer trabalho, leia:
- VISION.md
- CHARTER.md
- docs/specs/constitution.md

## Workflows Disponíveis
Quando executar tarefas, siga os workflows em .agent/workflows/:
- sdd_protocol.md — Fluxo SDD completo (Specify → Plan → Tasks → Implement)
- debug_protocol.md — Protocolo de debug
- onboarding_protocol.md — Carregamento de contexto

## Regras
- Siga Conventional Commits (feat, fix, docs, refactor, vibe, chore)
- Nunca implemente sem task em docs/specs/tasks.md
- Consulte constitution.md antes de sugerir dependências
- Atualize SESSION_HISTORY.md ao final de cada sessão
```

> **Nota**: Diferente do Claude Code, o GEMINI.md não precisa listar as skills explicitamente — o Antigravity as descobre automaticamente via `.agent/skills/`.

### 2.5 Regras no Antigravity

Regras de comportamento vão em `.agent/rules/`:

```bash
mkdir -p .agent/rules

# Exemplo: regras de desenvolvimento
cat > .agent/rules/developer_rules.md << 'EOF'
---
description: Regras obrigatórias de desenvolvimento
---

1. Sempre leia constitution.md antes de sugerir dependências.
2. Siga Conventional Commits para todos os commits.
3. Nunca implemente sem task aprovada em tasks.md.
4. Atualize docs quando alterar código.
5. Rode testes após cada implementação.
EOF
```

### 2.6 Resumo Antigravity

| Artefato | Onde colocar | Como o agente acessa |
|----------|-------------|---------------------|
| Workflows | `.agent/workflows/*.md` | Via instrução ou nome |
| Skills | `.agent/skills/<nome>/SKILL.md` | Auto-descoberta via Progressive Disclosure |
| Skills (global) | `~/.gemini/antigravity/skills/<nome>/SKILL.md` | Disponível em todos os projetos |
| Rules | `.agent/rules/*.md` | Carregado automaticamente |
| System instructions | `GEMINI.md` na raiz | Carregado a cada sessão |
| SpecKit | `docs/specs/*.md` | Referenciado via GEMINI.md |

---

## 3. Checklist de Setup Rápido

### Para um projeto NOVO (Greenfield):

```bash
# 1. Estrutura base
mkdir -p docs/specs docs/sessions docs/architecture docs/onboarding docs/manual

# 2. Copiar templates do framework
cp [framework]/3.MJRP-Templates/onboarding_*.md       docs/onboarding/
cp [framework]/3.MJRP-Templates/reference_guide_index.md docs/manual/00_INDEX.md
cp [framework]/3.MJRP-Templates/adr_template.md        docs/architecture/ADR_TEMPLATE.md
cp [framework]/3.MJRP-Templates/technical_debt.md       docs/TECHNICAL_DEBT.md
cp [framework]/3.MJRP-Templates/roadmap.md              docs/ROADMAP.md
cp [framework]/3.MJRP-Templates/implementation_walkthrough.md docs/manual/WALKTHROUGH_TEMPLATE.md

# 3. Claude Code setup
mkdir -p .claude/commands
cp [framework]/2.MJRP-AgentsWorkflows/*.md .claude/commands/
# Criar .claudeprompt (ver template na seção 1.2)

# 4. Cowork setup (se usar)
mkdir -p skills/
# Copiar skills no formato SKILL.md (ver seção 1.4)

# 5. Antigravity setup (se usar)
mkdir -p .agent/workflows .agent/rules
cp [framework]/2.MJRP-AgentsWorkflows/*.md .agent/workflows/
cp [framework]/3.MJRP-Templates/agent_rules_template.md .agent/rules/RULES_GUIDE.md
# Skills: cada skill em sua pasta com SKILL.md (ver seção 2.3)
for skill in sdd-speckit context-handoff project-bootstrap multi-ai-orchestration \
  design-system conventional-commits code-quality ux-ui-designer frontend-developer \
  backend-developer mobile-developer qa-engineer; do
  mkdir -p .agent/skills/$skill
  cp [framework]/1.MJRP-AgentsSkills/$skill/SKILL.md .agent/skills/$skill/SKILL.md
done
# Criar GEMINI.md (ver template na seção 2.4)

# 6. Commit
git add docs/ .claude/ .agent/ .claudeprompt GEMINI.md skills/
git commit -m "chore: AI agent configuration (workflows, skills, templates, prompts)"
```

### Para um projeto EXISTENTE (Brownfield):

Mesmo processo, mas:
1. Verifique se `.claude/commands/` ou `.agent/workflows/` já existem
2. Faça merge dos novos com os existentes (não sobrescreva)
3. Adapte os paths nos workflows para a estrutura real do projeto
4. Templates: copie apenas os que não existem; não sobrescreva docs existentes
5. Commit: `chore: bootstrap AI agent configuration`
