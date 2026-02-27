# Histórico de Sessões — MJRPhtmlPreview

## Session: 2026-02-25 — Instalação do Framework (Skills & Workflows)

> Date: 2026-02-25T14:40:00-03:00
> Participants: mpedroso + Antigravity
> Branch: main
> Duration: ~10 minutos

### Resumo Executivo
Nesta sessão, foi instalada a estrutura completa do MJRP Framework no projeto `MJRPhtmlPreview`. Copiamos as `skills` do pacote Antigravity e os `workflows` (protocolos SDD, etc) do repositório de governança base (`MJRPprojSetupFramework`) para o diretório local do projeto `.agent`. Isso garante que futuras conversas com agentes neste projeto terão acesso a todos os comportamentos customizados.

### Decisões Tomadas
- O diretório `.agent` armazenará as cópias das skills e workflows no escopo do repositório do projeto, assegurando portabilidade e isolamento, de forma que o Agente Antigravity compreenda seus protocolos localmente.

### Artefatos Gerados/Modificados
| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `.agent/skills/*` | Criado | 22 diretórios importados (e.g. `frontend-developer`, `system-architect`, etc.) |
| `.agent/workflows/*` | Criado | 20 protocolos `.md` importados (e.g. `sdd_protocol.md`, `debug_protocol.md`) |

### Pendências para Próxima Sessão
1. Fazer o commit / stage dos novos arquivos `.agent/` no git (salvo se definidos de forma diferente).
2. Executar o `/onboarding_protocol` se o próximo agente precisar compilar o contexto inteiro antes de focar numa task.
3. Avançar no backlog (`docs/specs/tasks.md`) desenvolvendo em single HTML vanilla (JS/CSS inline) conforme manda a Constituição associada a este projeto.

### Dados-Chave para Referência
- Total de Assets do Framework instalados: 22 Skills e 20 Workflows de processo na pasta `.agent`.

---

## Session: 2026-02-25 — Milestones M1 a M3.5 + Deploy (Full Build)

> Date: 2026-02-25T20:00:00 → 2026-02-26T00:23:00 -03:00
> Participants: mpedroso + Antigravity
> Branch: dev → main (merged)
> Duration: ~4 horas

### Resumo Executivo
Sessão maratona onde saímos do zero até o deploy completo de produção. Executamos o fluxo SDD integral: Discovery → Design → Architecture → Plan → Tasks → Implement → Deploy. Construímos um visualizador HTML client-side completo em um único `index.html` vanilla (sem backend, sem build tools).

### O Que Foi Feito
1. **M1 (MVP):** Implementado editor split-screen (textarea + iframe), live preview via `srcdoc`, download local `.html` via Blob, botão Clear. Design System "Minimal Dark" com JetBrains Mono + Inter.
2. **M2 (Google Drive):** Integração OAuth 2.0 via GSI, Google Picker para seleção de pasta, upload multipart via fetch puro para Drive API v3.
3. **M3 (Export):** Botão PDF via `contentWindow.print()` nativo. Botão PNG via `html2canvas` (com limitação conhecida para HTML dinâmico — documentada em `docs/debug-log.md`).
4. **M3.5 (BYOK):** Arquitetura "Bring Your Own Keys" — modal de Settings com engrenagem ⚙️, credenciais salvas em `localStorage`, eliminação do `config.js` hardcoded.
5. **Deploy:** GitHub Pages ativado na branch `main`. Resolvido problema de unrelated histories no merge `dev→main`. Site live em `https://maujrp99.github.io/MJRPhtmlPreview/`.
6. **Docs (SDD):** Backfill do `spec.md` (estava vazio), atualização de `plan.md`, `tasks.md`, `story.md` a cada milestone.

### Decisões Chave
- **Single HTML File:** Toda a aplicação vive em `index.html` — CSS e JS inline. Sem frameworks, bundlers ou transpilers.
- **BYOK over config.js:** Credenciais Google são injetadas pelo usuário via modal e salvas no `localStorage` do navegador. Nenhuma chave trafega pelo Git.
- **html2canvas aceita como trade-off:** Biblioteca externa adicionada exclusivamente para captura PNG. Limitação conhecida com HTML dinâmico (canvas/charts).
- **PDF via print() nativo:** Zero dependências adicionais — usa o diálogo de impressão do Chrome/Safari.
- **M4 aprovada pelo Product Designer:** Markdown + Mermaid parser é o pivô natural do produto. Bibliotecas `marked.js` e `mermaid.js` via CDN.

