---
title: Kernel do MJRP Harness
summary: as 11 páginas do harness que este projeto carrega — o que os campos do VISION, a memória, o perfil e os sensores significam
---

## Definition

Cópia carimbada (versão **2026-09-16**, fonte `f7183b0`) das páginas do MJRP Harness que governam como uma instância funciona. **Não se edita aqui**: edite no harness e rode `new_project.py --refresh-kernel`. O doctor (I5) avisa quando o carimbo envelhece.

| Página | O que responde |
|---|---|
| [base-concept](base-concept.md) | a cadeia propósito → visão → objetivo → roadmap — o que cada elo responde, com que horizonte, e por que a ordem entre eles não é estilo |
| [vision-document](vision-document.md) | o que entra num documento de visão, o que não entra, e o teste que separa os dois |
| [memory-architecture](memory-architecture.md) | onde cada coisa que persiste mora e quando entra na janela — a arquitetura da ADR-0008, o que as referências fazem, e de onde veio a escolha |
| [context-vs-memory](context-vs-memory.md) | a fronteira entre os tokens que estão na janela agora e o que persiste fora dela — e por que a memória existe para não perder e retomar o contexto |
| [project-profiles](project-profiles.md) | os três perfis que o harness atende — e a distinção que o README apagava, entre PERFIL (o que o projeto entrega) e CAMINHO DE ADOÇÃO (por que porta ele entra) |
| [terms](terms.md) | o glossário do MJRP — todo o vocabulário, agrupado por função no harness e alfabético dentro de cada grupo |
| [doctor](doctor.md) | o que o doctor mede, o que ele deliberadamente não mede, e por que uma checagem só nasce depois de um incidente |
| [adr-practice](adr-practice.md) | quando uma decisão vira ADR, o que a ADR pode e não pode mudar depois, e o gate Proposed → Accepted |
| [harness-concept](harness-concept.md) | o que o campo chama de harness — cinco fontes, onde elas convergem, onde discordam, e a posição que o MJRP adota |
| [harness-elements](harness-elements.md) | os harness elements — as onze peças de um sistema agêntico, o domínio de cada uma, e onde o MJRP está |
| [engineering-canon](engineering-canon.md) | os três livros que fundamentam a Parte I do PRINCIPLES — destilados, com o que é universal separado do que é opinião de stack |
