# 🏛️ Solution Architecture — re:Invent Community Planner

> Complete architecture reference for the re:Invent Community Planner: a
> trip‑and‑event planning application for Brazilians attending AWS re:Invent.
> This document describes the deployed system end to end — components, data
> model, security, deployment pipeline, and cost.

For product scope see [`SPEC.md`](./SPEC.md); for the decision log see the ADRs
in [`DESIGN.md`](./DESIGN.md).

---

## 1. Overview

The application is a **static single‑page app (SPA)** hosted on **GitHub Pages**
that works fully anonymously, plus an **optional serverless backend on AWS** that
unlocks a *logged area* with three account‑gated features:

| # | Feature | Summary |
|---|---------|---------|
| **F11** | Accounts & cloud plan | Sign up / sign in (Cognito); save checklist, budget and trip to the cloud, synced across devices. |
| **F12** | Location sharing | Opt‑in, reciprocal, auto‑expiring location sharing — coarse venue (default) or precise GPS (optional). |
| **F13** | findPeople | Meet‑up finder: see other attendees who are currently sharing (reciprocal), with an optional pepper 🌶️ highlight for a featured member. |

Design principles: **content‑first, mobile‑friendly, offline‑capable, privacy‑by‑design,
anonymous‑first** (login is never required for the core planning experience).

---

## 2. High‑Level Architecture

```
                          ┌──────────────────────────────────────────┐
                          │                Browser (PWA)             │
                          │   Vue 3 SPA · Pinia · Vue Router (hash)   │
                          │   Service Worker (offline cache)          │
                          └───────────────┬──────────────────────────┘
                                          │
              static assets               │  HTTPS (REST + JWT)
        ┌─────────────────────────────────┤
        │                                 │
        ▼                                 ▼
┌──────────────────┐            ┌───────────────────────────────────────────┐
│  GitHub Pages    │            │            AWS (us-east-1)                 │
│  (SPA hosting +  │            │                                            │
│   GitHub Actions │            │   Amazon Cognito  ──(JWT authorizer)──┐    │
│   CI/CD)         │            │   (User Pool)                         │    │
└──────────────────┘            │                                       ▼    │
                                │   API Gateway (HTTP API) ──► AWS Lambda     │
                                │      · CORS                  (FastAPI +     │
                                │      · Cognito JWT auth       Mangum)       │
                                │      · OPTIONS = no auth         │          │
                                │                                  ▼          │
                                │                        Amazon DynamoDB      │
                                │                        (single table, TTL)  │
                                └───────────────────────────────────────────┘
```

- The **frontend never talks to DynamoDB or Cognito credentials directly** for
  data; all data access goes through the authenticated API. Cognito is used
  only for the auth handshake (SRP) in the browser.
- If `VITE_API_URL` is not configured, the SPA runs in a **mock mode** (in‑memory
  / localStorage) so the full UX is demoable without any backend.

---

## 3. Frontend Architecture

**Stack:** Vue.js 3 (Composition API, `<script setup>`), TypeScript, Vite,
Tailwind CSS v4, Pinia (+ `pinia-plugin-persistedstate`), Vue Router (hash mode),
`vite-plugin-pwa`, `amazon-cognito-identity-js`.

### 3.1 Routing & guards
- **Hash routing** (`createWebHashHistory`) so refreshes never 404 on GitHub Pages
  (ADR‑002).
- Protected routes (`/perfil`, `/findpeople`) declare `meta.requiresAuth`; a global
  `router.beforeEach` guard redirects unauthenticated users to `/login?redirect=…`.
- `/findpepper` redirects to `/findpeople` (legacy path compatibility).

### 3.2 State & composables (module‑scope singletons)
| Composable | Responsibility |
|------------|----------------|
| `useAuth` | Cognito SRP sign‑up/confirm/sign‑in, session hydration, profile update, account deletion; falls back to a local mock when Cognito env is absent. |
| `useLocationShare` | Opt‑in sharing state, peer list, expiry countdown, reciprocal‑403 handling. |
| `useCloudSync` | Push/pull the plan (checklist/budget/trip) to the API; last‑write‑wins by timestamp; best‑effort (never blocks login). |
| `useI18n` / `useTheme` | i18n (PT/EN/ES) and light/dark theme, both persisted in `localStorage`. |

Pinia stores (`checklist`, `budget`, `trip`) persist locally; when authenticated
they also sync to the cloud.

