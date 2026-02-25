---
name: save-session
description: >
  Salva o contexto da conversa atual como um arquivo markdown persistente em
  /Users/mpedroso/0.MyPetProjects/claude_cowork_sessions/. Use sempre que o
  usuário dizer "salva essa sessão", "salva o contexto", "context dump",
  "guarda essa conversa", ou qualquer variação. Também usar ao final de sessões
  longas de trabalho como handoff. O arquivo gerado permite retomar o trabalho
  exatamente de onde parou, mesmo após perda de contexto.
---

# Skill: Save Session

Salva o contexto da conversa atual como arquivo markdown em `/Users/mpedroso/0.MyPetProjects/claude_cowork_sessions/`.

## Por que isso importa

O Cowork não persiste histórico de conversas entre sessões. Este skill resolve isso — cria um arquivo legível tanto por humanos quanto por Claude para retomar o trabalho exatamente de onde parou.

## Como executar

### 1. Detectar o projeto

Identifica o projeto pelo contexto da conversa (nome do repositório, pasta mencionada, ou pergunta direta ao usuário se ambíguo).

### 2. Gerar o nome do arquivo

```
YYYY-MM-DD_<NomeDoProjeto>.md
```

Se já existir um arquivo com essa data e projeto, adicionar sufixo `_b`, `_c`, etc.

Exemplo: `2026-02-19_MJRPpersonal.md`

Caminho completo: `/sessions/zen-nice-carson/mnt/mpedroso/0.MyPetProjects/claude_cowork_sessions/<filename>`

### 3. Escrever o arquivo

Use o template abaixo. Preencha cada seção com o que aconteceu na conversa — seja fiel ao que realmente foi feito, não genérico.

```markdown
# Cowork Session — <Nome do Projeto>

> **Data:** <data completa>
> **Projeto:** <nome> (`<caminho local>`)
> **Participantes:** Zé (maujrp) + Claude (Cowork)

---

## O Que Foi Feito

<Lista numerada das atividades da sessão, do mais importante ao menos importante.
Seja específico: nomes de arquivos, decisões tomadas, problemas resolvidos.>

---

## Estado Atual

<Tabela ou lista mostrando o estado de cada área relevante — milestones, stories,
tasks, features — com status claro (✅ Done, 🔄 In Progress, ⏳ Pending)>

---

## Decisões Chave

<Bullets das decisões arquiteturais ou de processo tomadas nesta sessão.
Essas decisões precisam sobreviver entre sessões.>

---

## Arquivos Modificados

<Lista dos arquivos criados/modificados. Para arquivos importantes, uma linha
explicando o que mudou.>

---

## Próximos Passos

<O que fazer na próxima sessão. Separar por agente se relevante:
- Claude Code / Antigravity (execução)
- Cowork (estratégia)
- Stitch (design)>

---

## Contexto Técnico Rápido

<Stack, paths importantes, variáveis de ambiente, convenções que Claude precisa
conhecer ao retomar. Máximo 10 bullets — só o essencial.>
```

### 4. Confirmar ao usuário

Após salvar, dizer:

> "Sessão salva em `claude_cowork_sessions/YYYY-MM-DD_Projeto.md`. Na próxima sessão, basta me mandar esse arquivo ou citar o caminho e retomo de onde paramos."

## Ao retomar uma sessão

Quando o usuário enviar ou mencionar um arquivo de sessão salvo:

1. Ler o arquivo
2. Confirmar o projeto e o estado atual
3. Resumir em 2-3 linhas o que foi feito e o que está pendente
4. Perguntar: "Por onde quer continuar?"

## Regras

- **Ser específico**: nomes reais de arquivos, decisões reais tomadas — nada genérico
- **Ser conciso**: o arquivo é para leitura rápida, não um romance
- **Decisões > Código**: o que Claude precisa saber entre sessões são as decisões, não o código em si
- **Próximos passos claros**: a seção mais importante para continuidade é "Próximos Passos"
