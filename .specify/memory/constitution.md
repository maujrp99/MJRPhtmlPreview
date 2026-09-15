<!-- GERADO de docs/specs/constitution.md em 2026-09-15 — nao edite aqui.
     Edite a fonte e regenere com mjrp-scripts/gen_speckit_constitution.py.
     PRINCIPLES.md Parte III: uma escrita e uma gerada, nunca duas escritas
     (em 2 de 5 projetos elas ja tinham divergido). -->

# Project Constitution — MJRPhtmlPreview

Este projeto segue o **`PRINCIPLES.md` do MJRP Harness, versão 1.0**. Esta constituição **não
reescreve** nada de lá: declara a herança e acrescenta só o que é da stack deste projeto —
`PRINCIPLES.md` Parte III.

> **O que saiu daqui em 2026-09-15, e para onde foi.** *Technical Stack* e *AI Orchestration*
> viraram campo do contrato (`.mjrp-project.yml` → `stack:`, `models:`) — constituição não
> descreve stack nem quem-faz-o-quê. *Development Methodology (SDD)* e *SCM & Governance* são os
> princípios I e II do harness — herdados, não repetidos; o "nenhum código sem task definida" é o
> II.7. O que ficou é o que **só vale aqui**: a disciplina vanilla, o que a stack proíbe e as
> restrições de credencial e de conta. De 38 linhas para o que segue. Original em
> `_backups/constitution.md.20260915-1159.bak`.

## 1 · O que é proibido nesta stack

- **Nada de dependência externa.** *Vanilla-first* é a regra, não a preferência: biblioteca só
  entra com decisão registrada. O produto é um arquivo que abre sem servidor — dependência
  quebra isso antes de quebrar qualquer outra coisa.
- **Nada de build tool no M1.** O MVP tem que continuar rodando como `file://`. Build entra em M2
  ou M3, se entrar, e a decisão vira ADR.
- **Credencial não mora no repositório.** As chaves de Google API passam por `.env`, nunca
  commitadas. *(A regra do MJRP: segredo em disco versionado está fora.)*
- **Nada de assumir a conta.** O fluxo tem que funcionar com conta Google **pessoal e
  profissional** — código que assume um domínio é bug, não configuração.

## 2 · A forma deste projeto: um arquivo só

O MVP é **uma SPA de arquivo único** — HTML com CSS e JS inline. Isso não é atalho; é a
restrição de produto. Enquanto ela valer:

| O que | Onde mora |
|---|---|
| Marcação, estilo e comportamento | o próprio `.html` |
| Integração com Google (OAuth2, Drive v3, Picker) | uma camada de funções isolada dentro do arquivo, atrás de nomes próprios do projeto — nunca chamada de API espalhada pela UI (`PRINCIPLES.md` II.2) |
| Decisões visuais | [`design-system.md`](design-system.md) |

**O teste de fronteira deste projeto:** se trocar o Drive por outro armazenamento exigir mexer em
mais do que a camada de integração, a fronteira vazou.

## 3 · Design system

Vibe **Minimal Dark**, e dela não se desvia: fundo `#0d1117`, acento ciano `#58a6ff`, acento
verde `#3fb950`; JetBrains Mono para código e textarea, Inter para rótulos de UI. Contraste
**WCAG AA** sobre fundo escuro é requisito, não meta. O detalhe mora em
[`design-system.md`](design-system.md); aqui fica só o que é inegociável.

## 4 · Convenções de branch e commit

`main` estável · `dev` integração. Conventional Commits, com o tipo extra **`vibe`** para mudança
puramente estética.
