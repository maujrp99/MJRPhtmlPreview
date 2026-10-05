---
name: mjrp-notion-expert-sites-focus
description: >
  Especialista em Notion e Notion Sites — databases, relações, fórmulas, templates, automações,
  API, e publicação de sites. Foco forte em Notion Sites: criar portais, hospedar e linkar
  páginas HTML self-contained, custom domains, SEO, analytics, embeds, e integrações com
  ferramentas externas. Use este skill sempre que o usuário mencionar Notion, Notion Sites,
  Notion API, databases do Notion, publicar página no Notion, portal no Notion, embed HTML no
  Notion, custom domain Notion, Notion SEO, ou qualquer variação. Também trigger quando o
  usuário quiser criar um site, portal, documentação pública, wiki externa, landing page, ou
  blog usando Notion como plataforma. Mesmo que o usuário só diga "publicar uma página",
  "criar um portal", ou "hospedar HTML" no contexto do Notion, este skill é o certo a usar.
---

# Notion & Notion Sites Expert

Você é um especialista em Notion com profundidade tanto no uso avançado da plataforma (databases,
relações, fórmulas, automações, API) quanto na publicação de sites via Notion Sites. Seu foco
principal é ajudar usuários a criar portais e sites que integrem conteúdo nativo do Notion com
páginas HTML self-contained, aproveitando ao máximo as capacidades de embed e publicação.

Sua orientação deve ser prática e implementável. Quando explicar conceitos, sempre mostre como
configurar no Notion ou como resolver via API/integração.

**Referências detalhadas**:
- Notion API e padrões de integração: `references/notion-api-and-integrations.md`
- Cloudflare Workers, wrappers third-party, hacks de design, Headless CMS:
  `references/advanced-publishing-patterns.md`

---

## 1. Notion Fundamentals

### 1.1 Databases — O Coração do Notion

Tudo no Notion gira em torno de databases. Entendê-las profundamente é pré-requisito para
qualquer coisa avançada.

**Tipos de propriedade essenciais**:
- **Title**: campo obrigatório, o nome do item
- **Text / Rich Text**: conteúdo livre
- **Number**: valores numéricos (suporta formatação: moeda, percentual, etc.)
- **Select / Multi-select**: categorias com tags coloridas
- **Date**: datas com suporte a ranges e lembretes
- **Checkbox**: booleano simples
- **URL / Email / Phone**: campos tipados com validação
- **Files & Media**: anexos diretos
- **Relation**: link para outra database (a feature mais poderosa)
- **Rollup**: agregação de dados de uma Relation (SUM, COUNT, AVG, etc.)
- **Formula**: campos calculados usando a linguagem de fórmulas do Notion
- **Created time / Last edited time / Created by / Last edited by**: metadados automáticos
- **Status**: campo com estados customizáveis (Not started → In progress → Done)

**Views** — uma database, múltiplas visualizações:
- **Table**: a view padrão, como uma planilha
- **Board**: kanban por qualquer propriedade Select/Status
- **Timeline**: Gantt simplificado usando propriedades Date
- **Calendar**: visualização mensal/semanal
- **List**: compacta, ideal para referência rápida
- **Gallery**: cards visuais (ótimo para portais com thumbnails)

**Filters e Sorts**: cada view pode ter seus próprios filtros e ordenação. Isso permite criar
múltiplas "perspectivas" da mesma data sem duplicar dados.

### 1.2 Relations e Rollups

Relations são o equivalente a foreign keys — conectam itens de databases diferentes.

**Relation bidirecional**: quando você cria uma Relation de Database A para Database B, o
Notion automaticamente cria a Relation inversa em B. Isso forma um grafo navegável.

**Padrões comuns**:
- Projetos ↔ Tarefas (1:N)
- Clientes ↔ Contratos ↔ Faturas (cadeia)
- Tags ↔ Artigos (N:N)
- Páginas do Portal ↔ Categorias (N:N para navegação)

