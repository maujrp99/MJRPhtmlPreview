---
name: mjrp-clde-antigravity-expert
description: >
  Expert on Claude Code/Cowork and Google Antigravity AI platforms — covering skills, workflows,
  MCP connectors, plugins, hooks, CLAUDE.md, GEMINI.md, and new features of both. Use this skill
  whenever the user wants to: keep the mjrpSetup MJRP framework current with the latest platform
  capabilities; install or update skills, workflows, plugins, or MCP connectors in Claude
  Code/Cowork or Antigravity; understand current SKILL.md format, plugin structure, hooks, or
  agent configuration; find and configure MCP servers; audit what's outdated in the MJRP framework;
  or troubleshoot skill/workflow installation issues. ALWAYS invoke when the user mentions
  "antigravity", "cowork features", "claude code capabilities", "mcp connector", "plugin", "hooks",
  "new features", "atualizar framework", "framework desatualizado", "instalar skill", "install
  skill", "update skills", or asks about capabilities of either AI platform. On every invocation,
  fetches the latest documentation to ensure advice is always current.
---

# Clde + Antigravity Expert

This skill maintains the MJRP Vibe Coding Framework aligned with the latest capabilities of both AI platforms. It always fetches current documentation before advising, so recommendations reflect the state of each platform at the time of invocation.

## ⚡ Regra de Ouro (Rule of Thumb)

**Toda vez que esta skill for invocada, execute o protocolo de consulta web antes de qualquer recomendação.** Isso garante que as informações estejam atualizadas com os últimos lançamentos de ambas as plataformas.

---

## Protocolo de Consulta Web (Execute SEMPRE ao iniciar)

Ao ser invocada, busque a documentação mais recente de ambas as plataformas em paralelo:

**Claude Code / Cowork:**
```
WebFetch: https://code.claude.com/docs/llms.txt
Prompt: "List all documentation pages, new features, and recent changes"
```
```
WebFetch: https://code.claude.com/docs/en/changelog.md
Prompt: "Extract the most recent releases, new features, and breaking changes"
```

**Google Antigravity:**
```
WebSearch: "Google Antigravity AI agent skills workflows documentation 2025 2026"
WebFetch: https://antigravity.google/docs/home  (or /docs/ if home fails)
Prompt: "Extract skills format, workflow format, new features, MCP support"
```

Se algum URL falhar, use WebSearch com os termos `site:antigravity.google docs` ou `Google Antigravity agent documentation changelog` para encontrar o caminho correto.

Após a busca, sintetize:
1. Novas features lançadas desde o último update do framework
2. Mudanças de formato (SKILL.md, hooks, plugins, .mcp.json, etc.)
3. Novos MCP connectors disponíveis
4. Novos plugins ou capabilities que o framework ainda não referencia

---

## Modos de Operação

### MODO 1 — AUDIT (Auditar o mjrpSetup)

Quando o usuário pede para verificar se o framework está atualizado:

1. Leia `references/mjrp-audit-checklist.md` para o checklist completo de auditoria
2. Após a consulta web, compare o estado atual do framework com as capacidades mais recentes
3. Produza um relatório com:
   - ✅ O que está alinhado com a versão atual das plataformas
   - ⚠️ O que está desatualizado ou usa formato legado
   - 🆕 O que está faltando (novas features não aproveitadas)
   - 📋 Recomendações priorizadas de atualização

**O que auditar no mjrpSetup:**
- Formato dos SKILL.md (frontmatter fields atuais: `name`, `description`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `context`, `agent`, `hooks`, `model`)
- Estrutura de paths para skills pessoais (`~/.claude/skills/`) vs projeto (`.claude/skills/`)
- SETUP_GUIDE_AI_Tools.md — se os bash scripts de instalação ainda são válidos
- README.md — se a estrutura de folders e contagens estão corretas
- Referências a plugins (`MJRP_ai_workflows/mjrp-workflow-skills/` — são `.skill` files compatíveis?)
- MCP connectors usados nos projetos do usuário — se têm versões mais recentes
- Hooks — se o framework deveria recomendar hooks para automação
- CLAUDE.md / GEMINI.md templates — se precisam de atualizações

### MODO 2 — UPDATE (Atualizar o framework)

Quando o usuário confirma que quer atualizar um item específico:

1. Identifique os arquivos afetados (SKILL.md, SETUP_GUIDE, README, framework docs)
2. Aplique as mudanças necessárias seguindo os formatos atuais das plataformas
3. Se uma skill precisa ser reempacotada, use o script `package_dual.py`:
   ```bash
   cd /path/to/mjrpSetup/MJRP_ai_skills/scripts/
   python package_dual.py ../skill_sources/<skill-name>/
   ```
4. Para instalar no Antigravity global:
   ```bash
   cp -r /path/to/mjrpSetup/MJRP_ai_skills/skill_packages_Antigravity/<skill-name>/ \
         ~/.gemini/antigravity/skills/<skill-name>/
   ```

### MODO 3 — INSTALL (Instalar no projeto do usuário)

Quando o usuário quer instalar skills/workflows em um projeto específico:

Pergunte: **"Em qual ferramenta você quer instalar? (Claude Code / Cowork / Antigravity / Todos)"**

**Para Claude Code (terminal):**
- Skills vão em `~/.claude/skills/<nome>/SKILL.md` (globais) ou `.claude/skills/<nome>/SKILL.md` (projeto)
- Workflows/commands vão em `.claude/commands/<nome>.md`
- Rules vão em `.claude/rules/<nome>.md`
- Refira o usuário à seção 1.2-1.6 do `SETUP_GUIDE_AI_Tools.md`

