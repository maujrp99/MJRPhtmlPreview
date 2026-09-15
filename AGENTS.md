# AGENTS.md - MJRPhtmlPreview

Instruções canônicas deste projeto, para qualquer AI Platform (Claude Code, Gemini, ou outra). `CLAUDE.md`/`GEMINI.md` importam este arquivo - o que é específico de uma ferramenta vive lá, nunca aqui.

## Herança

Este projeto segue o `PRINCIPLES.md` do MJRP Harness, versão 1.0. A `docs/specs/constitution.md` deste projeto acrescenta o que é da stack; não reescreve nada do PRINCIPLES.md.

## Antes de qualquer trabalho

1. Ler `MEMORY.md` -> `## Now` e `## Ways of Working` (o estado e as correções já feitas).
2. Ler `VISION.md` (por que este projeto existe) e `docs/specs/constitution.md` (padrões da stack).
3. Se for trabalho de implementação: existe `spec.md` -> `plan.md` -> `tasks.md` aprovados para a feature? Sem isso, não implementar - ver `story.md` e o ciclo SDD.
4. Rodar `python3 <caminho-do-harness>/mjrp-scripts/doctor.py .` antes de commitar. Vermelho não commita.

## O que este arquivo NÃO faz

Não decide stack, não decide quem-faz-o-quê (isso é do contrato de instância, `.mjrp-project.yml`) e não reescreve o PRINCIPLES.md - só declara que este projeto o segue.
