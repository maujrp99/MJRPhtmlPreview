---
title: O doctor
aliases: [doctor, doctor.py, sensores, o que o doctor vê]
summary: o que o doctor mede, o que ele deliberadamente não mede, e por que uma checagem só nasce depois de um incidente
tags: [harness, sensores, verificacao]
status: em formação
atualizado: 2026-09-14
---
<!-- kernel do MJRP Harness · versão 2026-09-16 · fonte 19eaf95 · cópia derivada: não edite aqui — edite no harness e rode `new_project.py --refresh-kernel` -->

## Definition
O **doctor** é o sensor do harness: um script que lê a instância e devolve verde,
amarelo ou vermelho por critério nomeado. Ele não julga o trabalho — julga se a instância
obedece ao que ela mesma declara. Uma checagem só entra depois de um incidente que ela teria
pegado (ADR-0002, emendada pela ADR-0007): checagem sem incidente é opinião com exit code.

## History

> Página criada em 09/09/2026 pelo BACKLOG #28a, por indicação do Zé. As entradas abaixo vieram
> **inteiras** do `MEMORY.md` — nada foi condensado na mudança; a edição, se vier, vem depois e
> com o `memory_check` capaz de vê-la.
- **2026-09-09 18:55** · **O `Stop` hook é o único ponto onde o harness impede.** `stop_gate.py`
  bloqueia o fim do turno quando houve edição em área vigiada sem critério declarado **e
  aprovado**. Turno de conversa nunca bloqueia — gate que trava o que não devia é gate que o
  humano desliga. Critério aprovado **antes** da última edição não vale: está velho.
- **2026-09-08 22:54** · **O doctor deixou de exigir PyYAML.** Lê YAML sozinho quando a biblioteca falta
  (`_yaml_min`), e o selftest compara os dois parsers para o fallback não divergir em silêncio. O
  `environment.setup` do contrato virou `nenhum` — era um comando que o Homebrew recusa. A porta de
  entrada de qualquer instância não pode exigir instalação.