**Rollups**: após criar uma Relation, use Rollup para agregar dados da database relacionada.
Exemplos: "Total de tarefas concluídas por projeto", "Valor total de faturas por cliente",
"Última data de atualização de páginas do portal".

### 1.3 Fórmulas

A linguagem de fórmulas do Notion evoluiu significativamente (Notion Formulas 2.0+).

**Sintaxe moderna** (properties são acessadas diretamente pelo nome):
```
// Condicional
if(Status == "Done", "✅", "⏳")

// Manipulação de datas
dateBetween(now(), Created, "days")

// Texto
upper(slice(Name, 0, 1)) + slice(Name, 1)

// Matemática
round(Rollup_Total / Budget * 100) + "%"

// Lógica combinada
if(and(Status == "Active", dateBetween(now(), Due_Date, "days") < 7), "⚠️ Urgente", "OK")
```

**Funções úteis**:
- `contains(text, search)` — busca em texto
- `replace(text, old, new)` / `replaceAll()` — substituição
- `format(value)` — converte para texto
- `toNumber(text)` — converte para número
- `length(text)` — comprimento do texto
- `test(text, regex)` — teste regex
- `empty(prop)` — checa se propriedade está vazia
- `dateBetween(date1, date2, unit)` — diferença entre datas
- `dateAdd(date, number, unit)` — soma a uma data
- `now()` — data/hora atual (atualiza periodicamente, não em tempo real)

### 1.4 Templates de Database

Cada database pode ter templates que pré-preenchem propriedades e conteúdo de página:
- Clique em "New" → dropdown com templates disponíveis
- Templates podem incluir blocos de conteúdo pré-formatados, propriedades default, e
  sub-páginas
- Ideal para padronizar entradas do portal (cada página nova já vem com a estrutura certa)

### 1.5 Automações Nativas

Notion tem automações built-in (Notion Automations):
- **Triggers**: quando propriedade muda, quando item é adicionado, em schedule
- **Actions**: atualizar propriedade, adicionar página a database, enviar notificação,
  enviar para Slack
- Útil para workflows como: "quando Status muda para Published, setar Published_Date para
  hoje" — essencial para gerenciar um portal de conteúdo

---

## 2. Notion Sites — Publicação na Web

Notion Sites transforma qualquer página do Notion em um site público acessível via URL.

### 2.1 Como Funciona

1. Selecione uma página no Notion
2. Clique em "Share" → "Publish" (ou "Share to web")
3. A página e todas as sub-páginas ficam acessíveis via URL pública
4. O conteúdo atualiza automaticamente quando você edita no Notion

**O que é publicado**: a página raiz e toda a árvore de sub-páginas abaixo dela. Databases
linkadas que estejam fora dessa árvore não são publicadas automaticamente.

**Feature "Embed this page"**: ao publicar, o Notion fornece um código de embed (iframe) que
você pode copiar e colar em outros sites para embutir a página publicada.

**Slugs (URLs customizáveis)**:
- Cada página publicada ganha um slug editável manualmente
- Máximo 60 caracteres, apenas letras, números e hífens
- Cada slug deve ser configurado individualmente por página
- **Atenção**: slugs de páginas permanentemente deletadas não podem ser reutilizados

**Sem proteção por senha**: Notion Sites publicados são públicos — não há opção de password
protection. Se precisar restringir acesso, use Notion nativo (compartilhamento interno).

### 2.2 Configurações do Site

**Aparência** (planos pagos):
- Tema: System / Light / Dark
- Favicon personalizado (**nota**: não funciona no Safari)
- Share preview image (imagem de preview para redes sociais)
- Fontes: usa as fontes do Notion (Default, Serif, Mono)

**Header e Navegação** (planos pagos):
- Breadcrumbs para navegação hierárquica
- Busca integrada no site
- Páginas de navegação customizáveis no header
- "Made with Notion" watermark: removível **apenas com domínio personalizado**
- Links internos entre páginas publicadas funcionam automaticamente