### Arquivos Modificados
| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `index.html` | Criado/Atualizado | Aplicação completa: UI, CSS, JS, Google Drive, BYOK Modal |
| `docs/specs/spec.md` | Preenchido | Requisitos Funcionais (FR01-FR04) e NFRs retroativos |
| `docs/specs/plan.md` | Atualizado | M1-M3 marcadas CONCLUÍDO, M4 planejada |
| `docs/specs/tasks.md` | Atualizado | Tasks M3.5 (BYOK) completadas |
| `docs/specs/story.md` | Atualizado | US-01 a US-05 com acceptance criteria |
| `docs/debug-log.md` | Criado | Bug tracking: html2canvas + HTML dinâmico |
| `.gitignore` | Atualizado | `config.js` adicionado ao ignore |
| `config.js` | Deletado | Substituído pela arquitetura BYOK |

### Pendências para Próxima Sessão
1. **M4: Markdown & Mermaid** — Especificar tasks, injetar `marked.js` + `mermaid.js`, implementar detecção automática de sintaxe MD vs HTML no textarea, renderizar diagramas Mermaid como SVG inline.
2. **Debug PNG:** Investigar alternativas ao `html2canvas` para HTMLs dinâmicos (ex: `dom-to-image`, ou abordagem com Puppeteer cloud function).
3. **Polish UI:** Micro-animações, hover effects, possível dark/light toggle no iframe.

### Contexto Técnico Rápido
- **Stack:** Vanilla HTML/CSS/JS, single file `index.html`, zero build.
- **Deploy:** GitHub Pages, branch `main`, URL: `https://maujrp99.github.io/MJRPhtmlPreview/`
- **Google Cloud:** Projeto com Drive API + Picker API habilitadas. OAuth Client ID com origens `localhost:8000` e `maujrp99.github.io`. Test user: `maujrp@gmail.com`.
- **Branches:** `dev` (desenvolvimento) → merge para `main` (produção/pages).
- **Credenciais:** BYOK via `localStorage` key `mjrp_google_keys`.
- **Design System:** Minimal Dark — tokens em `:root` CSS vars, fontes Inter + JetBrains Mono via Google Fonts CDN.

---

## Session: 2026-02-26 — Fullscreen Preview, Base Href & Image Privacy

> Date: 2026-02-26T15:58:00 → 2026-02-26T19:34:00 -03:00
> Participants: mpedroso + Antigravity
> Branch: dev → main (merged)
> Duration: ~1 hora (com intervalo)

### Resumo Executivo
Sessão focada em 3 melhorias de UX e segurança: resolução de caminhos relativos de imagem no iframe via `<base href>`, modo Fullscreen Preview (toggle para esconder o editor), e migração de imagens para Google Drive Links (privacidade).

### O Que Foi Feito
1. **Base Href Injection:** Implementada função `injectBaseHref()` que insere automaticamente `<base href="...images/">` no HTML antes de renderizar no iframe. Resolve caminhos relativos de imagem sem que o usuário precise escrever o path completo.
2. **Fullscreen Preview Mode:** Adicionado botão "⛶ Preview" (azul, na toolbar) que esconde o editor e expande o iframe para 100% da tela. Barra superior "✏️ Editor" permite voltar ao modo split.
3. **Image Privacy:** Imagens removidas do repositório público. Pasta `images/` adicionada ao `.gitignore`. Estratégia definida: usar Google Drive thumbnail links (`drive.google.com/thumbnail?id=ID&sz=w1000`) para servir imagens com controle de acesso.
4. **Organização de Assets:** Criada pasta `images/` local. Imagens LATAM renomeadas para nomes limpos (`status-report.png`, `the-road-ahead.png`).

### Decisões Chave
- **Base href aponta para `/images/`:** Permite que HTMLs colados usem apenas `src="filename.png"` sem path completo. Trade-off aceito: se o HTML tiver outros assets relativos fora de `/images/`, precisarão de path explícito.
- **Google Drive como CDN privada (Opção B):** Imagens hospedadas no Drive com share link "Anyone with the link". URL transformada para thumbnail endpoint direto. Permite revogar acesso a qualquer momento.
- **`images/` no `.gitignore`:** Imagens locais ficam no Mac para uso com `localhost`, mas nunca sobem para o GitHub público.

### Arquivos Modificados
| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `index.html` | Atualizado | Base href injection, fullscreen toggle CSS + JS |
| `.gitignore` | Atualizado | Adicionado `images/` |
| `images/` | Criado local, removido do Git | Pasta local para assets protegidos |

