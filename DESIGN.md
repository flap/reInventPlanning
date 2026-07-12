# 🏗️ Design Document — TripEvent Planner

> Documento de design técnico para o sistema TripEvent Planner.
> Baseado na especificação [`SPEC.md`](./SPEC.md).

---

## 1. Resumo Executivo

### 1.1 Objetivo deste Documento

Definir a arquitetura técnica, stack, estrutura de projeto e estratégia de deploy para o TripEvent Planner — um sistema de planejamento de viagens e eventos para brasileiros.

### 1.2 Decisões de Stack

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| Frontend | **Vue.js 3** (Composition API) | Reativo, leve (~33KB), ecossistema maduro, curva de aprendizado suave |
| Build Tool | **Vite** | Build rápido, HMR instantâneo, suporte nativo a Vue 3 |
| Roteamento | **Vue Router** | SPA com navegação por hash (compatível com GitHub Pages) |
| Estado | **Pinia** | Store oficial do Vue 3, leve, TypeScript-friendly |
| Estilo | **Tailwind CSS** | Utility-first, purge automático, responsivo |
| Conteúdo | **Markdown** (via vite-plugin-md ou frontmatter) | Guias existentes reutilizados como fonte de dados |
| Backend (Fase 2+) | **Python + FastAPI** | Async, tipado, auto-documentado (OpenAPI), ideal para APIs REST |
| Deploy Fase 1 | **GitHub Pages** (static SPA) | Gratuito, CI/CD integrado, sem infra para gerenciar |

### 1.3 Escopo por Fase

| Fase | Frontend | Backend | Deploy |
|------|----------|---------|--------|
| **Fase 1** | Vue.js SPA (static build) | ❌ Nenhum | GitHub Pages |
| **Fase 2** | Vue.js SPA + PWA | FastAPI (opções externas: câmbio, clima) | GitHub Pages + API separada |
| **Fase 3** | Vue.js SPA + auth | FastAPI + DynamoDB | CloudFront + S3 / API Gateway |

---

## 2. Estratégia de Deploy — GitHub Pages (Fase 1)

### 2.1 O Desafio

GitHub Pages serve apenas arquivos estáticos. Uma SPA Vue.js precisa:
1. Ser buildada em arquivos HTML/CSS/JS estáticos
2. Lidar com roteamento client-side (sem 404 em refresh)
3. Manter URLs amigáveis mesmo sem server-side routing

### 2.2 Solução: Hash-based Routing + Static Build

```
Vue.js App (dev)
    │
    ▼  [vite build]
dist/
├── index.html          ← Entry point único
├── assets/
│   ├── index-[hash].js ← Bundle JS (code-split por rota)
│   ├── index-[hash].css← CSS purged
│   └── ...chunks...
└── 404.html            ← Cópia do index.html (SPA fallback)
    │
    ▼  [GitHub Actions]
GitHub Pages (https://usuario.github.io/reInventPlanning/)
```

**Roteamento com hash mode:**
```
https://usuario.github.io/reInventPlanning/#/evento
https://usuario.github.io/reInventPlanning/#/hoteis
https://usuario.github.io/reInventPlanning/#/checklist
```

Isso elimina o problema de 404 no refresh — o servidor sempre entrega `index.html` e o Vue Router resolve a rota pelo hash.

### 2.3 Alternativa Considerada: History Mode + 404 Fallback

```
# Com 404.html como cópia do index.html
# URLs "limpas": /reInventPlanning/evento
# Problema: GitHub Pages retorna 404 status code antes de redirecionar
# SEO: prejudicado pelo status 404
```

**Decisão:** Usar **hash mode** na Fase 1 por simplicidade e confiabilidade. Migrar para history mode quando mover para CloudFront + S3 (Fase 3).

### 2.4 Configuração do Vite para GitHub Pages

```typescript
// vite.config.ts
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/reInventPlanning/', // subpath do GitHub Pages
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  }
})
```

### 2.5 GitHub Actions — CI/CD

```yaml
# .github/workflows/deploy.yml
name: Deploy Vue.js to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: npm ci
        working-directory: frontend

      - name: Build
        run: npm run build
        working-directory: frontend

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: frontend/dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 3. Arquitetura Geral

### 3.1 Fase 1 — SPA Estática no GitHub Pages

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Pages                               │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   Vue.js 3 SPA                            │   │
│  │                                                            │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────┐  │   │
│  │  │ Vue Router │  │   Pinia    │  │  Service Worker    │  │   │
│  │  │ (hash mode)│  │  (stores)  │  │  (cache offline)   │  │   │
│  │  └────────────┘  └────────────┘  └────────────────────┘  │   │
│  │                                                            │   │
│  │  ┌────────────────────────────────────────────────────┐   │   │
│  │  │              Componentes / Views                     │   │   │
│  │  │  Home · Evento · Hotéis · Voos · Clima · Turismo   │   │   │
│  │  │  Checklist · Timeline · Orçamento                   │   │   │
│  │  └────────────────────────────────────────────────────┘   │   │
│  │                                                            │   │
│  │  ┌────────────────────────────────────────────────────┐   │   │
│  │  │              Camada de Dados                         │   │   │
│  │  │  JSON estático · Markdown parsed · localStorage     │   │   │
│  │  └────────────────────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Fase 2+ — Com Backend FastAPI

```
┌──────────────┐          ┌───────────────────────┐
│  Vue.js SPA  │──HTTPS──▶│  FastAPI Backend      │
│  (GitHub     │◀─────────│                       │
│   Pages)     │          │  /api/v1/             │
└──────────────┘          │  ├── cambio/          │
       │                  │  ├── clima/           │
       │                  │  ├── usuarios/        │
       ▼                  │  └── viagens/         │
┌──────────────┐          └───────────┬───────────┘
│  Service     │                      │
│  Worker      │                      ▼
│  (offline)   │          ┌───────────────────────┐
└──────────────┘          │  DynamoDB / PostgreSQL │
                          └───────────────────────┘
                                      │
                          ┌───────────┴───────────┐
                          ▼                       ▼
                  ┌──────────────┐      ┌──────────────┐
                  │  APIs Ext.   │      │  Cache       │
                  │  Câmbio/Clima│      │  (Redis)     │
                  └──────────────┘      └──────────────┘