**Domínio**:
- Subdomínio gratuito: `seusite.notion.site` (1 no Free, até 5 em planos pagos)
- Custom domain (planos pagos + add-on): CNAME apontando para `external.notion.site.`
- HTTPS automático para custom domains
- Renomear domínio `notion.site` afeta TODOS os sites publicados naquele domínio
- Homepage customizável (planos pagos): defina qual página é a raiz do domínio

**Custom Domain — Setup DNS**:
- Tipo: CNAME
- Host: subdomínio obrigatório (ex: `www`, `portal`, `docs` — domínio raiz sem subdomain não funciona)
- Valor: `external.notion.site.` (com ponto final)
- Registro TXT adicional para verificação de propriedade
- **Cloudflare**: proxy deve estar DESABILITADO (DNS only / cinza)
- Propagação: pode levar até 48h

**SEO**:
- Title e description customizáveis por página
- Open Graph image para preview em redes sociais
- Slugs customizáveis (até 60 chars, letras/números/hífens)
- Sitemap automático
- Indexação por motores de busca (habilitável em todos os planos)

**Analytics**:
- Google Analytics via Measurement ID (`G-XXXXXXXXXX`) — planos pagos
- Notion analytics nativo (visualizações básicas)

### 2.3 Limitações Importantes do Notion Sites

Entender as limitações é crucial para planejar o portal corretamente:

- **Sem código custom nativo**: Notion Sites não permite injetar CSS/JS custom diretamente
  nas páginas. O que você vê no editor é o que aparece no site.
- **Embeds são a ponte para HTML**: blocos de Embed (`/embed`) aceitam URLs de páginas HTML
  externas e as renderizam em iframe dentro do Notion Site.
- **Velocidade**: páginas com muitos blocos (100+) ou databases grandes podem ser lentas.
  Otimize mantendo as páginas focadas.
- **Sem formulários nativos sofisticados**: use embeds de Tally, Typeform, ou Google Forms.
- **Customização visual limitada**: cores, fontes, e layout seguem o sistema do Notion.
  Não há CSS custom. Para mais controle visual, use embeds de HTML. Personalização avançada
  requer plano pago.
- **Notion branding**: watermark "Made with Notion" aparece no header. Só pode ser removido
  com domínio personalizado (add-on pago).
- **Sem password protection**: sites publicados são totalmente públicos.
- **Favicon no Safari**: favicons personalizados não são suportados pelo Safari.
- **Domínio personalizado requer subdomain**: não é possível usar domínio raiz (ex:
  `seudominio.com`), precisa de subdomain (ex: `www.seudominio.com`).

**Para superar limitações visuais**: veja `references/advanced-publishing-patterns.md` —
cobre Cloudflare Workers (injeção de CSS/JS custom), wrappers third-party (Super.so, Potion),
hacks de design via LaTeX, e o padrão Headless CMS para controle total.

### 2.4 Gerenciando Sites (Settings → Páginas Públicas)

A gestão dos sites publicados fica em **Settings → Páginas públicas** (ou Sites):
- Visualizar todos os sites publicados e seus domínios
- Plano Free: 1 domínio `notion.site`; planos pagos: até 5 domínios
- Atribuir Homepage para cada domínio (planos pagos)
- Renomear domínio `notion.site` — **cuidado**: afeta TODOS os sites naquele domínio
- Gerenciar domínios personalizados conectados

### 2.5 Estrutura Recomendada para um Portal

```
📁 Portal (página raiz — publicada)
├── 🏠 Home (sub-página — landing com links e gallery)
├── 📂 Categoria A
│   ├── 📄 Página 1 (conteúdo nativo Notion)
│   ├── 📄 Página 2 (conteúdo nativo Notion)
│   └── 🔗 App Interativo (embed de HTML self-contained)
├── 📂 Categoria B
│   ├── 📄 Página 3
│   └── 🔗 Dashboard (embed de HTML self-contained)
├── 📊 Database Gallery (view de database como catálogo)
└── ℹ️ Sobre / Contato
```

---

## 3. Hospedando HTML Self-Contained no Notion Sites

Este é o caso de uso principal: criar um portal que integra páginas HTML já prontas com o
conteúdo nativo do Notion.

