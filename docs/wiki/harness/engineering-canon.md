---
title: Cânone de engenharia
aliases: [engineering-canon, canone, cânone, clean code, clean architecture, pragmatic programmer]
summary: os três livros que fundamentam a Parte I do PRINCIPLES — destilados, com o que é universal separado do que é opinião de stack
tags: [harness, engenharia, kernel]
status: vivo
atualizado: 2026-09-16
fontes: [pragmatic-programmer, clean-code, clean-architecture]
---
<!-- kernel do MJRP Harness · versão 2026-09-16 · fonte f7183b0 · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
O **cânone** é o corpo de referência que fundamenta os princípios de engenharia do MJRP: *The
Pragmatic Programmer* (Andrew Hunt e David Thomas), *Clean Code* e *Clean Architecture* (Robert
C. Martin). O `PRINCIPLES.md` carrega **a regra e o teste**; esta página carrega **o porquê e o
detalhe**, lida por quem vai desenhar — não por toda sessão. Nem tudo aqui é universal, e o que
não é está marcado: ver § *O que é opinião de stack*.

## What it is

### Componentização

Modularizar não é estética: é o que permite trocar uma parte sem reabrir as outras. O design
pattern escolhido tem que **levar** a isso — se o padrão está no código e as partes continuam
grudadas, o padrão virou decoração.

- **REP — Reuse/Release Equivalence:** a granularidade do reúso é a granularidade do release.
- **CCP — Common Closure:** junte no mesmo componente o que muda pelos mesmos motivos e ao mesmo
  tempo. É o SRP no nível de componente.
- **CRP — Common Reuse:** não obrigue quem usa o componente a depender do que ele não usa.

### SRP e o Stepdown Rule

**Single Responsibility:** um módulo tem **uma razão para mudar** — ou seja, responde a **um
ator**. Não é "faz uma coisa só"; é "muda por causa de uma pessoa só".

**Stepdown Rule:** as instruções de uma função estão todas no mesmo nível de abstração. Misturar
"calcular o imposto" com "abrir o arquivo" na mesma função é o sintoma mais comum de God File em
formação.

### Dependency Rule e DIP

**A regra primária do Clean Architecture:** dependências de código-fonte apontam **estritamente
para dentro**, na direção das políticas de alto nível e da regra de negócio. O círculo interno
não sabe nada do externo — nada de framework, banco ou UI vazando para dentro.

**DIP:** política de alto nível não depende de detalhe; o código depende de **abstração**, não de
implementação concreta.

**Os três princípios de acoplamento entre componentes:**

- **ADP — Acyclic Dependencies:** nenhum ciclo no grafo de dependência entre componentes.
- **SDP — Stable Dependencies:** dependa na direção da estabilidade — o menos estável depende do
  mais estável, nunca o contrário.
- **SAP — Stable Abstractions:** um componente deve ser tão abstrato quanto é estável.

### Camadas concêntricas

| Camada | O que é dela |
|---|---|
| **Entities** | regra de negócio crítica da empresa, e os dados dela |
| **Use Cases** | regra de negócio da aplicação — orquestra as entidades para cumprir um objetivo |
| **Interface Adapters** | converte entre o formato do Use Case e o do agente externo |
| **Frameworks & Drivers** | UI, framework web, banco, dispositivo — o anel externo, isolado do núcleo |

### Padrões, com endereço

O padrão só serve se o próximo agente o reconhecer. Cada um em uso é declarado na
`constitution.md` do projeto com **onde mora** e **para quê** — Repository, Service, Strategy,
Adapter, Facade, Composable. Padrão sem endereço é padrão que será reinventado.

### ETC e DRY

**ETC — Easier to Change:** o critério único de bom design. Diante de duas opções, a melhor é a
que deixa a mudança seguinte mais barata.

**DRY:** *"every piece of knowledge must have a single, unambiguous, authoritative representation
within a system"*. Note que é sobre **conhecimento**, não sobre texto: duas funções parecidas que
representam regras diferentes não são DRY violado.

### Nomes e funções

- **Nome revela intenção**, é buscável e pronunciável. Nada de desinformação nem de encoding
  ultrapassado (notação húngara, `m_`) — *isto é opinião de stack, ver abaixo*.
- **Funções pequenas**, que fazem **uma coisa**, bem, e só ela.
- **Comentário não compensa código ruim.** A intenção mora no próprio código.
- **Lei de Demeter:** fale com amigos, não com estranhos — um módulo não conhece o interior dos
  objetos que manipula.

### Regras de Kent Beck — design simples, em ordem de prioridade

1. **Passa todos os testes** — o sistema é testável.
2. **Sem duplicação.**
3. **Expressa a intenção.**
4. **Minimiza o número de elementos** (classes, métodos) — sem violar as três acima.

A ordem importa: quando duas brigam, a de cima ganha.

### Tratamento de erro