```

### 3.3 Separação de Responsabilidades

| Camada | Fase 1 (sem backend) | Fase 2+ (com backend) |
|--------|---------------------|----------------------|
| Conteúdo estático (guias) | JSON/MD compilado no build | Idem (não muda) |
| Estado do usuário | localStorage + Pinia | API /usuarios + Pinia (sync) |
| Dados dinâmicos (câmbio, clima) | Hardcoded / links externos | API /cambio, /clima |
| Checklist/progresso | localStorage | API /viagens/{id}/checklist |
| Orçamento | Cálculos client-side | Cálculos client-side + API para salvar |

---

## 4. Estrutura do Projeto

### 4.1 Monorepo — Visão Geral

```
reInventPlanning/
├── README.md
├── SPEC.md
├── DESIGN.md
│
├── frontend/                    ← Vue.js App
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── index.html               ← Entry point
│   ├── public/
│   │   ├── favicon.ico
│   │   └── manifest.json        ← PWA manifest
│   ├── src/
│   │   ├── main.ts              ← Bootstrap do app
│   │   ├── App.vue              ← Root component
│   │   ├── router/
│   │   │   └── index.ts         ← Definição de rotas
│   │   ├── stores/
│   │   │   ├── checklist.ts     ← Pinia store: checklist
│   │   │   ├── budget.ts        ← Pinia store: orçamento
│   │   │   ├── trip.ts          ← Pinia store: viagem do usuário
│   │   │   └── content.ts       ← Pinia store: conteúdo/guias
│   │   ├── views/
│   │   │   ├── HomeView.vue
│   │   │   ├── EventoView.vue
│   │   │   ├── HoteisView.vue
│   │   │   ├── VoosView.vue
│   │   │   ├── ClimaView.vue
│   │   │   ├── TurismoView.vue
│   │   │   ├── ChecklistView.vue
│   │   │   ├── TimelineView.vue
│   │   │   └── OrcamentoView.vue
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── AppHeader.vue
│   │   │   │   ├── AppFooter.vue
│   │   │   │   ├── AppSidebar.vue
│   │   │   │   └── AppNav.vue
│   │   │   ├── shared/
│   │   │   │   ├── ProgressBar.vue
│   │   │   │   ├── PriorityBadge.vue
│   │   │   │   ├── CurrencyDisplay.vue
│   │   │   │   ├── CardGrid.vue
│   │   │   │   └── MarkdownRenderer.vue
│   │   │   ├── evento/
│   │   │   │   ├── SessionTypeCard.vue
│   │   │   │   ├── WeekSchedule.vue
│   │   │   │   └── VenueMap.vue
│   │   │   ├── hoteis/
│   │   │   │   ├── HotelCard.vue
│   │   │   │   ├── HotelComparator.vue
│   │   │   │   └── ShuttleRoutes.vue
│   │   │   ├── checklist/
│   │   │   │   ├── ChecklistCategory.vue
│   │   │   │   ├── ChecklistItem.vue
│   │   │   │   └── ChecklistProgress.vue
│   │   │   ├── timeline/
│   │   │   │   ├── TimelineTrack.vue
│   │   │   │   ├── MilestoneCard.vue
│   │   │   │   └── TimelineStatus.vue
│   │   │   └── orcamento/
│   │   │       ├── BudgetCalculator.vue
│   │   │       ├── BudgetBreakdown.vue
│   │   │       ├── ScenarioSelector.vue
│   │   │       └── CurrencyConverter.vue
│   │   ├── composables/
│   │   │   ├── useLocalStorage.ts
│   │   │   ├── useCurrency.ts
│   │   │   ├── useMarkdown.ts
│   │   │   └── useOffline.ts
│   │   ├── data/
│   │   │   ├── eventos/
│   │   │   │   └── reinvent-2025.json
│   │   │   ├── destinos/
│   │   │   │   └── las-vegas.json
│   │   │   ├── hoteis.json
│   │   │   ├── checklist-items.json
│   │   │   ├── timeline-milestones.json
│   │   │   └── budget-defaults.json
│   │   ├── content/
│   │   │   ├── sobre-o-evento.md
│   │   │   ├── hoteis-hospedagem.md
│   │   │   ├── voos-deslocamento.md
│   │   │   ├── clima-vestuario.md
│   │   │   └── turismo-compras.md
│   │   ├── types/
│   │   │   ├── evento.ts
│   │   │   ├── destino.ts
│   │   │   ├── hotel.ts
│   │   │   ├── checklist.ts
│   │   │   └── budget.ts
│   │   └── assets/
│   │       ├── styles/
│   │       │   └── main.css        ← Tailwind imports
│   │       └── images/
│   └── tests/
│       ├── unit/
│       └── e2e/
│
├── backend/                     ← FastAPI (Fase 2+)
│   ├── pyproject.toml
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              ← FastAPI app entry
│   │   ├── config.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── cambio.py
│   │   │   ├── clima.py
│   │   │   ├── usuarios.py
│   │   │   └── viagens.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── usuario.py
│   │   │   ├── viagem.py
│   │   │   └── checklist.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── cambio.py
│   │   │   ├── viagem.py
│   │   │   └── usuario.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── cambio_service.py
│   │   │   ├── clima_service.py
│   │   │   └── viagem_service.py
│   │   └── db/
│   │       ├── __init__.py
│   │       └── dynamodb.py
│   └── tests/
│       ├── __init__.py
│       ├── test_cambio.py
│       └── test_viagens.py
│
├── docs/                        ← Guias originais (preservados)
│   └── guias/
│       ├── 01-sobre-o-evento.md
│       ├── 02-hoteis-hospedagem.md
│       ├── 03-voos-deslocamento.md
│       ├── 04-clima-vestuario.md
│       └── 05-turismo-compras.md
│
└── .github/
    └── workflows/
        └── deploy.yml           ← Build Vue + Deploy GitHub Pages
