---
title: Governança de git
aliases: [git-governance, governança de git, conventional commits, convenção de commit, branching, tags]
summary: como se commita, ramifica, integra e marca versão num projeto do harness — tipos e formato do commit, os commits de cada estação do Delivery, branch e PR por feature, o merge do agente e suas condições, tags, brownfield, e o que os hooks exigem
tags: [kernel, git, processo]
status: firme
atualizado: 2026-10-09
fontes: [conventionalcommits.org, mjrp-deployer (aposentada, S-76), 1999-fowler-refactoring]
---
<!-- kernel do MJRP Harness · versão 2026-10-09 · fonte c470187 · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
**Governança de git** é o conjunto de regras que faz o histórico de um projeto ser legível por quem vem depois —
humano ou agente: cada commit diz o tipo da mudança e o porquê, os estágios do SDD deixam marca no histórico, e
o que é estável fica separado do que está em curso. Vale para todo projeto do harness; as skills que commitam
(`mjrp-implementing-tasks`, `mjrp-debugging`, `mjrp-specifying-sdd-artifacts`) seguem esta página. No loop Delivery
([[pdlc-loops]] §5), cada feature vive numa branch e volta a `main` por PR, com o merge feito pelo agente quando o
verificador passa.

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

### Commits das estações do Delivery
| Estação concluída | Commit |
|---|---|
| Specify | `docs: complete specify stage for <feature>` |
| Plan | `docs: complete plan stage for <feature>` |
| Tasks | `docs: generate tasks for <feature>` |
| Implement | `feat: implement <descrição>` (cita a task) |
| Escalada ao contrato (a spec estava errada) | `docs: revise <stage> for <feature> — requirement change` |
| Cascata de documentação | `docs: complete cascade for <milestone>` |
| Rodada de UAT | `docs: uat round <n> for <feature>` |

### Branches e PR
- **`main`**: estável, implantável. **Não há `dev`:** a feature sai de `main` e volta a `main` por PR.
- **Uma branch por feature ou fix**, curta: `feat/<nome>-<AAAAMMDD>`, `fix/<nome>-<AAAAMMDD>` — ex.:
  `feat/bookshelf-filters-20260217`, `fix/cover-loading-20260217`.
- **O PR leva a evidência:** os requisitos cobertos (REQ-IDs), o verificador verde (testes, sensores, grafo sem
  contradição) e o link da spec. O CI roda o mesmo verificador; o agente não altera o verificador no PR que ele verifica.

### O merge
- **É do agente**, quando o verificador passa (exit 0) — nunca pelo auto-relato. Merge com commit de merge
  (`--no-ff`): os commits de cada estação ficam no histórico, e reverter a feature é reverter um commit.
- **O que o merge quebrar, o agente corrige** — um `fix:` novo, ou `git revert` do merge enquanto corrige.
- **O humano decide, não executa**, só quando pede ou quando há risco de impacto financeiro ou de negócio (apagar ou
  quebrar algo e perder o cliente). Todo merge aparece no Control Center.
- **Pré-condições do merge autônomo:** tudo versionado, rollback possível (o revert do merge) e backup recorrente do
  repositório. **O backup** é um `git bundle --all` a cada commit, no iCloud Drive (`mjrp-backups/<repo>/`): 5 slots de
  commit e 14 de dia, sobrescritos e nunca apagados; restaura com `git clone <arquivo>.bundle`. Quem grava é o hook
  `post-commit` (`mjrp-scripts/backup_repo.py`); o doctor avisa quando o último backup está atrás do HEAD. Numa sessão
  do agente, a pasta do iCloud Drive precisa estar conectada — sem ela o backup é pulado e o próximo commit no Mac o
  recupera (o bundle leva o repositório inteiro). **O push é do humano** (`git push origin main`): não há PR remoto —
  o agente trabalha na branch, roda o verificador e faz o merge local em `main`.
- **Isolamento:** a trava de sessão basta com um agente por vez; com agentes em paralelo, um worktree por feature.

### Tags
- Adoção do harness: `v0-harness-adoption` (brownfield) · marcos: `v1.0`, `v1.1` · sprints: `sprint-01-complete`.
- O próprio harness: `harness-before-loop` marca o estado antes do PDLC em loops; `v0.0`, o resultado da migração — toda
  mudança de núcleo ou de PDLC parte dela.
- `git tag -a v1.0 -m "First stable release"`.

### Brownfield
1. Nunca reescrever (rebase/squash) o histórico existente.
2. As convenções valem do commit de adoção em diante.
3. Marcar a adoção com a tag.
4. Branches existentes ficam até o merge natural; um `dev` existente fecha no próximo merge em `main` e não recebe
   feature nova.

### O que os hooks exigem
- **`commit-msg`:** todo commit traz uma entrada nova no `docs/log.md` (o registro da sessão); e todo commit que traz
  versão nova ou mudada em `design/inception/<name>-vN.html` traz o `info-arch.md` e os wireframes de todas as telas da
  versão. Ir por cima (`--no-verify`, ou o trailer `Prototype-sync: skip — <motivo>`) é decisão do humano, nunca do
  agente.
- **`pre-commit`:** a estrutura por natureza (inclusive `design/wireframes/` e `design/diagrams/<tema>/ep-NN/`) e as
  contradições do grafo de requisitos nos nós tocados.
- **`post-commit`:** o backup (`backup_repo.py`), sem bloquear.
- **Duas sessões no mesmo repositório:** commit só por *pathspec* — nunca `git add -A` com outra sessão ativa.

## History
- **2026-10-09 20:55** · Revisão geral de 2026-10-09: *O que os hooks exigem* ganhou o guarda do protótipo no `commit-msg` (info-arch e wireframes de todas as telas da versão; o trailer de saída é do humano), as pastas novas da estrutura no `pre-commit` e o `post-commit` do backup.
- **2026-10-04 17:32** · Nasce da aposentadoria da `mjrp-deployer` (S-76, decisão do MJRP): a governança de git era
  a parte da skill que as outras citavam (`mjrp-dev`, `mjrp-debug`, `mjrp-pdlc`); como regra de todo projeto, mora no
  kernel e chega aos filhos no refresh. A tag de adoção passa a ser `v0-harness-adoption` (a do bootstrap
  brownfield); a antiga `v0-framework-bootstrap` fica no arquivo.
- **2026-10-07 19:55** · PDLC em loops (onda B.4 de `design/proposals/pdlc-loops-migration-plan.md`; decisões do MJRP de 07/10):
  sai o `dev` — branch por feature com PR direto em `main`; o PR leva a evidência e o CI roda o mesmo verificador; o
  merge é do agente quando o verificador passa, o humano decide só quando pede ou há risco financeiro ou de negócio;
  pré-condições: versionado, rollback, backup recorrente — até lá, merge local e push do humano. Tags do harness
  `harness-before-loop` e `v0.0`.

- **2026-10-08 17:43** · Backup recorrente do repositório (onda F de `design/proposals/pdlc-loops-migration-plan.md`; decisões do
  MJRP de 08/10): iCloud Drive, a cada commit, antes da tag `v0.0`; o push sem credencial sai do caminho — o push é dele.

## Related
[[pdlc-loops]] · [[spec-kit]] · [[requirements-graph]] · [[hooks-concept]] · [[engineering-canon]]
