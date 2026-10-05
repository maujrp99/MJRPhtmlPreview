# S-79 · MJRPhtmlPreview → grafo de requisitos · 2026-10-05 16:14

## IDs (story.md → nós)
`US-NN` não casa com o padrão do sensor → `S-NN`, **mesmo número**: US-01→S-01 … US-12→S-12.
NFR de `spec.md` §3: NFR01→NFR-01, NFR02→NFR-02, NFR03→NFR-03, NFR04→NFR-04. NFR05/06/07 já eram as stories US-07/08/09 → só S-07/S-08/S-09 (não duplicados).

## Resultados e épicos
ROADMAP só tinha placeholders ("[primeira fase]") → nova seção `## Resultados` com os 4 Goals do PRD § Objetivo e métricas, copiados, `^OUT-01..04`. Nada reescrito.
Épicos = os 4 Goals (story.md não tinha seções):
- EP-01 Preview instantâneo → OUT-01 · S-01, S-07, S-08, S-09, S-10, S-11
- EP-02 Salvar no Google Drive → OUT-02 · S-03, S-06
- EP-03 Salvar localmente e exportar → OUT-03 · S-02, S-04, S-05
- EP-04 Edição de texto no preview → OUT-04 · S-12

## Features
- F01-core-preview-and-export ← spec/plan/tasks planos (M1–M3.5, sessão 02/26, M6) · Done · imports S-01..S-09
- F02-markdown-mermaid-render ← m4/ · Done · imports S-10
- F03-load-and-edit ← m5/ (+ _backups) · Done (tasks "Completed", tudo [x]; o spec dizia "Draft") · imports S-11, S-12
Sem REQ-/TASK- no filho (usa FR0x.y, T-05.x) → nada de `implements::`/`verified_by::` acrescentado; conteúdo intacto, exceto os 2 links `../m5/` → `./` em F03 plan/tasks.

## Status e evidência
S-01..S-12 **Done**: story.md "✅ Done" + feature Done que importa + `delivered_by`:
S-01, S-02 f63600f · S-03 ff78aa1 · S-04 d690cc2 · S-05 bc00ed3 · S-06 f51beaa · S-07 0069a4c · S-08 6e0d518 · S-09 4e3662e · S-10 c7c8555 · S-11, S-12 842ba62.
Nenhum **Accepted**: o uat.md não registra aceite (só UAT-001, aberto).
NFR-01, NFR-03 Done (f63600f) · NFR-04 Done (f51beaa) · **NFR-02 Backlog**: o sandbox do iframe não aparece em tasks nem no git.
`points_to`: o Done também é cobrado, e o filho não tinha info-arch.md nem behavior.md → criado `docs/specs/behavior.md` com 12 estados descritos a partir dos AC do story.md (retroativo, sem julgamento, como no harness).

## Não mapeado
- Milestone 6 (drag & drop + memória de pasta, 3bd570d) não tem story → ficou só nas tasks da F01.
- PRD In Scope "syntax highlighting (optional)" → sem story nem entrega.
- Introdução do prd.md ainda cita `[story.md](story.md)`, link agora quebrado (deixado como estava).
- `.gitkeep` mantidos. Sensor rodado com um shim local de `doctor.py` (falta em refs/mjrp-scripts).

## Perguntas para o MJRP
1. Épicos pelos 4 Goals do PRD, ou pelos milestones (M1…M5)?
2. Os Goals do PRD como resultados no ROADMAP: valem? Os placeholders "Agora/Depois" ficam?
3. PDF e PNG (S-04, S-05) servem ao OUT-03 ("salvar local .html em 1 clique")? Ou pedem um resultado próprio?
4. Estados em behavior.md: aceita, ou quer estados de tela no info-arch.md (protótipo julgado)?
5. M6 drag & drop: vira story (S-13, EP-01, Done por 3bd570d)?
6. NFR-02 (sandbox do iframe): está no index.html? Se sim, Done com o commit.
7. Algum dos S-01..S-12 já é aceite seu (→ Accepted com `accepted_in`)?