```

---

## 5. Componentes Vue.js — Design Detalhado

### 5.1 Roteamento

```typescript
// src/router/index.ts
import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  { path: '/evento', name: 'evento', component: () => import('@/views/EventoView.vue') },
  { path: '/hoteis', name: 'hoteis', component: () => import('@/views/HoteisView.vue') },
  { path: '/voos', name: 'voos', component: () => import('@/views/VoosView.vue') },
  { path: '/clima', name: 'clima', component: () => import('@/views/ClimaView.vue') },
  { path: '/turismo', name: 'turismo', component: () => import('@/views/TurismoView.vue') },
  { path: '/checklist', name: 'checklist', component: () => import('@/views/ChecklistView.vue') },
  { path: '/timeline', name: 'timeline', component: () => import('@/views/TimelineView.vue') },
  { path: '/orcamento', name: 'orcamento', component: () => import('@/views/OrcamentoView.vue') },
]

export default createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})
```

### 5.2 Layout Principal

```
┌─────────────────────────────────────────────┐
│  AppHeader (logo, nav principal, progresso) │
├─────────┬───────────────────────────────────┤
│         │                                   │
│  App    │         <router-view>             │
│  Nav    │                                   │
│  (móvel:│    Conteúdo da view ativa         │
│  bottom │                                   │
│  bar)   │                                   │
│         │                                   │
├─────────┴───────────────────────────────────┤
│  AppFooter (links, créditos)                │
└─────────────────────────────────────────────┘
```

**Responsividade:**
- Desktop (≥1024px): sidebar lateral com navegação
- Tablet (768–1023px): header com nav colapsável
- Mobile (<768px): bottom navigation bar (5 ícones principais)

### 5.3 Hierarquia de Componentes por Feature

#### Home (Landing)
```
HomeView
├── HeroSection          → Banner com nome do evento e CTA
├── ProgressOverview     → Progresso geral do planejamento
├── QuickActions         → Cards com ações rápidas (checklist, orçamento)
├── TimelinePreview      → Próximos marcos da timeline
└── GuideCards           → Grid com links para cada guia
```

#### Evento
```
EventoView
├── EventHeader          → Nome, datas, local com banner visual
├── SessionTypeGrid      → Grid de tipos de sessão (KEY, BLD, WRK...)
│   └── SessionTypeCard  → Card individual com ícone, descrição, dicas
├── DepthLevels          → Explicação dos níveis 100-400
├── WeekSchedule         → Cronograma dia a dia do evento
│   └── DayColumn        → Coluna com atividades do dia
├── VenueMap             → Mapa esquemático dos venues
├── TipsList             → Dicas organizadas (antes/durante/networking)
└── UsefulLinks          → Links externos (site, app, YouTube)
```

#### Hotéis
```
HoteisView
├── HotelFilters         → Filtros: orçamento, distância, nível
├── HotelGrid            → Grid de hotéis filtrados
│   └── HotelCard        → Card com foto, preço, distância, rating
├── HotelComparator      → Tabela comparativa (seleção de 2-3 hotéis)
├── CostCalculator       → Calculadora: diárias + resort fee + gorjeta
├── ShuttleRoutes        → Mapa/tabela de rotas de shuttle
└── BookingTips          → Dicas de reserva em accordion
```

#### Checklist
```
ChecklistView
├── ChecklistProgress    → Barra de progresso global + stats
├── CategoryTabs         → Abas por categoria
│   └── ChecklistCategory → Lista de itens da categoria
│       └── ChecklistItem → Item individual (checkbox, prioridade, notas)
├── ChecklistActions     → Botões: reset, exportar, filtrar por pendentes
└── SmartSuggestions     → Sugestões baseadas na timeline (o que fazer agora)
```

#### Orçamento
```
OrcamentoView
├── ScenarioSelector     → Toggle: Econômico / Confortável / Luxo
├── BudgetCalculator     → Formulário interativo de inputs
│   ├── FlightSection    → Custo de passagem
│   ├── HotelSection     → Diárias × noites + resort fee
│   ├── EventSection     → Ingresso do evento
│   ├── FoodSection      → Alimentação × dias
│   ├── TransportSection → Uber, shuttle, monorail
│   ├── TourismSection   → Atrações e compras
│   └── ExtrasSection    → Seguro, chip, extras
├── BudgetBreakdown      → Gráfico de pizza / barras por categoria
├── CurrencyConverter    → BRL ↔ USD com taxa + IOF
├── TaxInfo              → Sales tax + resort fee info
└── SavingTips           → Dicas de economia por categoria
```

### 5.4 Componentes Compartilhados (Design System)

| Componente | Uso | Props principais |
|-----------|-----|-----------------|
| `ProgressBar` | Progresso visual (checklist, geral) | `value`, `max`, `color`, `label` |
| `PriorityBadge` | Indicador de prioridade | `level: 'alta' \| 'media' \| 'baixa'` |
| `CurrencyDisplay` | Exibição de valores USD/BRL | `amount`, `currency`, `showConversion` |
| `CardGrid` | Layout responsivo de cards | `columns`, `gap` |
| `MarkdownRenderer` | Renderiza conteúdo markdown | `content`, `class` |
| `CollapsibleSection` | Seção expansível (accordion) | `title`, `defaultOpen` |
| `InfoTooltip` | Tooltip com informação extra | `text`, `position` |
| `StatusChip` | Chip de status (pendente, feito) | `status`, `size` |

---

## 6. Gerenciamento de Estado (Pinia)

### 6.1 Stores

#### `stores/trip.ts` — Estado principal da viagem

```typescript
interface TripState {
  eventoId: string              // 'reinvent-2025'
  destinoId: string             // 'las-vegas'
  dataIda: string | null
  dataVolta: string | null
  hotelSelecionado: string | null
  statusVisto: 'pendente' | 'agendado' | 'aprovado' | 'negado'
  statusPassagem: 'pesquisando' | 'comprada' | null
  acompanhantes: number
}
```

#### `stores/checklist.ts` — Checklist com persistência

```typescript
interface ChecklistState {
  items: Record<string, ChecklistItemState>  // id → estado
  lastUpdated: string
}