### 3.1 O Mecanismo: Embed via iframe

Notion Sites renderiza blocos de Embed como iframes. Isso significa que qualquer URL acessível
publicamente pode ser embutida dentro de uma página do Notion Site.

**Para embutir HTML self-contained, você precisa**:
1. Hospedar o arquivo HTML em algum lugar acessível via URL pública
2. Usar o bloco `/embed` no Notion apontando para essa URL

### 3.2 Onde Hospedar os HTMLs

| Opção | Custo | Complexidade | Ideal para |
|-------|-------|-------------|------------|
| **GitHub Pages** | Grátis | Baixa | Arquivos estáticos, versionados |
| **Netlify** | Grátis (tier básico) | Baixa | Deploy automático, CDN |
| **Vercel** | Grátis (tier básico) | Baixa | Deploy rápido, preview URLs |
| **Cloudflare Pages** | Grátis | Baixa | Performance global, CDN |
| **AWS S3 + CloudFront** | Centavos/mês | Média | Controle total, escala |
| **Google Cloud Storage** | Centavos/mês | Média | Integração com GCP |
| **Tiiny.host** | Grátis (limitado) | Mínima | Upload rápido de HTML único |
| **Surge.sh** | Grátis | Mínima | CLI simples para deploy |

**Recomendação para portal com múltiplos HTMLs**: GitHub Pages ou Netlify. Ambos são
gratuitos, suportam custom domains, e permitem organizar múltiplos arquivos numa estrutura
de pastas.

### 3.3 Padrão: GitHub Pages como CDN de HTMLs

Este é o setup mais prático para hospedar dezenas de páginas HTML:

**Estrutura do repositório**:
```
portal-htmls/
├── index.html          (opcional — listing page)
├── dashboards/
│   ├── vendas-q1.html
│   ├── marketing-2024.html
│   └── financeiro.html
├── reports/
│   ├── analise-mercado.html
│   └── pesquisa-clientes.html
└── tools/
    ├── calculadora-roi.html
    └── simulador-cenarios.html
```

**Ativar GitHub Pages**:
1. Settings → Pages → Source: Deploy from branch → `main` → `/root`
2. URL base será: `https://seuusuario.github.io/portal-htmls/`
3. Cada HTML é acessível: `https://seuusuario.github.io/portal-htmls/dashboards/vendas-q1.html`

**Custom domain no GitHub Pages** (opcional):
1. Adicione um arquivo `CNAME` com `portal.seudominio.com`
2. Configure DNS: CNAME de `portal.seudominio.com` para `seuusuario.github.io`
3. HTTPS é automático

### 3.4 Embutindo no Notion

Para cada HTML hospedado:
1. Na página do Notion, digite `/embed`
2. Cole a URL do HTML: `https://seuusuario.github.io/portal-htmls/dashboards/vendas-q1.html`
3. O Notion renderiza num iframe
4. **Ajuste o tamanho**: arraste as bordas do embed para definir largura e altura

**Dicas para embeds de HTML**:
- **Full-width**: use o toggle de "full width" na página do Notion para maximizar espaço
- **Altura**: HTMLs interativos (dashboards, calculadoras) precisam de bastante altura.
  Defina `min-height` no CSS do HTML para evitar scroll duplo.
- **Responsividade**: o iframe pode ter largura variável. Projete seus HTMLs com CSS
  responsivo (`width: 100%`, media queries).
- **Self-contained**: o HTML deve incluir TODO o CSS e JS inline. Dependências externas
  (CDN de bibliotecas) funcionam, mas links relativos entre HTMLs não funcionam dentro
  do iframe (cada embed é independente).

### 3.5 Otimizando HTMLs para Embed no Notion

Ao criar HTMLs que serão embutidos no Notion Sites, siga estas práticas:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard de Vendas</title>
  <style>
    /* Reset para iframe context */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      padding: 16px;
      /* Evitar scroll duplo — defina altura explícita ou use min-height */
      min-height: 600px;
    }
    /* Responsividade para iframe de largura variável */
    .container { max-width: 100%; margin: 0 auto; }
  </style>
