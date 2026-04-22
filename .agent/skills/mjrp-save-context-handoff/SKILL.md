---
name: mjrp-save-context-handoff
description: >
  Salva e transfere o contexto entre sessões e ferramentas de IA. Use ao FINAL de sessões de
  trabalho ou ao trocar de ferramenta. Triggers: "salva essa sessão", "salva o contexto",
  "context dump", "guarda essa conversa", "handoff", "transferir contexto", "preciso ir para o
  Antigravity", "troca de ferramenta", ou quando SESSION_HISTORY.md precisar de manutenção
  (compressão, retroativos). Para INICIAR uma sessão e recuperar contexto, use
  mjrp-onboarding — não este skill.
---

# Skill: Save Context & Handoff

**Responsabilidade**: Salvar e transferir contexto ao FINAL de sessões e entre ferramentas.
**NÃO é responsabilidade deste skill**: Recuperar contexto no início de sessão — para isso,
use `mjrp-onboarding`.

Resolve o problema fundamental: agentes de IA perdem todo o contexto entre sessões. Sem um
mecanismo de handoff, cada sessão nova começa do zero — desperdiçando tempo relendo arquivos
e arriscando decisões contraditórias.

O único destino de persistência é o **SESSION_HISTORY.md** dentro do repositório do projeto.
Ele é cumulativo, vive no Git, e serve de ponte universal entre todas as ferramentas
(Cowork, Claude Code, Antigravity, Stitch).

**Localização padrão**: `docs/sessions/SESSION_HISTORY.md`

---

## 1. Salvar Sessão (Final de Sessão)

Executar ao final de cada sessão de trabalho, ou quando o usuário pedir explicitamente.

### 1.1 Detectar o Projeto

Identifica o projeto pelo contexto da conversa: nome do repositório, pasta mencionada, branch
ativa. Se ambíguo, perguntar ao usuário.

### 1.2 Atualizar SESSION_HISTORY.md no Repo

Criar `docs/sessions/SESSION_HISTORY.md` se não existir. Este arquivo é cumulativo — cada
sessão adiciona uma entrada no topo, abaixo do cabeçalho.

**Template de entrada**:

```markdown
## Session: [YYYY-MM-DD] — [Título Breve]

> Data: [data e hora completas]
> Participantes: [humano] + [ferramenta de IA]
> Branch: [branch ativa]
> Duração: [aproximada]

### Resumo Executivo
[2-3 frases: o que foi realizado nesta sessão. Deve ser compreensível sem ler o resto.]

### Decisões Tomadas
- [Decisão 1]: [Contexto e justificativa]
- [Decisão 2]: [Contexto e justificativa]

### Artefatos Gerados/Modificados
| Arquivo | Ação | Descrição |
|---------|------|-----------|
| [caminho] | Criado/Modificado | [o que mudou] |

### Pendências para Próxima Sessão
1. [Item de maior prioridade]
2. [Segunda prioridade]
3. [Terceira prioridade]

### Dados-Chave
- [Métrica, contagem ou valor que sessões futuras precisam]
```

### 1.3 Confirmar ao Usuário

Após salvar:

> "Sessão salva em `docs/sessions/SESSION_HISTORY.md`.
>
> Na próxima sessão, use `mjrp-onboarding` e retomo de onde paramos."

---

## 2. Recuperar Contexto (Início de Sessão)

> **Este skill não é responsável por recuperação de contexto.**
> Use `mjrp-onboarding` para iniciar uma sessão — ele cobre recuperação do
> SESSION_HISTORY.md, leitura de VISION/CHARTER/ROADMAP/constitution/specs, e síntese de contexto
> por role. Este skill só deve ser invocado para SALVAR ao final ou BRIDGE entre ferramentas.

---

## 3. Transferência Cross-Tool (Bridge Pattern)

Quando o contexto precisa migrar entre ferramentas de IA diferentes (Cowork → Claude Code,
Cowork → Antigravity, etc.).

### 3.1 O Princípio do Bridge

O repositório Git é a ponte universal. Todas as ferramentas leem e escrevem no mesmo repo.

