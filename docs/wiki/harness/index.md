---
title: Kernel do MJRP Harness
summary: as 24 páginas do harness que este projeto carrega — o que os campos do VISION, a memória, o perfil e os sensores significam
---

## Definition

Cópia carimbada (versão **2026-10-07**, fonte `3d3763e`) das páginas do MJRP Harness que governam como uma instância funciona. **Não se edita aqui**: edite no harness e rode `new_project.py --refresh-kernel`. O doctor (I5) avisa quando o carimbo envelhece.

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
| [engineering-canon](engineering-canon.md) | os quatro livros que fundamentam a Parte I do PRINCIPLES — destilados, com o que é universal separado do que é opinião de stack |
| [spec-kit](spec-kit.md) | as três camadas com o mesmo nome (Spec Kit do GitHub, SpecKit do MJRP, uso real por projeto), a lista única de 9 artefatos e onde cada um mora no grafo de requisitos, o que foi fundido de propósito, e as duas extensões do MJRP — PRD com o mapa dos requisitos (do BMAD) e uat.md |
| [agents-agentic-concepts](agents-agentic-concepts.md) | o que o campo chama de agente, os padrões agênticos, os cinco tipos de sistema, a taxonomia skills/MCP/RAG/memória — e onde as fontes discordam |
| [graph-engineering-concept](graph-engineering-concept.md) | o fluxo do agente como grafo — os três padrões, a comparação loop × graph × swarm, e a pergunta única que escolhe entre eles |
| [hooks-concept](hooks-concept.md) | hook como evento + script — a camada de determinismo dentro de um sistema probabilístico, e a regra que decide o que vai para hook e o que fica no prompt |
| [loop-engineering-concept](loop-engineering-concept.md) | o loop como o que roda sem você — os 4 níveis, a matemática dos erros compostos, loop fixo × criador, e por que o gargalo é o verificador, não o modelo |
| [harness-kaizen](harness-kaizen.md) | onde o harness falhou e o que se aprendeu com isso — o erro e a correção no mesmo lugar |
| [design-canon](design-canon.md) | as fontes elevadas que fundamentam UX, UI e conteúdo explicativo no MJRP — organizadas em oito disciplinas com regras de ID estável que as skills citam em vez de recitar |
| [requirements-graph](requirements-graph.md) | como requisitos e artefatos do PDLC viram nós com ID estável e arestas tipadas, legíveis no Obsidian e por script; a cardinalidade feature × requisito; como a release agrupa requisitos e épicos |
| [knowledge-graph-concept](knowledge-graph-concept.md) | o que é um knowledge graph, o que é ontologia e como ela difere de taxonomia e vocabulário controlado; tripla, RDF × grafo de propriedades, schema × instância, e validação por formas |
| [linked-notes-concept](linked-notes-concept.md) | o modelo de notas atômicas e densamente ligadas que o Obsidian popularizou — de onde vem, os nomes que ele tem, os mecanismos (wikilink, backlink, embed, block ID, MOC) e como o harness o usa como a leitura humana do grafo |
| [git-governance](git-governance.md) | como se commita, ramifica e marca versão num projeto do harness — tipos e formato do commit, os commits de cada estágio do SDD, branches, tags, regras de brownfield, e o que os hooks exigem |
| [spreadsheet-standard](spreadsheet-standard.md) |  |
| [product-discovery](product-discovery.md) | o processo da FASE 1b do MJRP — Rapid (cinco passos essenciais, iterativo com o LLM) e Full (o Rapid mais técnicas que o PM marca no início), os quatro riscos transformados em teste, a decisão matar · iterar · avançar e onde cada saída mora no grafo do projeto |