**O que é universal:** falha não é silenciosa. Todo erro é sinalizado por algum mecanismo, e
quem chama consegue distinguir sucesso de falha.

**O que é opinião de stack:** *"use exceções em vez de códigos de retorno"* e *"não retorne
null"*. Valem em Java, C# e TypeScript; **não** valem em Go (que usa valores de erro por design)
nem em Rust (`Result`/`Option`), e em Apps Script `null` é idiomático. O projeto decide na
`constitution.md` dele — o princípio só exige que a falha **apareça**.

### Testes e TDD

**As três leis do TDD:** não escrever código de produção sem um teste falhando; escrever só o
suficiente do teste para falhar; escrever só o código necessário para passar.

**F.I.R.S.T.:** Fast · Independent · Repeatable · Self-Validating · Timely.

### Entropia e a regra do escoteiro

**Software Entropy / No Broken Windows:** código ruim, decisão ruim e design ruim se consertam
**na hora em que são descobertos**. Uma janela quebrada não consertada autoriza a segunda.

**Boy Scout Rule:** deixe o acampamento mais limpo do que o encontrou.

**Boiled Frogs:** mantenha consciência situacional — a mudança que mata é a gradual, a que não
dispara alarme em nenhum dia isolado.

**Stone Soup:** seja catalisador — comece pequeno e mostre, em vez de pedir permissão para o todo.

### The Cat Ate My Source Code

Responsabilidade plena pelas próprias ações, aprendizado e código. Quando o erro acontece, se
assume com honestidade e **no lugar da desculpa vem a opção acionável**. É o princípio mais fácil
de citar e o mais difícil de cumprir na hora.

### Good-Enough Software

Qualidade é **requisito**, e portanto é negociação com quem recebe: escopo, qualidade e prazo se
decidem juntos, e saber parar de refinar é parte do ofício. Não é desculpa para entregar torto —
é a recusa de refinar o que ninguém pediu enquanto o valor não chega.

### Comunicação e conhecimento — o que fica de fora do PRINCIPLES

*Knowledge Portfolio* (conhecimento é ativo que expira; invista, diversifique, questione com os
Cinco Porquês) e *Communicate!* (trate linguagem natural como código: conheça a audiência, escolha
o momento, ouça) são princípios do **profissional**, não do software. Ficam registrados aqui
porque fazem parte do cânone, mas não regulam ação sobre código — e por isso não subiram para o
`PRINCIPLES.md`.

## O que é opinião de stack

> **A regra de leitura:** o `PRINCIPLES.md` vale em Apps Script, Vue e Next.js igualmente. O que
> só vale em algumas linguagens é regra de projeto — mora na `constitution.md` dele, como delta
> ([[base-concept]], `PRINCIPLES.md` Parte III).

| O que o cânone diz | Por que não é universal |
|---|---|
| **Exceções em vez de códigos de retorno** | Go usa valores de erro por design; Rust usa `Result` |
| **Nunca retorne `null`** | em Apps Script é idiomático; em Kotlin e TS o tipo já resolve |
| **LSP e ISP** | pressupõem subtipo e interface — não têm objeto em código funcional (React, Composition API) |
| **Minimize classes e métodos** | escrito para OO; num projeto funcional a unidade não é a classe |
| **Notação húngara, `m_`** | datado, específico de C++/Java antigo |
| **Limite de 300 linhas por arquivo** | número é da `constitution.md` do projeto, não do harness |

## How MJRP uses it

- **Esta página é do kernel** — vai carimbada para dentro de todo projeto em
  `docs/wiki/harness/`, junto com as outras do pacote básico, e o I5 do `doctor` confere que
  chegou e que o carimbo não envelheceu.
- **Lê-se sob demanda, não por sessão.** Quem vai desenhar arquitetura ou revisar um PR abre;
  quem vai corrigir um texto, não. É o `PRINCIPLES.md` que toda sessão carrega.
- **Quando o cânone e o projeto discordarem, o projeto decide** — desde que a decisão esteja
  escrita na `constitution.md` dele, e desde que ela não contrarie um princípio da Parte I.

## History

> A decisão mora na página do assunto que ela muda, com data (ADR-0008).
- **2026-09-16** · **A página nasce do desmembramento do `PRINCIPLES.md`.** O MJRP reescreveu a
  parte de engenharia trazendo os três livros por inteiro — o arquivo foi de 117 para 172 linhas
  e de 6.960 para 12.895 caracteres. O conteúdo era bom; o lugar, não: o `PRINCIPLES.md` é
  herdado por todo projeto e lido em toda sessão. **A decisão dele:** os princípios ficam lá, com
  o teste de cada um, e o cânone vem para cá — *"progressive disclosure aplicado ao próprio
  harness"*. Junto veio a marcação do que é **opinião de stack**, que a versão anterior misturava
  com o universal. Entra no **kernel**, por decisão dele no mesmo turno.

## Related
[[base-concept]] · [[terms]] · [[doctor]] · [[harness-elements]] · [[adr-practice]]