**Para Cowork (desktop app):**
- Skills são instaladas via `.skill` packages (disponíveis em `skill_packages_Claude/` e `mjrp-workflow-skills/`)
- Ou via source folders copiados para `skills/<nome>/<nome>/SKILL.md` no projeto montado
- Consulte `references/claude-capabilities.md` para detalhes atuais

**Para Antigravity:**
- Skills vão em `.agent/skills/<nome>/SKILL.md` (projeto) ou `~/.gemini/antigravity/skills/<nome>/SKILL.md` (global)
- Workflows vão em `.agent/workflows/<nome>.md`
- Rules vão em `.agent/rules/<nome>.md`
- Consulte `references/antigravity-capabilities.md` para formato atualizado

### MODO 4 — MCP CONNECTORS (Instalar/Atualizar MCPs)

Quando o usuário quer adicionar um MCP connector:

1. Identifique o connector desejado (nome da ferramenta: Notion, Slack, GitHub, etc.)
2. Busque o URL ou comando mais recente:
   ```
   WebFetch: https://code.claude.com/docs/en/mcp.md
   ```
   Ou consulte o registry oficial: `https://api.anthropic.com/mcp-registry/docs`
3. Forneça o comando exato de instalação:
   ```bash
   # HTTP (recomendado)
   claude mcp add --transport http <nome> <url>

   # SSE (legado)
   claude mcp add --transport sse <nome> <url>

   # Stdio local
   claude mcp add --transport stdio --env KEY=VALUE <nome> -- npx -y <package>
   ```
4. Indique o scope: `--scope local` (default), `--scope project` (compartilhado), `--scope user` (cross-projects)
5. Para MCPs em Antigravity, verifique se há suporte nativo ou se precisam do formato `.agent/`

### MODO 5 — PLUGINS (Criar/Instalar Plugins)

Quando o usuário quer criar ou instalar um plugin:

**Estrutura de um plugin Claude Code:**
```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          ← manifest (name, description, version)
├── skills/
│   └── skill-name/
│       └── SKILL.md
├── commands/                 ← slash commands legados
├── agents/                   ← subagents customizados
├── hooks/
│   └── hooks.json
├── .mcp.json                 ← MCP servers bundled
└── settings.json             ← defaults do plugin
```

**Testar localmente:**
```bash
claude --plugin-dir ./my-plugin
```

**Instalar de marketplace:**
```bash
/plugin install <url-or-name>
```

Para criar plugins MJRP, use o skill `cowork-plugin-management:create-cowork-plugin`.

---

## Checklist de Novas Features a Verificar

Ao auditar, verifique especificamente se o framework já adota:

**Claude Code (features recentes):**
- [ ] `context: fork` em skills para rodar em subagent isolado
- [ ] `agent` field para especificar tipo de subagent (`Explore`, `Plan`, `general-purpose`)
- [ ] `hooks` field no frontmatter das skills (hooks scoped à skill)
- [ ] `!`command`` syntax para dynamic context injection nas skills
- [ ] `$ARGUMENTS[N]` / `$N` para argumentos posicionais
- [ ] `${CLAUDE_SKILL_DIR}` e `${CLAUDE_SESSION_ID}` como variáveis de substituição
- [ ] `user-invocable: false` para skills que só o Claude deve ativar
- [ ] `disable-model-invocation: true` para skills só-usuário
- [ ] `allowed-tools` para restringir ferramentas por skill
- [ ] MCP Tool Search automático (novo em versões recentes)
- [ ] Plugins com `.lsp.json` para language server support
- [ ] Subagents com sistema de preload de skills
- [ ] `/batch` e `/simplify` como bundled skills
- [ ] `/loop` para tasks recorrentes (scheduled tasks)

**Google Antigravity (verificar via web):**
- [ ] Suporte a MCP connectors nativos
- [ ] Novo formato de frontmatter nas skills
- [ ] Suporte a plugins
- [ ] Capacidades de subagents
- [ ] Qualquer mudança no formato de `.agent/` config

---

## Formato de Saída Recomendado

### Para relatório de auditoria:

```
## Auditoria do MJRP Framework — [data]
### Plataformas consultadas: Claude Code vX.X.X | Antigravity [versão]

### ✅ Alinhado (X itens)
- [item]: [status ok]

### ⚠️ Desatualizado (X itens)
- [item]: [formato antigo → formato novo]

### 🆕 Features não aproveitadas (X itens)
- [feature]: [o que é e como poderia beneficiar o framework]

### 📋 Recomendações Priorizadas
1. [Alta prioridade] — [ação concreta]
2. [Média prioridade] — [ação concreta]
3. [Baixa prioridade] — [ação concreta]
```

---

## Arquivos de Referência

Para detalhes mais profundos sobre cada plataforma, leia os arquivos de referência quando necessário:

- **`references/claude-capabilities.md`** — Formato atual de skills, plugins, MCP, hooks para Claude Code/Cowork. Leia quando precisar de detalhes técnicos de instalação ou formato.
- **`references/antigravity-capabilities.md`** — Formato atual e capacidades do Google Antigravity. Leia quando precisar configurar skills/workflows para Antigravity.
- **`references/mjrp-audit-checklist.md`** — Checklist completo do que auditar no framework, com paths específicos e o que verificar em cada arquivo.

> **Nota importante**: Os arquivos de referência capturam o estado do conhecimento no momento da criação desta skill. A consulta web no início de cada invocação é o que garante informações realmente atuais. Se houver conflito entre os arquivos de referência e o que a web retornar, a web tem precedência.