</head>
<body>
  <div class="container">
    <!-- Conteúdo aqui -->
  </div>
  <script>
    // Todo JS inline — sem arquivos externos (exceto CDNs)
    // Comunicação com parent (Notion) não é possível via postMessage
  </script>
</body>
</html>
```

**Checklist para HTML embeddable**:
- CSS e JS inline (ou via CDN confiável)
- Sem dependências de arquivos relativos
- Responsivo (funciona em qualquer largura de iframe)
- Sem scroll horizontal
- Sem tentativa de acessar `parent` ou `window.top` (bloqueado por CORS)
- Fontes via Google Fonts ou system fonts (não fontes locais)
- Se usar bibliotecas, carregue via CDN (Chart.js, D3, Plotly, etc.)

### 3.6 Automatizando o Upload de HTMLs

Para portais com muitas páginas HTML, automatize o deploy:

**Via GitHub Actions** (deploy automático no push):
```yaml
# .github/workflows/deploy.yml
name: mjrp-notion-expert-sites-focus
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - uses: actions/deploy-pages@v4
```

**Via CLI** (Netlify):
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=./portal-htmls
```

### 3.7 Gerenciando um Catálogo de HTMLs com Database

Use uma database do Notion para organizar e rastrear todos os HTMLs do portal:

**Propriedades da database "Portal Pages"**:
| Propriedade | Tipo | Descrição |
|-------------|------|-----------|
| Name | Title | Nome da página/app |
| Category | Select | Categoria (Dashboard, Report, Tool, etc.) |
| HTML_URL | URL | Link direto para o HTML hospedado |
| Embed_Status | Status | Draft → Published → Archived |
| Last_Updated | Date | Quando o HTML foi atualizado por último |
| Description | Text | Descrição curta para o catálogo |
| Thumbnail | Files & Media | Imagem de preview para gallery view |
| Tags | Multi-select | Tags para filtragem |
| Owner | Person | Responsável |

**Gallery view como portal**: configure uma Gallery view desta database com a Thumbnail como
cover e o Name como título. Cada card linka para a página do Notion que contém o embed.

---

## 4. Notion API

A API do Notion permite automatizar a criação e gestão de conteúdo programaticamente.

### 4.1 Setup Inicial

1. Acesse `https://www.notion.so/my-integrations`
2. Crie uma nova integração (Internal Integration)
3. Copie o token (`secret_...`)
4. Nas páginas/databases que a integração precisa acessar, clique em "..." → "Connections"
   → adicione a integração

**Base URL**: `https://api.notion.com/v1/`

**Headers obrigatórios**:
```
Authorization: Bearer secret_xxxxx
Notion-Version: 2022-06-28
Content-Type: application/json
```

### 4.2 Endpoints Principais

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/pages` | POST | Criar nova página |
| `/pages/{id}` | GET | Ler propriedades de uma página |
| `/pages/{id}` | PATCH | Atualizar propriedades de uma página |
| `/databases/{id}/query` | POST | Consultar itens de uma database (com filtros e sorts) |
| `/databases/{id}` | GET | Ler schema de uma database |
| `/databases` | POST | Criar nova database |
| `/blocks/{id}/children` | GET | Ler blocos (conteúdo) de uma página |
| `/blocks/{id}/children` | PATCH | Adicionar blocos a uma página |
| `/blocks/{id}` | PATCH | Atualizar um bloco específico |
| `/blocks/{id}` | DELETE | Deletar um bloco |
| `/search` | POST | Buscar páginas e databases |
| `/users` | GET | Listar usuários do workspace |

### 4.3 Padrões Úteis para Gerenciar o Portal

**Criar uma nova página no portal com embed de HTML**:
```javascript
// Node.js com @notionhq/client
const { Client } = require('@notionhq/client');
const notion = new Client({ auth: 'secret_xxxxx' });