interface ChecklistItemState {
  completed: boolean
  completedAt: string | null
  notes: string
}

// Ações
// toggleItem(id) → marca/desmarca + salva localStorage
// resetAll() → limpa progresso
// getProgress() → computed: { total, completed, percentage }
// getByCategory(cat) → computed: items filtrados
```

#### `stores/budget.ts` — Orçamento interativo

```typescript
interface BudgetState {
  scenario: 'economico' | 'confortavel' | 'luxo'
  inputs: {
    passagem: number
    hotelDiaria: number
    noites: number
    resortFee: number
    ingresso: number
    alimentacaoDia: number
    dias: number
    transporte: number
    turismo: number
    seguro: number
    chip: number
    extras: number
  }
  taxaUSD: number              // Taxa de câmbio
  iof: number                  // 4.38% ou 1.1%
}

// Computed
// totalUSD → soma de todos os inputs
// totalBRL → totalUSD × taxaUSD × (1 + iof)
// breakdown → objeto por categoria com percentuais
```

#### `stores/content.ts` — Conteúdo dos guias

```typescript
interface ContentState {
  guides: Record<string, GuideContent>  // slug → conteúdo parseado
  loaded: boolean
}

// Carrega JSON/markdown compilado no build time
// Sem necessidade de API — dados estáticos
```

### 6.2 Persistência (localStorage)

```typescript
// composables/useLocalStorage.ts
// Wrapper que sincroniza Pinia stores com localStorage

// Stores persistidos:
// - checklist → 'tripevent:checklist'
// - budget → 'tripevent:budget'
// - trip → 'tripevent:trip'

// Stores NÃO persistidos (estáticos, carregados do build):
// - content
```

### 6.3 Fluxo de Dados (Fase 1)

```
┌──────────────┐    build-time     ┌──────────────┐
│  Markdown    │──────────────────▶│  JSON/HTML   │
│  (guias)     │  vite-plugin-md   │  (importado) │
└──────────────┘                   └──────┬───────┘
                                          │
                                          ▼
┌──────────────┐    import         ┌──────────────┐
│  JSON Data   │──────────────────▶│  Pinia Store │
│  (hoteis,    │                   │  (content)   │
│   checklist) │                   └──────┬───────┘
└──────────────┘                          │
                                          ▼
                                   ┌──────────────┐
                                   │  Vue         │
                                   │  Components  │
                                   └──────┬───────┘
                                          │
           ┌──────────────────────────────┼──────────────┐
           ▼                              ▼              ▼
    ┌──────────────┐            ┌──────────────┐  ┌──────────────┐
    │  Leitura     │            │  Interação   │  │  Cálculos    │
    │  (renderiza  │            │  (checklist  │  │  (orçamento  │
    │   conteúdo)  │            │   toggle)    │  │   converter) │
    └──────────────┘            └──────┬───────┘  └──────────────┘
                                       │
                                       ▼
                                ┌──────────────┐
                                │ localStorage │
                                │ (persistir)  │
                                └──────────────┘
