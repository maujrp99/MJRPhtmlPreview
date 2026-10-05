---
title: Governança de git
aliases: [git-governance, governança de git, conventional commits, convenção de commit, branching, tags]
summary: como se commita, ramifica e marca versão num projeto do harness — tipos e formato do commit, os commits de cada estágio do SDD, branches, tags, regras de brownfield, e o que os hooks exigem
tags: [kernel, git, processo]
status: firme
atualizado: 2026-10-04
fontes: [conventionalcommits.org, mjrp-deployer (aposentada, S-76), 1999-fowler-refactoring]
---
<!-- kernel do MJRP Harness · versão 2026-10-05 · fonte c2453c9 · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
**Governança de git** é o conjunto de regras que faz o histórico de um projeto ser legível por quem vem depois —
humano ou agente: cada commit diz o tipo da mudança e o porquê, os estágios do SDD deixam marca no histórico, e
o que é estável fica separado do que está em curso. Vale para todo projeto do harness; as skills que commitam
(`mjrp-implementing-tasks`, `mjrp-debugging`, `mjrp-specifying-sdd-artifacts`) seguem esta página.

## Details

### Tipos de commit
| Tipo | Quando | Exemplo |
|---|---|---|
| `feat` | funcionalidade nova | `feat: add book card component with cover grid` |
| `fix` | correção de defeito | `fix: resolve filter reset on page navigation` |
| `docs` | documentação e specs | `docs: complete specify stage for bookshelf` |
| `refactor` | muda o código sem mudar o comportamento | `refactor: extract API calls into shared service` |
| `vibe` | ajuste estético de UI/UX | `vibe: adjust card shadows and hover transitions` |
| `chore` | manutenção (dependências, configs, CI) | `chore: update Next.js to 15.2` |
| `test` | testes novos ou atualizados | `test: add unit tests for BookCard component` |

### Formato da mensagem
- `<tipo>: <descrição curta no imperativo>` + corpo opcional (o **porquê**, não o quê) + rodapé opcional (referências,
  breaking changes).
- Imperativo ("add", não "added"/"adds"), minúscula depois do prefixo, sem ponto final, assunto ≤ 72 caracteres.
- O diff mostra **o que** mudou; o corpo explica **por quê**. **Um tipo por commit.**
- **O fix vai separado da limpeza que ele inspirou:** primeiro `fix:`, depois `refactor:` ou `chore:` no seu próprio
  commit. Misturados, reverter a limpeza leva o fix junto, e a revisão não sabe qual linha corrigiu o defeito.

### Commits dos estágios do SDD
| Estágio concluído | Commit |
|---|---|
| Specify | `docs: complete specify stage for <feature>` |
| Plan | `docs: complete plan stage for <feature>` |
| Tasks | `docs: generate tasks for <feature>` |
| Implement | `feat: implement <descrição>` (cita a task) |
| Volta de estágio | `docs: revise <stage> for <feature> — requirement change` |
| Cascata de documentação | `docs: complete cascade for <milestone>` |
| Rodada de UAT | `docs: uat round <n> for <feature>` |

### Branches
- `main`: estável, implantável, protegida · `dev`: integração · `feat/<nome>-<AAAAMMDD>`: curta.
- Nome: `feat/bookshelf-filters-20260217`, `fix/cover-loading-20260217`.
- Fluxo: `main ← dev ← feat/<feature>-AAAAMMDD` (sai de `dev` → commit → merge em `dev` → merge em `main` quando
  estável).

### Tags
- Adoção do harness: `v0-harness-adoption` (brownfield) · marcos: `v1.0`, `v1.1` · sprints: `sprint-01-complete`.
- `git tag -a v1.0 -m "First stable release"`.

### Brownfield
1. Nunca reescrever (rebase/squash) o histórico existente.
2. As convenções valem do commit de adoção em diante.
3. Marcar a adoção com a tag.
4. Branches existentes ficam até o merge natural.

### O que os hooks exigem
- **`commit-msg`:** todo commit traz uma entrada nova no `docs/log.md` (o registro da sessão); ir por cima
  (`--no-verify`) é decisão do humano, nunca do agente.
- **`pre-commit`:** a estrutura por natureza e as contradições do grafo de requisitos nos nós tocados.
- **Duas sessões no mesmo repositório:** commit só por *pathspec* — nunca `git add -A` com outra sessão ativa.

## History
- **2026-10-04 17:32** · Nasce da aposentadoria da `mjrp-deployer` (S-76, decisão do MJRP): a governança de git era
  a parte da skill que as outras citavam (`mjrp-dev`, `mjrp-debug`, `mjrp-pdlc`); como regra de todo projeto, mora no
  kernel e chega aos filhos no refresh. A tag de adoção passa a ser `v0-harness-adoption` (a do bootstrap
  brownfield); a antiga `v0-framework-bootstrap` fica no arquivo.

## Related
[[spec-kit]] · [[requirements-graph]] · [[hooks-concept]] · [[engineering-canon]]