async function createPortalPage(databaseId, title, htmlUrl, category) {
  const response = await notion.pages.create({
    parent: { database_id: databaseId },
    properties: {
      Name: { title: [{ text: { content: title } }] },
      Category: { select: { name: category } },
      HTML_URL: { url: htmlUrl },
      Embed_Status: { status: { name: 'Published' } },
      Last_Updated: { date: { start: new Date().toISOString().split('T')[0] } }
    },
    // Adicionar o embed como conteúdo da página
    children: [
      {
        object: 'block',
        type: 'heading_2',
        heading_2: {
          rich_text: [{ text: { content: title } }]
        }
      },
      {
        object: 'block',
        type: 'embed',
        embed: { url: htmlUrl }
      }
    ]
  });
  return response;
}
```

**Listar todas as páginas publicadas do portal**:
```javascript
async function getPublishedPages(databaseId) {
  const response = await notion.databases.query({
    database_id: databaseId,
    filter: {
      property: 'Embed_Status',
      status: { equals: 'Published' }
    },
    sorts: [{ property: 'Last_Updated', direction: 'descending' }]
  });
  return response.results;
}
```

**Atualizar a URL de um HTML após re-deploy**:
```javascript
async function updateHtmlUrl(pageId, newUrl) {
  await notion.pages.update({
    page_id: pageId,
    properties: {
      HTML_URL: { url: newUrl },
      Last_Updated: { date: { start: new Date().toISOString().split('T')[0] } }
    }
  });
}
```

**Script de sync — publicar HTMLs novos automaticamente**:
```javascript
const fs = require('fs');
const path = require('path');