### Pendências para Próxima Sessão
1. ~~**M4: Markdown & Mermaid** — Concluído na sessão seguinte.~~
2. **Debug PNG:** Investigar alternativas ao `html2canvas` para HTML dinâmico.

---

## Session: 2026-02-26/27 — M4 Markdown & Mermaid + Modularização

> Date: 2026-02-26T20:00:00 → 2026-02-27T15:00:00 -03:00
> Participants: mpedroso + Antigravity
> Branch: dev → main (merged)
> Duration: ~2 sessões (~4 horas total)

### Resumo Executivo
Completamos a Milestone 4 seguindo o SDD Protocol integral (Specify → Plan → Tasks → Implement). Além do Markdown/Mermaid, fizemos uma refatoração arquitetural significativa: modularizamos o JavaScript inline do `index.html` em 4 módulos separados. A sessão incluiu debugging de um problema de download causado por versão desatualizada do Chrome.

### SDD Flow Executado
1. **Spec** (`docs/specs/m4/spec.md`) — FR04.1 a FR04.4, NFRs, edge cases. APPROVED.
2. **Plan** (`docs/specs/m4/plan.md`) — Pipeline dual, lazy loading, ASCII mockups. APPROVED.
3. **Tasks** (`docs/specs/m4/tasks.md`) — 8 steps (0-8 incluindo modularização), 25 tasks. APPROVED.
4. **Implement** — Código implementado, testado e deployed em GitHub Pages.

### O que foi implementado
| Feature | Arquivo | Detalhes |
|---------|---------|---------|
| JS Modularization | `js/*.js` | 4 módulos: app, preview, drive, export |
| Markdown Rendering | `js/preview.js` | `marked.js` CDN + `detectInputType()` |
| Mermaid Diagrams | `js/preview.js` | Lazy-loaded dentro do iframe |
| MD Styling | `js/preview.js` | `wrapWithMdStyles()` — GitHub-like |
| Smart Download | `js/export.js` | `.md` para Markdown, `.html` para HTML |
| Script Load Order | `index.html` | CDN → modules → Google async (no head) |

### Decisões Técnicas
- **Modularização vanilla**: Sem ES modules/import, sem bundler. Apenas `<script src="">` tags no final do `<body>`.
- **Mermaid lazy**: Carrega 1.5MB apenas se bloco mermaid detectado. Carrega **dentro do iframe** para isolamento.
- **Script order fix**: CDN libs → app modules → Google async scripts. Evita `ReferenceError` em callbacks `onload`.
- **DOMContentLoaded removido**: Desnecessário com scripts no final do body.

### Bug Encontrado & Resolvido
- **Sintoma**: Downloads com nomes UUID ao invés de `preview_*.html`.
- **Investigação**: Criamos `test.html` minimal — mesmo bug. Isolou o problema ao browser.
- **Causa raiz**: Chrome desatualizado. Após update do browser, downloads funcionaram normalmente.
- **Lição**: Sempre verificar se o ambiente (browser, server) está atualizado antes de debugar o código.

### Arquivos Alterados
| Arquivo | Ação | Descrição |
|---------|------|-----------|
| `index.html` | Refatorado | 759 → 421 linhas (só HTML+CSS) |
| `js/app.js` | Novo | Bootstrap e event wiring |
| `js/preview.js` | Novo | Render pipeline MD/HTML + Mermaid |
| `js/drive.js` | Novo | Google Drive OAuth/Picker/Upload + BYOK |
| `js/export.js` | Novo | Download, PDF, PNG |
| `docs/specs/m4/*` | Novo | spec.md, plan.md, tasks.md |
| `docs/specs/arch.md` | Reescrito | Arquitetura modular documentada |
| `CHARTER.md` | Atualizado | M4 ✅ Done |
| `docs/specs/story.md` | Atualizado | US-10 ✅ Done |
| `docs/specs/tasks.md` | Atualizado | M4 ✅ Done |
| `docs/specs/plan.md` | Atualizado | M4 ✅ Concluído |

### Pendências para Próxima Sessão
1. **M5 (a definir)**: Possibilidades — syntax highlighting no editor, temas, keyboard shortcuts, templates.
2. **Debug PNG**: html2canvas tem limitações com HTML dinâmico.
3. **constitution.md**: Atualizar para refletir arquitetura modular (não é mais single-file).