### 3.3 Service layer
- `services/api.ts` — REST client with an **automatic mock fallback**. The mock
  mirrors the server’s privacy rules (opt‑in, reciprocity, expiry) so behaviour is
  identical with or without the cloud.
- `services/cognito.ts` — thin wrapper over `amazon-cognito-identity-js` (SRP flow;
  the password never leaves the browser in plaintext). Stores the **access token**
  used as the API Gateway JWT.

### 3.4 PWA / caching
- `registerType: autoUpdate` plus `cleanupOutdatedCaches`, `skipWaiting`,
  `clientsClaim` so a new deploy purges stale chunks and the new service worker
  takes control immediately (prevents mismatched‑chunk bugs across frequent deploys).

---

## 4. Backend Architecture

**Stack:** Python 3.12, FastAPI, Mangum (Lambda adapter), boto3, Pydantic;
packaged and deployed with **AWS SAM**.

### 4.1 Request flow
1. Browser calls `https://{api}.execute-api.us-east-1.amazonaws.com/api/v1/...`
   with `Authorization: Bearer <Cognito access token>`.
2. **API Gateway (HTTP API)** validates the JWT via the **Cognito authorizer**
   (issuer = the User Pool, audience = the app client) *before* invoking Lambda.
   `OPTIONS` (CORS preflight) is an explicit **unauthenticated** route so browsers
   are never blocked.
3. **Lambda (FastAPI via Mangum)** reads the verified `sub` claim from the request
   context (never trusts a raw token) and serves the route.
4. Handlers read/write **DynamoDB** through a single‑table repository.

### 4.2 Modules
```
backend/app/
├── main.py          FastAPI app, CORS, Mangum handler
├── config.py        Settings (table name, region, TTL caps, pepper email)
├── dependencies.py  get_current_user_sub — sub from gateway JWT claims
│                    (+ debug-only bearer fallback for local dev/tests)
├── db.py            DynamoDB single-table repository
├── schemas.py       Pydantic request/response models
└── routers/
    ├── plan.py      profile + plan (checklist/budget/trip) + account deletion
    └── share.py     start/stop/list/status location sharing
```

### 4.3 API endpoints (all under `/api/v1`, JWT‑protected except health)
```
GET    /api/health                 Public health check (no auth)

GET    /api/v1/profile             Get profile (email is never returned)
PUT    /api/v1/profile             Upsert profile (displayName, avatar, locale, email)
GET    /api/v1/plan                Get cloud plan (checklist/budget/trip)
PUT    /api/v1/plan/{kind}         Upsert a plan part (last-write-wins by updatedAt)
DELETE /api/v1/account             Right to erasure: wipe all user data

POST   /api/v1/share               Start/refresh sharing (venue | gps, duration, crew?)
DELETE /api/v1/share               Stop sharing (immediate revoke)
GET    /api/v1/share               List peers (any authenticated user; non-reciprocal)
GET    /api/v1/share/status        My current sharing status
```

---

## 5. Data Model (DynamoDB single table)

Table `tripevent-app` — one table, composite `PK`/`SK`, on‑demand billing, PITR
enabled, **TTL on `expiresAt`**.

| PK | SK | Item | TTL |
|----|-----|------|-----|
| `USER#{sub}` | `PROFILE` | displayName, avatar, locale, email*, updatedAt | — |
| `USER#{sub}` | `PLAN#checklist` | data, updatedAt | — |
| `USER#{sub}` | `PLAN#budget` | data, updatedAt | — |
| `USER#{sub}` | `PLAN#trip` | data, updatedAt | — |
| `SHARE#{scope}` | `USER#{sub}` | mode, venueId?/lat?/lng?, displayName, avatar, isPepper, statusText?, sharedAt, **expiresAt** | ✅ |

- `scope` is `GLOBAL` (open reciprocal pool) or a **crew code** (private group).
- `*email` is stored **only** to derive the `isPepper` highlight server‑side; it is
  **never** returned in any peer listing (data minimization).
- Location items exist **only while the user is actively sharing**; stopping sharing
  deletes the item, and TTL removes it automatically if the client disappears.

---

## 6. Security & Privacy

Location is the most sensitive data in the system, so privacy is enforced
**server‑side**, not merely in the UI (ADR‑010 / ADR‑011):