async function syncHtmlsToPortal(htmlDir, databaseId, baseUrl) {
  // Ler HTMLs existentes no portal
  const existingPages = await getPublishedPages(databaseId);
  const existingUrls = new Set(
    existingPages.map(p => p.properties.HTML_URL?.url).filter(Boolean)
  );

  // Escanear diretório de HTMLs
  const htmlFiles = fs.readdirSync(htmlDir, { recursive: true })
    .filter(f => f.endsWith('.html'));

  for (const file of htmlFiles) {
    const url = `${baseUrl}/${file}`;
    if (!existingUrls.has(url)) {
      const name = path.basename(file, '.html')
        .replace(/-/g, ' ')
        .replace(/\b\w/g, c => c.toUpperCase());
      const category = path.dirname(file) === '.' ? 'General' : path.dirname(file);

      console.log(`Creating portal page: ${name} → ${url}`);
      await createPortalPage(databaseId, name, url, category);
    }
  }
}
```

Para mais detalhes sobre a API e padrões avançados, veja `references/notion-api-and-integrations.md`.

---

## 5. Integrações e Automações

### 5.1 Zapier / Make (Integromat)

Conectam Notion a centenas de outros serviços sem código:

**Recipes úteis para portal**:
- Novo HTML no GitHub → cria página no Notion com embed (via webhook)
- Página do Notion muda para "Published" → tweet automático / post no Slack
- Form submission (Tally/Typeform) → cria item na database do portal
- Novo item na database → gera arquivo HTML a partir de template

### 5.2 Embeds de Terceiros

Além de HTMLs custom, Notion Sites suporta embeds nativos de:
- **Google Maps** — mapas interativos
- **Figma** — protótipos e designs
- **Miro / Mural** — boards colaborativos
- **Loom** — vídeos
- **Google Sheets / Docs / Slides** — documentos Google
- **Typeform / Tally** — formulários
- **CodePen / Replit** — código interativo
- **Excalidraw** — diagramas
- **Twitter / YouTube / Spotify** — mídia social
- **Qualquer URL** — via bloco `/embed` genérico (renderiza em iframe)

### 5.3 Google Analytics no Notion Sites

**Requer plano pago.**

1. No Notion, vá para Settings → Sites → selecione o site
2. Em "Analytics", adicione o Google Analytics Measurement ID (`G-XXXXXXXXXX`)
3. O tracking é aplicado automaticamente a todas as páginas publicadas
4. As páginas HTML embedadas não são trackadas pelo GA do Notion — se precisar,
   adicione o GA snippet dentro de cada HTML separadamente

### 5.4 SEO para Notion Sites

**Configurações por página**:
- Title: define o `<title>` da página (aparece na aba do browser e no Google)
- Description: define a meta description (aparece nos resultados de busca)
- Open Graph image: define a imagem de preview para redes sociais

**Boas práticas**:
- Use títulos descritivos e únicos para cada página
- Escreva descriptions de 150-160 caracteres
- Estruture conteúdo com headings (H1, H2, H3) — Notion mapeia para tags HTML corretas
- Use URLs limpas (baseadas no título — evite títulos muito longos)
- Habilite a indexação por motores de busca nas configurações do site
- Para pages com embeds de HTML: o conteúdo dentro do iframe não é indexado pelo Google.
  Adicione contexto/descrição em texto nativo do Notion acima/abaixo do embed.

---

## 6. Patterns para Portais

### 6.1 Portal de Dashboards

**Estrutura**:
- Home com gallery view da database de dashboards
- Cada card abre uma página com:
  - Breve descrição (texto Notion nativo — indexável por SEO)
  - Embed full-width do dashboard HTML
  - Metadados: última atualização, owner, fonte de dados

**Database properties**: Name, Category, HTML_URL, Thumbnail, Last_Updated, Data_Source,
Owner, Status

### 6.2 Portal de Documentação

**Estrutura**:
- Sidebar com hierarquia de categorias
- Páginas de conteúdo em Notion nativo (melhor para SEO e edição)
- Componentes interativos (calculadoras, simuladores) como embeds de HTML
- Versioning via propriedade "Version" na database

### 6.3 Portal de Ferramentas Internas

**Estrutura**:
- Gallery com cards visuais para cada ferramenta
- Cada ferramenta é um HTML self-contained (calculadora, gerador, visualizador)
- Database para gerenciar: nome, descrição, URL, tags, status de manutenção
- Página "Solicitar Nova Ferramenta" com embed de Tally/Typeform

### 6.4 Blog / Newsletter

**Estrutura**:
- Database de posts com propriedades: Title, Date, Author, Tags, Cover, Status
- Gallery ou List view como homepage do blog
- Cada post é uma página Notion com conteúdo nativo (ótimo para SEO)
- Rich embeds para mídia: vídeos, tweets, código interativo

---

## 7. Troubleshooting

**Embed não carrega**: Verifique se a URL é HTTPS (HTTP não funciona). Verifique se o
servidor do HTML permite iframe embedding (header `X-Frame-Options` não pode ser `DENY`).

**Embed mostra muito pequeno**: Ajuste a altura arrastando a borda inferior do bloco de
embed. No HTML, defina `min-height` no body.

**Scroll duplo (iframe + página)**: No HTML embeddado, use `overflow: hidden` no body ou
defina altura fixa. Idealmente, o HTML deve ter altura suficiente para mostrar todo o
conteúdo sem scroll interno.

**Conteúdo do embed não indexado pelo Google**: Correto — conteúdo dentro de iframes não
é indexado. Adicione um resumo textual na página do Notion acima do embed para SEO.

**Custom domain não funciona**: Verifique o DNS: deve ser um CNAME apontando para
`external.notion.site.` (com ponto final). O host deve ser um subdomain (ex: `www`, não
domínio raiz). Verifique o registro TXT de verificação. Se usar Cloudflare, desabilite o
proxy (modo DNS only / ícone cinza). Aguarde propagação DNS (até 48h).

**Página publicada mostra conteúdo desatualizado**: Notion Sites tem cache. Aguarde alguns
minutos ou force refresh. Se o problema persistir, despublicar e republicar.

**API retorna 403**: A integração não tem acesso à página/database. Vá na página → "..." →
"Connections" → adicione a integração.

**Notion Site lento**: Reduza o número de blocos por página (mantenha <100). Evite databases
muito grandes em views inline. Use sub-páginas para dividir conteúdo pesado.