```
Cowork Session                    Claude Code / Antigravity
     │                                  │
     ├── Atualiza docs/specs/           │
     ├── Atualiza SESSION_HISTORY.md    │
     ├── git commit + push         ───► git pull
     │                                  ├── Lê SESSION_HISTORY.md
     │                                  ├── Lê docs/specs/
     │                                  └── Continua o trabalho
```

### 3.2 Regras para Handoff Cross-Tool

- Sempre commitar e pushar antes de trocar de ferramenta
- A entrada no SESSION_HISTORY.md deve mencionar qual ferramenta é esperada em seguida
- Incluir notas específicas para a ferramenta destino:
  "Antigravity deve focar em implementar tasks 1-3 do tasks.md"
- Nunca presumir que a próxima ferramenta tem histórico de chat — tudo deve estar em arquivos

### 3.3 Notas por Ferramenta

| Ferramenta | Lê de | Escreve em | Notas |
|------------|-------|------------|-------|
| **Cowork** | SESSION_HISTORY.md | SESSION_HISTORY.md | Estratégia e planejamento |
| **Claude Code** | SESSION_HISTORY.md + .claudeprompt | SESSION_HISTORY.md | Execução de código |
| **Antigravity** | SESSION_HISTORY.md + GEMINI.md | SESSION_HISTORY.md | Execução de código |
| **Stitch** | Contexto via humano | N/A | Design — handoff manual |

---

## 4. Contexto Retroativo (Brownfield)

Para sessões que aconteceram ANTES do framework ser adotado — recuperar contexto de
conversas antigas, commits, e docs existentes.

### 4.1 Template para Entradas Retroativas

```markdown
## [RETROATIVO] Sessão Consolidada: [período]

> Fontes: [de onde a info foi extraída]
> Consolidado por: [ferramenta] em [data]

### O que foi feito
[Resumo das atividades durante este período]

### Decisões que impactam o projeto
[Apenas decisões relevantes para trabalho futuro]

### Estado ao final
[Snapshot: o que existia ao final deste período]
```

### 4.2 Fontes de Extração

- `.gemini/antigravity/conversations/` — histórico do Antigravity
- Transcrições de sessões do Cowork
- Mensagens e diffs de commits no Git
- Google Docs, chats do Stitch, ou outras ferramentas de colaboração
- A memória do humano (pergunte!)

---

## 5. Compressão de Contexto

Com o tempo, SESSION_HISTORY.md cresce. Manter útil e enxuto.

### 5.1 Regras de Compressão

- Após 10+ entradas: arquivar entradas antigas em `docs/sessions/archive/session_history_[período].md`
- Manter as últimas 5 entradas no arquivo principal
- Criar uma seção "Timeline do Projeto" no topo com 1 linha por sessão

### 5.2 Exemplo de Timeline

```markdown
# Timeline do Projeto

| Data | Ferramenta | Resumo |
|------|------------|--------|
| 2026-02-15 | Cowork | Spec inicial, análise de dados, migração do vault |
| 2026-02-16 | Cowork | Skill de vault ops, design do framework |
| 2026-02-17 | Claude Code | Implementação v1.1/v1.2, workflows, skills |
| 2026-02-18 | Antigravity | Testes e correções, refactor do módulo auth |
```

---

## Regras Gerais

- **Ser específico**: nomes reais de arquivos, decisões reais — nada genérico
- **Ser conciso**: 150-300 palavras por entrada. Leitura rápida, não romance
- **Decisões > Código**: o que importa entre sessões são as decisões, não o código em si
- **Próximos passos são a seção mais importante**: é o ponto de partida da próxima sessão
- **Caminhos completos sempre**: "Atualizou o spec" → "Atualizou `docs/specs/auth/spec.md`"

### Anti-patterns

- ❌ Muito detalhado: entradas de 500+ palavras que ninguém vai ler por completo
- ❌ Muito vago: "Trabalhamos no projeto" — inútil para recuperação
- ❌ Sem caminhos: "Atualizou o spec" — qual spec? onde?
- ❌ Sem pendências: próxima sessão não tem ponto de partida
- ✅ Goldilocks: 150-300 palavras, específico, acionável