```

---

## 7. Conteúdo Estático — Estratégia de Dados

### 7.1 Fontes de Dados

| Tipo | Formato | Onde mora | Carregamento |
|------|---------|-----------|-------------|
| Guias (texto longo) | Markdown | `src/content/*.md` | Build-time (importado como HTML) |
| Dados estruturados (hotéis, sessões) | JSON | `src/data/*.json` | Build-time (importado como objeto) |
| Checklist items | JSON | `src/data/checklist-items.json` | Build-time |
| Budget defaults por cenário | JSON | `src/data/budget-defaults.json` | Build-time |
| Timeline milestones | JSON | `src/data/timeline-milestones.json` | Build-time |
| Imagens/ícones | PNG/SVG | `src/assets/images/` | Build-time (hashed) |

### 7.2 Exemplo: `src/data/hoteis.json`

```json
[
  {
    "id": "venetian",
    "nome": "The Venetian Resort",
    "endereco": "3355 S Las Vegas Blvd, Las Vegas, NV 89109",
    "venue": true,
    "distanciaVenetian": "No local",
    "distanciaMinutos": 0,
    "distanciaCategoria": "verde",
    "precoMin": 250,
    "precoMax": 450,
    "nivel": 5,
    "resortFee": 45,
    "destaques": ["Venue principal do re:Invent", "Expo Hall, labs e maioria das sessões"],
    "dica": "Reserve pelo site da AWS para tarifas especiais de grupo"
  }
]
```

### 7.3 Exemplo: `src/data/checklist-items.json`

```json
[
  {
    "id": "doc-001",
    "categoria": "documentacao",
    "texto": "Verificar validade do passaporte (mínimo 6 meses além da volta)",
    "prioridade": "alta",
    "timelineMes": -9,
    "detalhes": "O passaporte deve estar válido por pelo menos 6 meses após a data de retorno ao Brasil."
  },
  {
    "id": "doc-002",
    "categoria": "documentacao",
    "texto": "Solicitar visto americano B1/B2",
    "prioridade": "alta",
    "timelineMes": -6,
    "detalhes": "Preencher DS-160 online, agendar entrevista no consulado."
  }
]
```

### 7.4 Exemplo: `src/data/budget-defaults.json`

```json
{
  "cenarios": {
    "economico": {
      "passagem": 4500,
      "hotelDiaria": 80,
      "noites": 7,
      "resortFee": 35,
      "ingresso": 1800,
      "alimentacaoDia": 40,
      "dias": 7,
      "transporte": 100,
      "turismo": 150,
      "seguro": 200,
      "chip": 25,
      "extras": 100
    },
    "confortavel": {
      "passagem": 7000,
      "hotelDiaria": 200,
      "noites": 8,
      "resortFee": 45,
      "ingresso": 2100,
      "alimentacaoDia": 70,
      "dias": 8,
      "transporte": 200,
      "turismo": 400,
      "seguro": 350,
      "chip": 30,
      "extras": 200
    },
    "luxo": {
      "passagem": 12000,
      "hotelDiaria": 400,
      "noites": 9,
      "resortFee": 50,
      "ingresso": 2100,
      "alimentacaoDia": 120,
      "dias": 9,
      "transporte": 400,
      "turismo": 800,
      "seguro": 500,
      "chip": 50,
      "extras": 500
    }
  },
  "taxas": {
    "salesTaxNevada": 0.08375,
    "iofCartao": 0.0438,
    "iofCompraInternacional": 0.011
  }
}
```

### 7.5 Markdown como Conteúdo — Plugin Vite

```typescript
// vite.config.ts (com plugin para markdown)
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Markdown from 'unplugin-vue-markdown/vite'

export default defineConfig({
  plugins: [
    vue({
      include: [/\.vue$/, /\.md$/]
    }),
    Markdown({
      markdownItOptions: {
        html: true,
        linkify: true,
        typographer: true
      }
    })
  ],
  base: '/reInventPlanning/'
})
```

Os arquivos `.md` em `src/content/` podem ser importados diretamente como componentes Vue ou como strings HTML pré-processadas no build.

---

## 8. Backend — Python + FastAPI (Fase 2+)

### 8.1 Quando o Backend Entra

O backend **não existe na Fase 1**. Ele é introduzido quando as seguintes necessidades surgirem:

| Necessidade | Gatilho | Endpoint |
|------------|---------|----------|
| Câmbio em tempo real | Usuários pedem cotação atualizada | `GET /api/v1/cambio` |
| Clima atualizado | Previsão para datas do evento | `GET /api/v1/clima/{cidade}` |
| Conta de usuário | Sincronizar progresso entre dispositivos | `POST /api/v1/auth/*` |
| Salvar planejamento | Persistir viagem no servidor | `CRUD /api/v1/viagens` |
| Notificações | Alertas de prazos por email | Worker async |

### 8.2 Estrutura do Backend

```
backend/
├── pyproject.toml               ← Dependências (Poetry/uv)
├── Dockerfile
├── app/
│   ├── __init__.py
│   ├── main.py                  ← FastAPI app + middleware
│   ├── config.py                ← Settings com Pydantic
│   ├── dependencies.py          ← Dependency injection
│   │
│   ├── routers/                 ← Endpoints organizados por domínio
│   │   ├── __init__.py
│   │   ├── cambio.py            ← Cotação USD/BRL
│   │   ├── clima.py             ← Previsão do tempo
│   │   ├── auth.py              ← Registro/login
│   │   ├── usuarios.py          ← Perfil do usuário
│   │   └── viagens.py           ← CRUD de viagens + checklist
│   │
│   ├── schemas/                 ← Pydantic models (request/response)
│   │   ├── __init__.py
│   │   ├── cambio.py
│   │   ├── clima.py
│   │   ├── usuario.py
│   │   └── viagem.py
│   │
│   ├── models/                  ← Modelos de domínio / DB
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── viagem.py
│   │   └── checklist.py
│   │
│   ├── services/                ← Lógica de negócio
│   │   ├── __init__.py
│   │   ├── cambio_service.py    ← Integração API câmbio (BCB/AwesomeAPI)
│   │   ├── clima_service.py     ← Integração OpenWeatherMap
│   │   └── viagem_service.py    ← Lógica de planejamento
│   │
│   └── db/                      ← Camada de persistência
│       ├── __init__.py
│       ├── dynamodb.py          ← Cliente DynamoDB
│       └── repository.py        ← Padrão repository
│
└── tests/
    ├── conftest.py
    ├── test_cambio.py
    ├── test_clima.py
    └── test_viagens.py
```

### 8.3 Configuração Base

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cambio, clima, auth, usuarios, viagens
from app.config import settings

app = FastAPI(
    title="TripEvent Planner API",
    version="0.1.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cambio.router, prefix="/api/v1/cambio", tags=["Câmbio"])
app.include_router(clima.router, prefix="/api/v1/clima", tags=["Clima"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["Usuários"])
app.include_router(viagens.router, prefix="/api/v1/viagens", tags=["Viagens"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
```

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "TripEvent Planner API"
    debug: bool = False
    
    # CORS
    cors_origins: list[str] = ["https://usuario.github.io"]
    
    # DynamoDB
    dynamodb_table_prefix: str = "tripevent"
    aws_region: str = "us-east-1"
    
    # APIs externas
    awesome_api_url: str = "https://economia.awesomeapi.com.br"
    openweather_api_key: str = ""
    
    # Auth
    jwt_secret: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440  # 24h

    class Config:
        env_file = ".env"

settings = Settings()
```

### 8.4 Dependências Python

```toml
# pyproject.toml
[project]
name = "tripevent-backend"
version = "0.1.0"
requires-python = ">=3.12"

dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.5.0",
    "httpx>=0.27.0",           # HTTP client async
    "boto3>=1.35.0",           # AWS SDK
    "python-jose[cryptography]>=3.3.0",  # JWT
    "passlib[bcrypt]>=1.7.4",  # Password hashing
    "mangum>=0.17.0",          # Lambda adapter
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.27.0",           # TestClient
    "ruff>=0.6.0",
    "mypy>=1.11.0",
]
```

---

## 9. API Design

### 9.1 Endpoints

#### Câmbio (público, sem auth)

```
GET /api/v1/cambio
  → { "USD_BRL": 5.42, "updated_at": "2025-10-15T14:30:00Z" }

GET /api/v1/cambio/historico?dias=30
  → [{ "data": "2025-10-01", "valor": 5.38 }, ...]
```

#### Clima (público, sem auth)

```
GET /api/v1/clima/las-vegas?data_inicio=2025-12-01&data_fim=2025-12-06
  → {
      "cidade": "Las Vegas",
      "previsao": [
        { "data": "2025-12-01", "min": 3, "max": 15, "umidade": 18, "condicao": "ensolarado" }
      ]
    }
```

#### Auth

```
POST /api/v1/auth/registro
  Body: { "email": "...", "senha": "...", "nome": "..." }
  → { "token": "...", "usuario": {...} }

POST /api/v1/auth/login
  Body: { "email": "...", "senha": "..." }
  → { "token": "...", "usuario": {...} }
```

#### Viagens (requer auth)

```
GET    /api/v1/viagens              → Lista viagens do usuário
POST   /api/v1/viagens              → Cria nova viagem
GET    /api/v1/viagens/{id}         → Detalhes da viagem
PUT    /api/v1/viagens/{id}         → Atualiza viagem
DELETE /api/v1/viagens/{id}         → Remove viagem

GET    /api/v1/viagens/{id}/checklist     → Progresso do checklist
PUT    /api/v1/viagens/{id}/checklist     → Atualiza checklist (sync)

GET    /api/v1/viagens/{id}/orcamento     → Orçamento salvo
PUT    /api/v1/viagens/{id}/orcamento     → Atualiza orçamento
```

### 9.2 Schemas (Pydantic)

```python
# schemas/viagem.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class ViagemBase(BaseModel):
    evento_id: str
    destino_id: str
    data_ida: Optional[date] = None
    data_volta: Optional[date] = None
    hotel_id: Optional[str] = None
    acompanhantes: int = 0

class ViagemCreate(ViagemBase):
    pass

class ViagemResponse(ViagemBase):
    id: str
    usuario_id: str
    status_visto: str = "pendente"
    status_passagem: Optional[str] = None
    created_at: str
    updated_at: str

class ChecklistSync(BaseModel):
    items: dict[str, "ChecklistItemState"]
    last_updated: str

class ChecklistItemState(BaseModel):
    completed: bool = False
    completed_at: Optional[str] = None
    notes: str = ""
```

```python
# schemas/cambio.py
from pydantic import BaseModel

class CambioResponse(BaseModel):
    moeda_origem: str = "USD"
    moeda_destino: str = "BRL"
    valor: float
    variacao_24h: float
    updated_at: str

class CambioHistorico(BaseModel):
    data: str
    valor: float
```

### 9.3 Exemplo de Router

```python
# routers/cambio.py
from fastapi import APIRouter, HTTPException
from app.schemas.cambio import CambioResponse, CambioHistorico
from app.services.cambio_service import CambioService

router = APIRouter()
service = CambioService()


@router.get("/", response_model=CambioResponse)
async def get_cotacao_atual():
    """Retorna cotação atual USD → BRL."""
    cotacao = await service.get_cotacao_atual()
    if not cotacao:
        raise HTTPException(status_code=503, detail="Serviço de câmbio indisponível")
    return cotacao


@router.get("/historico", response_model=list[CambioHistorico])
async def get_historico(dias: int = 30):
    """Retorna histórico de cotação dos últimos N dias."""
    if dias > 90:
        raise HTTPException(status_code=400, detail="Máximo 90 dias")
    return await service.get_historico(dias)
```

### 9.4 Integração Frontend ↔ Backend

```typescript
// frontend/src/services/api.ts
const API_BASE = import.meta.env.VITE_API_URL || ''

export const api = {
  async getCambio(): Promise<CambioResponse> {
    // Fase 1: retorna valor hardcoded
    // Fase 2+: chama API real
    if (!API_BASE) {
      return { moeda_origem: 'USD', moeda_destino: 'BRL', valor: 5.40, variacao_24h: 0, updated_at: '' }
    }
    const res = await fetch(`${API_BASE}/api/v1/cambio`)
    return res.json()
  }
}
```

Na Fase 1 (sem backend), o frontend usa valores default. Na Fase 2+, a variável `VITE_API_URL` aponta para a API real.

---

## 10. Modelo de Dados (Persistência)

### 10.1 Fase 1 — localStorage

```
localStorage keys:
├── tripevent:trip          → JSON do TripState (hotel, datas, status)
├── tripevent:checklist     → JSON do ChecklistState (items com estado)
├── tripevent:budget        → JSON do BudgetState (inputs, cenário)
└── tripevent:preferences   → JSON de preferências (tema, idioma)
```

### 10.2 Fase 2+ — DynamoDB

**Tabela: `tripevent-usuarios`**

| PK | SK | Atributos |
|----|-----|-----------|
| `USER#email` | `PROFILE` | nome, email, hashed_password, created_at |
| `USER#email` | `VIAGEM#uuid` | evento_id, destino_id, datas, hotel, status |
| `USER#email` | `VIAGEM#uuid#CHECKLIST` | items: {...}, last_updated |
| `USER#email` | `VIAGEM#uuid#BUDGET` | scenario, inputs: {...}, last_updated |

**Single-table design** — uma tabela DynamoDB serve todas as entidades, usando PK/SK compostos.

**Tabela: `tripevent-cache`** (TTL para dados externos)

| PK | SK | TTL | Atributos |
|----|-----|-----|-----------|
| `CAMBIO` | `USD_BRL` | +1h | valor, variacao, source |
| `CLIMA#las-vegas` | `2025-12-01` | +6h | min, max, umidade, condicao |

### 10.3 Estratégia de Sync (localStorage ↔ API)

```
┌─────────────────────────────────────────────────┐
│              Sync Strategy                        │
├─────────────────────────────────────────────────┤
│                                                   │
│  1. Usuário sem conta → localStorage apenas      │
│  2. Usuário com conta → localStorage + API sync  │
│                                                   │
│  Conflito resolution: Last-write-wins            │
│  (timestamp mais recente prevalece)              │
│                                                   │
│  Fluxo:                                          │
│    App abre → carrega localStorage               │
│    Se logado → GET /viagens/{id}/checklist       │
│    Compara timestamps → merge (mais recente)     │
│    Usuário interage → salva local + PUT API      │
│                                                   │
└─────────────────────────────────────────────────┘
```

---

## 11. Deploy e CI/CD

### 11.1 Pipeline Completa

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────────┐
│  Push    │────▶│  Lint &  │────▶│  Build   │────▶│  Deploy      │
│  (main)  │     │  Test    │     │  (Vite)  │     │  (GH Pages)  │
└──────────┘     └──────────┘     └──────────┘     └──────────────┘
                      │
                      ├── ESLint (frontend)
                      ├── Vitest (unit tests)
                      ├── ruff (backend, Fase 2+)
                      └── pytest (backend, Fase 2+)
```

### 11.2 Workflow Frontend (Fase 1)

```yaml
# .github/workflows/deploy.yml
name: Build & Deploy

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - run: npm ci
        working-directory: frontend

      - run: npm run lint
        working-directory: frontend

      - run: npm run test:unit
        working-directory: frontend

  build-deploy:
    needs: lint-test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - run: npm ci
        working-directory: frontend

      - run: npm run build
        working-directory: frontend

      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: frontend/dist

      - id: deployment
        uses: actions/deploy-pages@v4
```

### 11.3 Workflow Backend (Fase 2+)

```yaml
# .github/workflows/backend.yml
name: Backend CI

on:
  push:
    paths: ['backend/**']
  pull_request:
    paths: ['backend/**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -e ".[dev]"
        working-directory: backend

      - name: Lint
        run: ruff check .
        working-directory: backend

      - name: Type check
        run: mypy app/
        working-directory: backend

      - name: Tests
        run: pytest --cov=app --cov-report=term-missing
        working-directory: backend
```

### 11.4 Estratégia de Deploy por Fase

| Fase | Frontend | Backend | Observação |
|------|----------|---------|-----------|
| 1 | GitHub Pages (auto) | — | Push → main = deploy |
| 2 | GitHub Pages (auto) | Railway / Render / Fly.io | Backend em free tier |
| 3 | CloudFront + S3 | AWS Lambda (Mangum) + API Gateway | Infra AWS completa |

Para Fase 2, o backend pode rodar em um PaaS gratuito com deploy automático via GitHub:
- **Railway:** Docker deploy, free tier com 500h/mês
- **Render:** Web service, free tier com spin-down
- **Fly.io:** Container, free allowance

---

## 12. Migração — Do MVP Atual para Vue.js

### 12.1 Estratégia de Migração

A migração deve ser **incremental** e preservar o conteúdo existente:

```
Fase Migração:

1. SETUP (Semana 1)
   ├── Inicializar projeto Vue.js no diretório /frontend
   ├── Configurar Vite, Tailwind, Vue Router, Pinia
   ├── Mover guias .md para /frontend/src/content/
   └── Extrair dados estruturados dos guias para JSON

2. HOME + NAVEGAÇÃO (Semana 1-2)
   ├── Recriar landing page como HomeView.vue
   ├── Implementar layout responsivo (header, nav, footer)
   └── Configurar rotas com lazy loading

3. CONTEÚDO (Semana 2-3)
   ├── Implementar views de conteúdo (Evento, Hotéis, Voos, Clima, Turismo)
   ├── Usar MarkdownRenderer para guias existentes
   └── Adicionar componentes interativos (filtros, cards)

4. FERRAMENTAS (Semana 3-4)
   ├── Migrar checklist HTML → ChecklistView.vue com Pinia
   ├── Implementar OrcamentoView (Feature 8 — nova)
   ├── Implementar TimelineView (Feature 7 — nova)
   └── Garantir persistência localStorage funcional

5. PWA + POLISH (Semana 4-5)
   ├── Adicionar Service Worker (vite-plugin-pwa)
   ├── Testar offline capability
   ├── Otimizar performance (code splitting, images)
   └── Atualizar CI/CD workflow

6. CUTOVER (Semana 5)
   ├── Atualizar GitHub Actions para buildar Vue
   ├── Remover arquivos estáticos antigos da raiz
   ├── Mover docs originais para /docs (preservar histórico)
   └── Verificar deploy no GitHub Pages
```

### 12.2 Coexistência Durante Migração

Durante a migração, ambos podem coexistir:

```
reInventPlanning/
├── index.html              ← Antigo (redireciona para /frontend/dist)
├── guias/                  ← Antigo (mantido até cutover)
├── ferramenta/             ← Antigo (mantido até cutover)
├── frontend/               ← Novo Vue.js app
│   └── dist/              ← Build output (servido pelo Pages)
└── .github/workflows/
    └── deploy.yml          ← Atualizado para buildar Vue
```

### 12.3 Dados a Extrair dos Guias

| Guia | Dados a extrair para JSON |
|------|--------------------------|
| 01-sobre-o-evento.md | Tipos de sessão, níveis, tipos de pass, cronograma semana |
| 02-hoteis-hospedagem.md | Array de hotéis com preços, distância, nível, shuttle routes |
| 03-voos-deslocamento.md | Rotas de voo, opções transporte, chips, documentação |
| 04-clima-vestuario.md | Temperaturas, lista de mala, remédios, mochila do dia |
| 05-turismo-compras.md | Atrações, shoppings, restaurantes, preços médios, passeios |

O conteúdo textual permanece como markdown renderizado. Apenas os **dados comparáveis/filtráveis** são extraídos para JSON.

---

## 13. Roadmap Técnico Detalhado

### Sprint 1 (Semanas 1-2): Setup + Estrutura

| Task | Esforço | Entrega |
|------|---------|---------|
| Init projeto Vue 3 + Vite + TypeScript | 2h | Scaffold funcional |
| Configurar Tailwind CSS | 1h | Design system base |
| Configurar Vue Router (hash mode) | 1h | Navegação funcionando |
| Configurar Pinia + localStorage plugin | 2h | Estado persistente |
| Layout principal (header, nav, footer) | 4h | Shell do app |
| HomeView com hero + cards de navegação | 4h | Landing page nova |
| CI/CD: GitHub Actions buildando Vue | 2h | Deploy automático |
| **Total Sprint 1** | **~16h** | **App navegável no Pages** |

### Sprint 2 (Semanas 3-4): Conteúdo + Views

| Task | Esforço | Entrega |
|------|---------|---------|
| Extrair dados dos guias para JSON | 4h | Dados estruturados |
| MarkdownRenderer component | 2h | Renderização de guias |
| EventoView (tipos sessão, cronograma) | 4h | Guia do evento interativo |
| HoteisView (cards, filtro, comparador) | 6h | Comparador de hotéis |
| VoosView + ClimaView + TurismoView | 6h | Guias com componentes |
| **Total Sprint 2** | **~22h** | **Conteúdo migrado** |

### Sprint 3 (Semanas 5-6): Ferramentas Interativas

| Task | Esforço | Entrega |
|------|---------|---------|
| ChecklistView + store (migrar HTML) | 6h | Checklist reativo |
| TimelineView + milestones | 4h | Timeline visual |
| OrcamentoView + calculadora | 8h | Budget planner |
| CurrencyConverter composable | 2h | Conversão USD/BRL |
| **Total Sprint 3** | **~20h** | **Features interativas** |

### Sprint 4 (Semana 7): PWA + Polish

| Task | Esforço | Entrega |
|------|---------|---------|
| Service Worker (vite-plugin-pwa) | 3h | Offline support |
| Performance audit (Lighthouse) | 2h | Score > 90 |
| Responsividade mobile | 4h | Mobile-first polido |
| Testes unitários (stores + composables) | 4h | Cobertura > 70% |
| Cutover: remover arquivos antigos | 1h | Deploy limpo |
| **Total Sprint 4** | **~14h** | **App pronto para produção** |

### Total Estimado Fase 1 (Vue.js): ~72h (9 dias úteis)

---

## 14. ADRs (Architecture Decision Records)

### ADR-001: Vue.js sobre React/Svelte

**Status:** Aceito

**Contexto:** Precisamos de um framework frontend reativo para SPA.

**Decisão:** Vue.js 3 com Composition API.

**Justificativa:**
- Curva de aprendizado mais suave que React para contribuidores ocasionais
- Bundle menor que React (~33KB vs ~45KB)
- Composition API oferece composables reutilizáveis (similar a hooks)
- Ecossistema maduro: Pinia, Vue Router, Vite são todos oficiais
- Single-file components (.vue) são intuitivos

**Alternativas descartadas:**
- React: mais complexo para projeto open-source com contribuidores variados
- Svelte: ecossistema menor, menos contratações no mercado BR
- Astro: excelente para conteúdo, mas menos adequado para ferramentas interativas

---

### ADR-002: Hash Routing no GitHub Pages

**Status:** Aceito

**Contexto:** GitHub Pages não suporta rewrite rules para SPA routing.

**Decisão:** Usar `createWebHashHistory` do Vue Router (URLs com `#`).

**Justificativa:**
- Funciona 100% em qualquer host estático, sem configuração
- Refresh de página nunca resulta em 404
- Sem necessidade de 404.html hack (que retorna status 404 ao crawler)
- Trade-off: URLs menos limpas (`/#/evento` vs `/evento`)
- Mitigação futura: migrar para history mode ao mover para CloudFront (Fase 3)

**Alternativas descartadas:**
- History mode + 404.html fallback: funciona mas prejudica SEO
- Prerender (SSG): adiciona complexidade de build sem benefício claro na Fase 1

---

### ADR-003: Pinia sobre Vuex

**Status:** Aceito

**Contexto:** Precisamos de gerenciamento de estado global.

**Decisão:** Pinia como store oficial.

**Justificativa:**
- Recomendado oficialmente pelo Vue.js (substitui Vuex)
- API mais simples (sem mutations, sem namespaced modules)
- TypeScript nativo sem boilerplate
- DevTools integrado
- Suporte a composables dentro de stores

---

### ADR-004: FastAPI sobre Django/Flask

**Status:** Aceito (para Fase 2+)

**Contexto:** Backend Python para APIs de dados dinâmicos e persistência.

**Decisão:** FastAPI.

**Justificativa:**
- Performance async nativa (importante para chamadas a APIs externas)
- Auto-documentação via OpenAPI/Swagger (ótimo para frontend dev)
- Type-safety com Pydantic (validação de request/response automática)
- Compatível com Lambda via Mangum (deploy serverless)
- Mais leve que Django para API-only (sem ORM/admin/templates)

**Alternativas descartadas:**
- Django: overhead de ORM e admin desnecessários; mais lento para API pura
- Flask: sem async nativo, sem validação automática, sem docs geradas
- Node.js/Express: separação de linguagem com o time; Python tem melhor ecossistema para data

---

### ADR-005: DynamoDB sobre PostgreSQL

**Status:** Aceito (para Fase 3)

**Contexto:** Banco de dados para persistência de usuários e viagens.

**Decisão:** DynamoDB com single-table design.

**Justificativa:**
- Serverless (sem servidor para gerenciar, auto-scaling)
- Pay-per-request (perfeito para tráfego variável)
- Integração nativa com Lambda (IAM, sem connection pooling)
- Free tier generoso (25GB + 25 WCU/RCU permanentes)
- Suficiente para o modelo de acesso (user → viagens → checklist)

**Alternativas descartadas:**
- PostgreSQL (RDS): precisa de instância rodando 24/7, custos fixos
- PostgreSQL (Neon/Supabase): possível, mas adiciona dependência externa
- Firebase: vendor lock-in ao Google, menos integrado com AWS

---

### ADR-006: Dados Estáticos no Build vs. CMS

**Status:** Aceito

**Contexto:** Conteúdo dos guias precisa ser servido no frontend.

**Decisão:** Dados compilados no build (JSON + Markdown importados pelo Vite).

**Justificativa:**
- Zero latência (dados já no bundle ou code-split)
- Funciona 100% offline
- Versionado no Git (histórico de alterações)
- Sem dependência de CMS ou API para conteúdo
- Edição por PR no GitHub (acessível para comunidade)
- Trade-off: atualização requer novo build/deploy (aceitável para conteúdo trimestral)

**Alternativas descartadas:**
- Headless CMS (Contentful, Strapi): overhead e custo para conteúdo que muda raramente
- API de conteúdo: latência desnecessária, complexidade adicional
- SSG (Astro/Nuxt): adicionaria complexidade sem ganho claro (SEO não é prioridade #1)

---

*Documento criado em: Julho 2026*
*Última atualização: 12/07/2026*
*Versão: 1.0*