- **Anonymous‑first:** the core app requires no account; login unlocks extras only.
- **Opt‑in by default:** a user is invisible (not listed) until they explicitly share.
- **Non‑reciprocal viewing (login required):** any *authenticated* user can view who is
  sharing, even without sharing themselves. Being *listed* remains opt‑in, so
  non‑consenting users are never exposed.
- **Coarse by default:** venue selection is the primary mode; precise GPS is an extra
  opt‑in. GPS peers surface a Google Maps link to the shared position.
- **Auto‑expiry:** every location item carries `expiresAt` (DynamoDB TTL). GPS is
  capped at 4h, venue at 8h, regardless of the requested duration.
- **Instant revoke:** stopping sharing deletes the item immediately.
- **Data minimization:** only current state is stored — no location history; email is
  never exposed to other users.
- **Right to erasure:** `DELETE /api/v1/account` removes the profile, plan and share
  items (the Cognito user record is deleted out of band).
- **Transport & auth:** HTTPS only; CORS restricted to the GitHub Pages origin and
  localhost; JWT verified by the API Gateway authorizer; SRP auth keeps passwords
  off the wire.

---

## 7. Deployment & CI/CD

### 7.1 Frontend (GitHub Pages)
- `.github/workflows/deploy-pages.yml`: on push to `main`, install → type‑check →
  `vite build` → upload artifact → deploy to Pages.
- Vite loads `frontend/.env.production` at build time, injecting `VITE_API_URL` and
  the Cognito public IDs (non‑secret client identifiers, safe to ship in a SPA).

### 7.2 Backend (AWS SAM)
```bash
cd backend
sam validate --lint --template infra/template.yaml
sam build      --template infra/template.yaml
sam deploy     --template .aws-sam/build/template.yaml \
               --stack-name tripevent-backend --region us-east-1 \
               --resolve-s3 --capabilities CAPABILITY_IAM \
               --parameter-overrides CorsOrigin=https://flap.github.io
```
The stack provisions: Cognito User Pool + app client, DynamoDB table (TTL + PITR),
API Gateway HTTP API (Cognito JWT authorizer + CORS + unauthenticated OPTIONS),
and the Lambda function (`app.main.handler`).

### 7.3 Testing
- Backend: **15 pytest tests** using `moto` to mock DynamoDB — covering reciprocity,
  opt‑in default, revoke, venue‑vs‑gps, crew isolation, TTL caps, last‑write‑wins,
  account deletion, and the email‑privacy / `isPepper` behaviour.
- Frontend: `npm run build` runs `vue-tsc` type‑check + Vite build.

---

## 8. Cost

At community scale (≈2,000 monthly active users, ~1M requests/month) the backend
sits largely inside AWS free tiers:

| Category | Service | Est. monthly |
|----------|---------|--------------|
| Compute | AWS Lambda | ~$0 (free tier) |
| Networking | API Gateway (HTTP API) | ~$1 |
| Security | Cognito Essentials (≤10k MAU free) | ~$0 |
| Database | DynamoDB on‑demand + TTL | ~$0 |
| Hosting | GitHub Pages | $0 |
| **Total** | | **~$1–2 / month** |

Costs scale with traffic; even an event‑week spike remains modest given the free tiers.

---

## 9. Environments & Configuration

| Setting | Frontend (`VITE_*`) | Backend (`TRIPEVENT_*`) |
|---------|---------------------|-------------------------|
| API base URL | `VITE_API_URL` | — |
| Cognito | `VITE_COGNITO_REGION`, `VITE_COGNITO_USER_POOL_ID`, `VITE_COGNITO_APP_CLIENT_ID` | `COGNITO_USER_POOL_ID`, `COGNITO_APP_CLIENT_ID` |
| DynamoDB | — | `TABLE_NAME`, `AWS_REGION`, `DYNAMODB_ENDPOINT_URL` (local) |
| CORS | — | `CORS_ORIGINS` |
| Highlight | — | `PEPPER_EMAIL` |

Without `VITE_API_URL`, the SPA runs in mock mode (no backend needed).

---

## 10. Roadmap Alignment

This architecture implements **Phase 3** of the roadmap in `SPEC.md` (accounts +
serverless backend on AWS). Phase 4 candidates (real‑time exchange/weather APIs,
flight‑price alerts, session recommendations) would attach as additional Lambda
routes and external integrations behind the same API Gateway.

---

*Architecture document — re:Invent Community Planner. See `SPEC.md` and `DESIGN.md`
for product scope and decision records.*