- **2026-09-08 23:24** · **A3 feito (#8): o `doctor` rodou no Mac pela primeira vez** — e o harness saiu **VERMELHO**,
  6 erros, todos I2, todos em skills do **toolkit** (o build-framework está limpo). 4 são
  `MJRPvault/Meeting-Notes/` — **o vault existe, a subpasta não** — e 2 são o Mac anterior
  (`/Users/mpedroso/`). É o incidente que criou a I2, pego enfim. **A fase A fecha com o A4 (hooks).**
- **2026-09-08 23:24** · **Os dois filhos avaliados saem em exit 2: contrato no schema antigo** (`mjrp_project:` com
  name/type/path), que é o que o `README` § 2 ainda ensina. A documentação ensina o formato que o doctor
  não avalia — o achado do inventário, confirmado na prática. É fase B (#14) e passo 2 (#3).
- **2026-09-09 00:39** · **Os 6 do I2 resolvidos.** `eq-advisor` → `MJRPhifi-music/`; `ebook-summarizer` →
  `MJRPvault/Books/` (onde já estão o Learning Dashboard e o kanban — a listagem do vault corrigiu a
  resposta anterior dele); `Meeting-Notes/` + `_logs/` + `HTML_Catalog.md` **criados no vault**, que era
  a escolha dele (criar e manter, não aposentar as skills). Três dos seis eram **molde, não caminho**.
- **2026-09-09 00:44** · **#9c feito: `entry_check.py`** — executa o caminho que o `HOWTO` promete e devolve 0/1/2.
  12 verificações: instalação, doctor sem PyYAML (e **concordando** consigo com e sem), comandos citados,
  `environment` do contrato, caminho do marketplace, skills citadas. Achou 1 erro na 1ª execução
  (`mjrp-env-setup` no README, inexistente). O HOWTO parou de mandar instalar PyYAML e passou a dizer
  **de onde** rodar o `marketplace add` — dois dos seis tropeços dele, agora com sensor.
- **2026-09-09 00:55** · **O `doctor_selftest` na máquina dele pegou um bug meu que aqui era invisível.** O
  `_yaml_min` perdia lista em bloco → `gates_open` vazio → **F2 calado**. Corrigido: lê lista, data e
  aninhado com comentário, e **grita** (`YamlNaoSuportado`) no que não sabe. Selftest reforçado com 5
  amostras + frontmatter + um caso de expectativa escrita à mão (vale sem PyYAML). 8 checagens acusam.
- **2026-09-08 17:57** · **W4 entra no doctor** — edição sem commit nas áreas vigiadas (identidade, concepts,
  decisions, skills, scripts, _archive). Aviso, não erro. Testado ao vivo: pegou a
  reestruturação do VISION e a mudança de pasta antes de eu saber. Achou um bug no próprio
  doctor no caminho: `sh()` faz strip e comia o estado da primeira linha do porcelain.
- **2026-09-08 16:55** · **Furo:** nada no harness me avisa quando o Zé edita um arquivo no disco sem commitar.
  Só vi a edição porque ele perguntou e eu rodei `git status`. O doctor não olha o working tree.
- **2026-09-08 22:45** · **O `environment.setup` do contrato não roda na máquina do Zé** — declara
  `python3 -m pip install --user pyyaml`, e o Homebrew 3.14 é *externally managed*: o pip recusa. Ele
  teve que criar um venv à mão para o doctor rodar. **Ninguém verifica o `environment`** — o A1 executa
  só os `sensors`. O contrato declara um pré-requisito falso e o harness fica verde. Incidente
  documentado; candidato a checagem pela regra da ADR-0002.
- **2026-09-08 22:45** · **O doctor exige PyYAML; o `build_plugin.py` já lê YAML sem depender dele.** O sensor que é
  a porta de entrada de qualquer instância pede instalação para rodar — atrito exatamente onde não pode
  haver. O precedente de como resolver já está no próprio repo.
- **2026-09-07** · O `doctor` verifica a conformidade da instância, **não o trabalho**. Ficou
  verde durante um estrago inteiro. Sensor do entregável ainda não existe.
- **2026-09-07** · Resultado de sensor guardado em cache mente com o tempo — `.mjrp/sensors.json`
  precisa de invalidação por commit.

- **2026-09-09 20:05** · **Um sensor novo precisa de três casos, não de um.** O `doctor_selftest`
  ganhou o teto do `MEMORY.md` (BACKLOG #28c) com o caso do arquivo gordo — e isso não prova nada
  sozinho: um F1 que reprovasse **sempre** passaria nele. Os três que provam são: o gordo reprova,
  a seção que voltou reprova, e **o correto passa calado**. O terceiro é o que separa sensor de
  alarme. Vale a frase que já estava aqui: *sensor que reprova o que está certo ensina a ignorar
  vermelho.*
- **2026-09-09 20:06** · **Dois sensores contando a mesma coisa de jeitos diferentes.** No mesmo
  minuto, o `memory_check --forma` dizia "`## Now` com 13 linhas" e o F1 do doctor dizia 8, para
  o mesmo arquivo. Nenhum dos dois estava errado no próprio critério; errado era haver dois
  critérios. O `memory_check` passou a contar exatamente como o `now_section()` do doctor. Número
  de sensor que discorda de outro número de sensor não gera dúvida sobre qual está certo — gera
  descrédito nos dois.

- **2026-09-09 20:35** · **Uma checagem que existe e não roda é uma checagem que não existe.** O
  `entry_check` conferia o `environment` do contrato desde 09/09 — e leva **92 segundos**, porque
  clona o repositório num temporário para provar que a porta abre num clone limpo. Por isso ele
  está fora do `sensors:`, e por isso, na prática, ninguém rodava a checagem. A divisão que ficou:
  **o barato e diário vai para o doctor** (o runtime declarado existe nesta máquina, o `setup` não
  está em branco), **o caro e raro fica no `entry_check`**, rodado à mão. E executar o `setup` fica
  do lado caro **de propósito** — o doctor roda em todo `SessionStart`, e rodar um comando de setup
  ali seria o harness instalando coisa nas costas do Zé.
- **2026-09-09 20:36** · **"Em branco" não é "nenhum".** Um `environment.setup` vazio parece
  inofensivo e diz duas coisas diferentes: *não há pré-requisito* ou *ninguém preencheu*. O doctor
  reprova o branco e aceita a palavra `nenhum` — declarar que não há é informação; omitir não é.

- **2026-09-09 20:45** · **Resultado guardado é uma afirmação sobre código, e código muda.** O
  `.mjrp/sensors.json` guardava `code: 1` para o sensor do loop enquanto o `loop_selftest` já
  estava consertado e passando. O registro **era verdadeiro quando foi escrito e falso quando foi
  lido**, e nada nele dizia qual dos dois. A correção é uma digital do estado do repositório
  gravada junto do resultado — e ela **não** é só o HEAD: a maior parte do dia o trabalho está sem
  commit, então entram também o `git status` filtrado dos derivados e o tamanho e mtime do que ele
  nomeia. Filtrar os derivados não é detalhe: sem isso o próprio arquivo de cache mudaria a
  digital ao ser escrito, e nenhum registro casaria com o estado seguinte.
- **2026-09-09 20:46** · **Registro velho não é reprovação — é "não avaliável".** Aprovar a partir
  dele era o defeito; reprovar seria inventar uma falha que ninguém viu. O `--skip-sensors` passou
  a dizer *não sei, rode sem a flag*, que é o **exit 2** do contrato do harness aplicado dentro de
  uma checagem. E o caso que quase ninguém escreve: o registro do **mesmo** estado tem que ser
  **usado**. Sem esse caso, um cache que nunca casasse passaria no teste e o `--skip-sensors`
  ficaria inútil sem ninguém notar.

- **2026-09-14 12:00** · **`stop_gate.py` parou de tratar exit 1 e exit 2 como a mesma coisa.**
  A ADR-0002 §8 já dizia "não é verde nem vermelho", mas o `gate()` gravava `passed = (código ==
  0)` e bloqueava os dois com a mesma mensagem — achado numa revisão manual das ADRs no Kindle
  (BACKLOG #6). A trava continua igual nos dois casos (não avaliado não é são), só a mensagem
  mudou: exit 2 agora diz que o problema é o próprio critério (caminho, contrato ausente), não o
  trabalho. `hooks_selftest.py` ganhou o caso 7 pra provar. `AGENTS.md` documenta a distinção
  perto do resto dos sensores.

- **2026-09-14 13:45** · **I5 e W6: um projeto aberto fora do Claude Code não herdava nada
  automaticamente.** O Zé começou um projeto novo direto no Gemini, sem passar por
  onboarding/bootstrap. Dois furos concretos: (1) o `PRINCIPLES.md` não foi herdado em
  lugar nenhum — nem `AGENTS.md`, nem `constitution.md`; (2) foi criado um `CHARTER.md`
  cheio, o padrão que a migração CHARTER→PRD (BACKLOG #33/#44) devia ter aposentado. A causa
  raiz dos dois: `.claude/settings.json` (`SessionStart`/`Stop`) só existe para o Claude Code —
  nenhuma outra AI Platform passa por ali, então nada força a herança nem a leitura do
  bootstrap. **I5** (obrigatória — consome 1 das 3 vagas do teto de 12, sobram 2): reprova se
  nem `AGENTS.md` nem `docs/specs/constitution.md` declaram a herança do `PRINCIPLES.md`
  (PRINCIPLES §III). **W6** (aviso): avisa quando existe um `CHARTER.md` de mais de 10
  linhas (não o stub de retrofit) sem `docs/specs/prd.md` correspondente — parece charter novo,
  não migração em andamento. Os dois têm 3–4 casos no `doctor_selftest.py`, no padrão do W5
  (caso que acusa + caso que fica calado). **O que ainda falta, fora do doctor**: nada garante
  que um projeto novo, em qualquer AI Platform, comece com a estrutura certa — é o que motivou
  desenhar o `new_project.py`, um scaffolding determinístico rodado pelo Zé antes de abrir
  qualquer IA (ver BACKLOG e ADR pendente sobre "como um projeto começa, de verdade").

## Related
[[harness-elements]] · harness-kaizen · skill-distribution · ADR-0002 · ADR-0007
