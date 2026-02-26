# Design System: Minimal Dark

> Documento fonte de tokens visuais e componentes do projeto.

## Paleta de Cores
- Background: #0d1117 — main background
- Surface: #161b22 — cards, panels, elevated surfaces
- Border: #30363d — subtle borders
- Text Primary: #e6edf3 — main text
- Text Secondary: #8b949e — labels, meta info
- Accent Cyan: #58a6ff — ações secundárias, links, estados de foco
- **Accent Green: #3fb950** — ação primária (Download Local / Save), estados de sucesso (Variante 2)
- Error: #f85149 — error states
- Warning: #d29922 — warning states

## Tipografia
- Code/Textarea: JetBrains Mono — monospace
- UI Labels: Inter — sans-serif
- Scale: H1: 1.5rem, H2: 1.25rem, Body: 0.875rem, Small: 0.75rem

## Espaçamento
- Base unit: 8px
- Border radius: 6px (panels), 4px (buttons), 2px (inputs)

## Componentes-Chave
- **Layout Grid**: Split-screen (50/50). Em resoluções móveis/menores, o layout empilha o editor de código no topo (Stack) e o preview embaixo.
- **Header/Toolbar**: Minimalista. Fica no topo da coluna do editor de código. Contém: botão "Clear", "Save to Drive" (desabilitado) e "Download Local" (cor Accent Green).
- **Textarea de Código**: Sem bordas agressivas, fonte Monospace padrão (JetBrains).
- **Iframe Preview**: Container branco puro (`#ffffff`) do lado direito. Imperativo manter fundo branco para garantir fidelidade da renderização sem o *bleed* do dark mode global.

## Referência Visual
- GitHub Dark Mode + CodePen minimal aesthetic
- **StitchMCP Prototype ID**: `54afd0a7b1b04cabaf1a474058705575` (Variant 2 - Green Accent View)
