---
name: mjrp-design
description: >
  MJRP Design Protocol for creating information architecture, UX/UI prototyping using ux-ui-designer,
  system-architect, and Stitch before implementation. Three sequential phases: (1) info-arch.md —
  sitemap, nav hierarchy, page templates; (2) design-system.md — visual tokens and component specs;
  (3) Stitch prototypes — high-fidelity mockups.
  Trigger: design protocol, design this feature, create mockup, UX design, UI design, prototyping,
  fase de design, information architecture, info-arch, page templates, sitemap.
---

# Design Protocol

**Purpose**: Bridge the gap between Discovery (the "What") and SDD Implementation (the "How-to-code").
Covers three sequential phases: Information Architecture → Visual Design System → High-Fidelity Prototypes.

## Pré-condições obrigatórias

Antes de iniciar qualquer fase deste protocolo, verificar:

- [ ] `docs/specs/story.md` existe com user stories INVEST-ready
- [ ] `docs/specs/arch.md` existe (mesmo que skeleton) — Claude precisa saber as rotas e layers
- [ ] `docs/specs/data-model.md` existe (mesmo que skeleton) — Claude precisa saber as entidades

> Se arch.md ou data-model.md não existirem: criar skeletons usando `mjrp-system-architect` skill
> ANTES de avançar. IA não pode ser definida sem saber quais entidades e rotas o sistema tem.

---

## 1. Participating Skills & Tools

- **`ux-ui-designer`**: Owns information architecture (Phase 0), usability heuristics, accessibility, wireframes
- **`system-architect`**: Ensures architecture and data model support the proposed IA and UX
- **`aesthetic-designer`**: Extracts visual DNA and generates design system direction
- **`design-system`**: Produces design-system.md with tokens, component specs, do's and don'ts
- **`StitchMCP`** (Tool): Generates high-fidelity UI mockups for visual approval

---

## 2. Phase 0: Information Architecture (`ux-ui-designer`)

**When**: Sempre. Esta é a primeira fase — você não estiliza o que não estruturou.
**Inputs**: `story.md` + `arch.md` + `data-model.md`
**Output**: `docs/specs/info-arch.md`

### Steps

1. **Sitemap**: Mapear todas as rotas do sistema do ponto de vista do usuário (não do roteador).
   - Usar `arch.md` como referência de rotas técnicas
   - Organizar em árvore hierárquica com URLs explícitas

2. **Hierarquia de navegação**: Definir os três níveis:
   - Primária (nav principal — sidebar, top bar, bottom nav)
   - Secundária (dentro de cada seção — tabs, filtros, sub-nav)
   - Terciária (contexto — breadcrumbs, prev/next, anchors)

3. **Page Templates**: Para cada tipo de página distinto, criar um ASCII wireframe com:
   - Zonas de conteúdo nomeadas (Hero, Grid, Sidebar, etc.)
   - Dimensões e comportamentos de cada zona
   - Componente responsável por cada zona
   - Tabela Zona | Conteúdo | Componente

4. **User Flows por persona**: Como cada persona entra e navega pelo produto

5. **Mapeamento Template → Épico SDD**: Qual SDD produz qual template

### Output format: `docs/specs/info-arch.md`

```markdown
# Information Architecture — [Projeto]
## 1. Sitemap (árvore de rotas)
## 2. Hierarquia de Navegação (primária, secundária, terciária)
## 3. Page Templates (T1–TN com ASCII wireframes e tabelas de zona)
## 4. Fluxos por Persona
## 5. Mapeamento Template → Épico SDD
## 6. Decisões de IA Tomadas
```

⛔ **GATE**: Aprovar `info-arch.md` antes de Phase 1. Mudanças na estrutura após o design visual
estar definido são 5–10x mais caras que mudanças antes.

---

## 3. Phase 1: UX Strategy (`ux-ui-designer`)

**Inputs**: `info-arch.md` (aprovado) + `story.md`

1. **Analyze Requirements**: Revisar User Stories e Acceptance Criteria em `story.md`
2. **Define Flow & Heuristics**: Determinar estados de cada page template (loading, error, empty)
   e constraints de acessibilidade (WCAG 2.1 AA)
3. **Draft UI Constraints**: Regras de layout e interação para cada template — alimentam o design system

---

## 4. Phase 2: Architectural Feasibility (`system-architect`)

**Inputs**: `info-arch.md` + `arch.md` + `data-model.md`

1. **Data Model Check**: `data-model.md` suporta o conteúdo de cada page template?
   - Cada zona de conteúdo tem entidade correspondente?
   - Filtros e navegação secundária têm suporte de dados?
2. **Layer Boundaries**: A IA proposta força alguma violação de layer?
   - Ex: frontend acessando diretamente vault bypassing APIs?
3. **Atualizar skeletons**: Se mudanças forem necessárias em arch.md ou data-model.md, aplicar aqui

---

## 5. Phase 3: Visual Design System (`aesthetic-designer` + `design-system`)

**Inputs**: `info-arch.md` (page templates aprovados) + VISION.md (vibe/DNA visual)

1. **Extract Visual DNA** (`aesthetic-designer`): Identificar paleta, tipografia, espaçamento e
   linguagem visual a partir de referências (Stitch, screenshots, brief)
2. **Populate design-system.md** (`design-system`):
   - Color tokens (CSS custom properties + Tailwind mapping)
   - Motion tokens + Z-index scale
   - Typography scale
   - Spacing scale
   - Component specs (por page template de info-arch.md)
   - Do's and Don'ts

**Output**: `docs/design/design-system.md`

> **Regra**: design-system.md não contém código TSX de implementação.
> Specs visuais (anatomia, variantes, estados) + referência para `components-staging.md`.

---

## 6. Phase 4: High-Fidelity Prototyping (`StitchMCP`) — Opcional

**Inputs**: `design-system.md` + `info-arch.md` (page templates)

1. **Generate Mockup**: Combinar design tokens + page template + vibe para prompt do Stitch
   - Exemplo: "Generate [Template T2 — Dashboard] applying [design-system.md tokens]. Background: surface (#F9F9F9). Sidebar: Navy (#000050). Hero: PP Fragment Glare Bold 64px."
2. **Save & Review**: Salvar HTML em `design/inception/` e pedir ao usuário para revisar no browser
3. **Iterate**: Ajustar até aprovação visual
4. **Log**: Adicionar referências de Stitch IDs em `docs/design/design-system.md` §15 Visual Reference

---

## 7. Exit Criteria

- [ ] `docs/specs/info-arch.md` existe, aprovado, com todos os page templates do produto
- [ ] `docs/design/design-system.md` existe e referencia info-arch.md para page templates
- [ ] arch.md e data-model.md foram validados/atualizados para suportar a IA proposta
- [ ] Próximo passo é handoff para SDD via `mjrp-sdd-specify` por épico
