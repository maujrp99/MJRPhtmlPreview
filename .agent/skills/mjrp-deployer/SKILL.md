---
name: mjrp-deployer
description: >
  DevOps and deployment expert for the MJRP portfolio. Covers Vercel (Next.js 15 App Router),
  Firebase Hosting, Cloud Run (Docker + Cloud Build), GitHub Actions CI/CD, GitHub Pages,
  Google Apps Script (clasp), GCP Secret Manager, and Firestore rules. Use when: deploying any
  project, writing pre-deploy checklists, running smoke tests, configuring CI/CD, managing
  secrets, debugging Dockerfiles, firebase.json, cloudbuild.yaml, vercel.json, .clasp.json.
  Trigger on: "deploy", "vercel", "hosting", "cloud run", "firebase deploy", "github pages",
  "clasp push", "docker", "cloud build", "CI/CD", "github actions", "secret manager",
  "firestore rules", "pipeline", "infra", "env vars", "smoke test", "production checklist",
  "preview channel", "southamerica-east1", "next-intl deploy", "admin auth deploy".
---

# Skill: MJRP Deployer / DevOps Expert

You are the infrastructure and deployment expert for the MJRP portfolio. You write real deployment
configurations grounded in the actual project stacks. You always check `constitution.md` before
recommending anything. You produce deployment checklists that cover configs, integrations, and
dependencies — not just "run these commands."

**Complements**:
- `mjrp-frontend-developer` / `mjrp-vue3-pinia` → code (you own how it gets deployed)
- `mjrp-backend-developer` → Node.js service code (you own Cloud Run config)
- `mjrp-system-architect` → architectural tradeoffs that affect infra choices

---

## Portfolio Infra Matrix

| Project | Frontend Deploy | Backend | CI/CD | Secrets |
|---------|----------------|---------|-------|---------|
| **MJRPpersonal** | Vercel (auto Git) | — (API Routes) | Vercel Git integration | Vercel env vars |
| **MJRPalbumblender-v1** | Firebase Hosting (free tier) | Cloud Run via Cloud Build | GitHub Actions | GCP Secret Manager |
| **MJRPhtmlPreview** | GitHub Pages (static) | — | Manual push | — |
| **NQCfupbot** | — (Apps Script) | Google infra | Manual / clasp | PropertiesService |
| **visual-notes-hub** | AppSheet | Apps Script via clasp | Manual / clasp | PropertiesService |

**GCP region standard**: `southamerica-east1` (Brazil) for all GCP services.

---

## 1. MJRPpersonal — Vercel + Next.js 15 (PRIMARY)

### Stack reality check
- Next.js 15 App Router + TypeScript + Tailwind + Framer Motion + Sonner
- **next-intl** — i18n middleware handles locale routing (`/pt/*` and `/en/*`)
- **JWT admin auth** — `middleware.ts` guards `/admin/*` via `jose` cookie-based JWT
- **Obsidian Vault as CMS** — local Markdown files bundled at build time; no runtime FS access
- **next/image** — external sources: `books.google.com`, `covers.openlibrary.org`, `m.media-amazon.com`
- **Python scripts** (`scripts/`) — data enrichment, run locally; never deployed to Vercel
- **outputFileTracingExcludes** — `venv/**` and `.pytest_cache/**` already excluded in `next.config.ts`

### 1.1 Pre-Deploy Checklist — Environment Variables

These MUST exist in Vercel dashboard before deploying to production.

```
[ ] GEMINI_API_KEY        → Vercel → Settings → Environment Variables → Production
[ ] ADMIN_PASSWORD        → Vercel → Settings → Environment Variables → Production
[ ] ADMIN_JWT_SECRET      → Vercel → Settings → Environment Variables → Production
                             ⚠️  If missing, middleware falls back to hardcoded dev secret —
                             this is a SECURITY RISK. Must be a 32-byte hex string.
                             Generate: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

**Verify via CLI:**
```bash
vercel env ls --environment production
# Must show: GEMINI_API_KEY, ADMIN_PASSWORD, ADMIN_JWT_SECRET
```

**Pull to local for parity check:**
```bash
vercel env pull .env.local
# Diffs against .env.local.example to verify nothing is missing
```

### 1.2 Pre-Deploy Checklist — Build & Code Quality

```
[ ] Type check passes
      npm run type-check  (or: npx tsc --noEmit)
      ❌ If this fails, Vercel build will also fail

[ ] Lint passes
      npm run lint
      ❌ ESLint errors = build failure on Vercel (unlike local next dev)

[ ] Local build succeeds
      npm run build
      ✓ Check output: no red errors, confirm page count is expected

[ ] Local production start works
      npm run start
      ✓ Visit http://localhost:3000 and http://localhost:3000/en
      ✓ Confirm i18n routing works locally before pushing
```

### 1.3 Pre-Deploy Checklist — next-intl i18n Configuration

```
[ ] Default locale resolves — visiting / redirects to /pt (or whichever is default)
[ ] /en/* routes resolve correctly
[ ] middleware.ts matcher excludes: api, _next, _vercel, static assets (verify config.matcher)
[ ] All translation keys exist in both pt.json and en.json
      Missing key = runtime error in production
[ ] No hardcoded locale strings in components (should come from useTranslations())
```

### 1.4 Pre-Deploy Checklist — Admin Auth (JWT)

```
[ ] ADMIN_JWT_SECRET is set in Vercel → NOT the dev fallback string
[ ] ADMIN_PASSWORD is set in Vercel
[ ] /admin/login page renders without error
[ ] Login form submits and sets cookie correctly
[ ] /admin/* redirects to /admin/login when cookie is absent or expired
[ ] /en/admin/login path works (intl variant)
[ ] JWT cookie has appropriate expiry (not "forever")
[ ] getJwtSecret() does NOT fall back to hardcoded string in production
      → Add runtime check: if (!process.env.ADMIN_JWT_SECRET) throw new Error(...)
```

### 1.5 Pre-Deploy Checklist — Content / Vault

```
[ ] MJRPvault/ content is committed to the repo (or accessible at build time)
      ⚠️  Vercel runs builds in an ephemeral container — content MUST be in the repo
      or fetched at build time via a script. It cannot be read from a local path at runtime.

[ ] NO local filesystem mutations in Serverless Functions
      ⚠️ Vercel `/var/task` is Read-Only in production. If the app has `/api` routes calling `fs.writeFile` or `fs.mkdir` to persist data, IT WILL CRASH in production. Writes must go to a Database, S3, or GitHub REST API.

[ ] All Markdown files parse without YAML frontmatter errors
      Run locally: npm run build — content parse errors surface here

[ ] next/image remotePatterns cover ALL external image domains in use
      Verify in next.config.ts: books.google.com, covers.openlibrary.org,
      m.media-amazon.com, images-na.ssl-images-amazon.com
      ❌ Missing domain = 400 error on image load in production

[ ] outputFileTracingExcludes is set for venv/ and .pytest_cache/
      ✓ Already configured — verify it's still in next.config.ts
```

### 1.6 Pre-Deploy Checklist — Vercel Project Config

In the Vercel dashboard (`vercel.com/[team]/mjrp-personal/settings`):

```
[ ] Root Directory: . (project root, not src/)
[ ] Framework Preset: Next.js (auto-detected)
[ ] Build Command: npm run build (default) — confirm it's not overridden incorrectly
[ ] Output Directory: .next (default for App Router)
[ ] Node.js Version: 18.x or 20.x — match what you develop with locally
      Check: node --version  →  must match Vercel setting
[ ] Install Command: npm ci (not npm install — for reproducible builds)
[ ] Git branch: main → Production, other branches → Preview
[ ] Custom domain: configured and DNS propagated (check CNAME/A records)
[ ] HTTPS: enforced (Vercel does this automatically — verify no http:// hardcoded links)
```

### 1.7 Pre-Deploy Checklist — Performance & SEO

```
[ ] Metadata API configured: each page/layout exports metadata or generateMetadata()
[ ] OG image: app/opengraph-image.tsx or .png exists
[ ] robots.ts / sitemap.ts generated (or static files in /public)
[ ] next/font used for all fonts (no Google Fonts CDN link tags — causes FOUT)
[ ] next/image used for all images (not <img> tags)
[ ] No console.log() calls left in Server Components (leaks to server logs)
[ ] Bundle size check:
      npx @next/bundle-analyzer (if configured) or check .next/analyze/
      Target: no single JS chunk > 250kb gzipped
```

### 1.8 Pre-Deploy Checklist — Security

```
[ ] ADMIN_JWT_SECRET is cryptographically random (≥32 bytes)
[ ] .env.local is in .gitignore — verify: git check-ignore .env.local
[ ] No API keys in client components (NEXT_PUBLIC_ prefix = exposed to browser)
      GEMINI_API_KEY must be server-only (no NEXT_PUBLIC_ prefix)
[ ] Server Actions: each action validates authentication before mutating data
[ ] Content Security Policy headers (optional but recommended):
      Add to next.config.ts → headers() if needed
[ ] Rate limiting on /api/admin/* routes (if any sensitive endpoints exist)
```

### 1.9 Deploy to Vercel — Commands

```bash
# Option A: Git push (recommended — triggers CI/CD automatically)
git push origin main           # → Production deploy
git push origin feat/my-feat   # → Preview deploy

# Option B: Vercel CLI (for urgent hotfixes or manual control)
vercel --prod                  # Deploy current dir to production
vercel                         # Deploy as preview

# Monitor deploy
vercel ls                      # List recent deployments
vercel inspect <deployment-url> # Inspect a specific deployment
vercel logs <deployment-url>   # Stream logs from a deployment

# Rollback (emergency)
vercel rollback                # Roll back to previous deployment
```

### 1.10 Smoke Tests — Post-Deploy

Run these IMMEDIATELY after every production deploy. Check against the live URL.

```
SITE=https://your-domain.com

## Routing & i18n
[ ] GET $SITE/          → 200 or redirect to /pt (default locale)
[ ] GET $SITE/en        → 200 (English locale root)
[ ] GET $SITE/pt        → 200 (Portuguese locale root)
[ ] GET $SITE/xyzzy     → 404 page renders (not blank, not Vercel default)

## Admin Auth flow
[ ] GET $SITE/admin     → 302 redirect to /admin/login (unauthenticated)
[ ] GET $SITE/en/admin  → 302 redirect to /en/admin/login (i18n variant)
[ ] GET $SITE/admin/login → 200 — login form renders
[ ] POST login with correct ADMIN_PASSWORD → 302 to /admin (cookie set)
[ ] GET $SITE/admin after login → 200 — admin area loads
[ ] POST login with wrong password → 401/stays on login, error message shown

## Content pages
[ ] At least 2 content pages load with real data (books, posts, etc.)
[ ] No "[object Object]" or "undefined" text visible anywhere
[ ] next/image images load (books.google.com / openlibrary.org sources render)

## Gemini integration (if any page triggers it)
[ ] Feature using GEMINI_API_KEY returns a real response (not 401 or 500)

## Performance
[ ] Lighthouse score ≥ 80 on Performance (run in incognito)
[ ] No hydration errors in browser console
[ ] No 404s for _next/static/* assets (means build output is correct)
```

**Quick CLI smoke test:**
```bash
SITE=https://your-domain.com
curl -sI "$SITE/"          | head -3
curl -sI "$SITE/admin"     | head -3   # expect 302 → /admin/login
curl -sI "$SITE/admin/login" | head -3 # expect 200
curl -sI "$SITE/en"        | head -3   # expect 200
```

### 1.11 Rollback Protocol

If smoke tests fail after a production deploy:

```bash
# 1. Immediate rollback via CLI
vercel rollback

# 2. Or via dashboard: vercel.com → project → Deployments → previous deploy → Promote to Production

# 3. Investigate failure:
vercel logs <failed-deployment-url>

# 4. Common post-deploy failure causes:
#    - Missing env var → check Vercel dashboard, re-add, redeploy
#    - Build succeeded but runtime error → check Function logs in Vercel dashboard
#    - i18n routing broke → check middleware.ts matcher wasn't accidentally changed
#    - Image optimization error → check remotePatterns in next.config.ts
```

---

## 2. MJRPalbumblender-v1 — Firebase Hosting + Cloud Run

### 2.1 firebase.json — SPA with Cloud Run backend
```json
{
  "hosting": {
    "public": "dist",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      { "source": "/api/**", "run": { "serviceId": "mjrp-proxy", "region": "southamerica-east1" } },
      { "source": "**", "destination": "/index.html" }
    ]
  }
}
```
- `"public": "dist"` — Vite output dir (never `build`)
- `/api/**` → Cloud Run; `**` → `index.html` (Vue SPA). Rewrite order matters — `**` MUST be last.

### 2.2 Pre-Deploy Checklist — AlbumBlender

```
[ ] Firebase project set in .firebaserc
[ ] GitHub secrets set: FIREBASE_SERVICE_ACCOUNT, FIREBASE_PROJECT
[ ] GCP Secret Manager has all secrets: AI_API_KEY, musickit-team-id,
    musickit-key-id, musickit-private-key, Spotify client secret, Firebase Admin SA
[ ] Firestore rules updated if schema changed: npx firebase-tools deploy --only firestore:rules
[ ] albumRankings rule changed from `if true` to `if request.auth != null` before launch
[ ] Cloud Run secrets mapping in cloudbuild.yaml matches Secret Manager names
[ ] Docker build succeeds locally: docker build -t mjrp-proxy server/
[ ] npm test passes in root and server/
[ ] npm run build produces dist/ with correct assets
```

### 2.3 Deploy Commands

```bash
# Frontend (Firebase Hosting)
npx firebase-tools deploy --only hosting --project $FIREBASE_PROJECT

# Backend (Cloud Run via Cloud Build)
gcloud builds submit --config cloudbuild.yaml --project $GCP_PROJECT

# Preview channel (PRs)
npx firebase-tools hosting:channel:deploy pr-$PR_NUM --project $FIREBASE_PROJECT

# Firestore rules only
npx firebase-tools deploy --only firestore:rules --project $FIREBASE_PROJECT
```

### 2.4 GitHub Actions — CI/CD Pattern
```yaml
# On PR → build + test + Firebase Preview Channel
# On push to main / tag v* → build + test + Firebase Production deploy
# Cloud Build (backend) triggered separately via gcloud CLI or GCP trigger
```
See: `.github/workflows/ci-firebase.yml` in the project for the full workflow.

### 2.5 Smoke Tests — AlbumBlender

```
[ ] GET https://your-app.web.app/         → 200 (Vue SPA loads)
[ ] GET https://your-app.web.app/api/health → 200 from Cloud Run (or defined health endpoint)
[ ] Spotify OAuth flow completes → token returned, user authenticated
[ ] Apple MusicKit initializes without console errors
[ ] Album library loads from Firestore
[ ] Gemini AI feature returns response (AI_API_KEY working)
[ ] No CORS errors on /api/** requests
```

---

## 3. MJRPhtmlPreview — GitHub Pages (Static)

```bash
# Deploy model: push to gh-pages branch (no build step)
git subtree push --prefix . origin gh-pages
# or: git push origin main:gh-pages

# Google OAuth redirect URI must match the exact Pages URL
# HTTPS enforced automatically
```

---

## 4. Google Apps Script / clasp (NQCfupbot, visual-notes-hub)

```bash
clasp login                          # One-time auth
clasp push                           # Upload .gs files to Apps Script
clasp deploy --description "v2.1.0"  # Create a new deployment
clasp logs                           # View execution logs

# .clasp.json
{ "scriptId": "<your-script-id>", "rootDir": "./src" }

# Secrets via PropertiesService (NOT environment variables)
PropertiesService.getScriptProperties().setProperty('API_KEY', 'xxx')  # run once
const key = PropertiesService.getScriptProperties().getProperty('API_KEY')
```

**Pre-deploy:**
```
[ ] clasp push succeeds without errors
[ ] No syntax errors in Apps Script editor after push
[ ] Test all triggers manually before deploying new version
[ ] PropertiesService values set in target script (not just local)
```

---

## 5. GCP Secret Manager

```bash
# Create a secret
echo -n "value" | gcloud secrets create SECRET_NAME --data-file=- --project $GCP_PROJECT

# Update a secret version
echo -n "new-value" | gcloud secrets versions add SECRET_NAME --data-file=- --project $GCP_PROJECT

# View (debug only)
gcloud secrets versions access latest --secret=SECRET_NAME --project $GCP_PROJECT

# Grant Cloud Run service access
gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member="serviceAccount:SA@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor" --project $GCP_PROJECT
```

---

## 6. Common Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Vercel build fails: type error | TSC finds issues ESLint missed | `npm run type-check` locally first |
| Vercel build fails: ESLint error | ESLint errors = hard fail on Vercel | `npm run lint` locally, fix all errors |
| `/admin` doesn't redirect (stays 200) | ADMIN_JWT_SECRET missing → fallback secret accepted | Set ADMIN_JWT_SECRET in Vercel env vars |
| i18n routes 404 in production | middleware.ts matcher too broad or too narrow | Check `config.matcher` in middleware.ts |
| Images 400 in production | Domain not in next.config.ts remotePatterns | Add domain to `images.remotePatterns` |
| Vault content missing in prod | Content files not committed to repo | Commit MJRPvault/ or adjust .gitignore |
| Gemini API 401 in production | GEMINI_API_KEY not set in Vercel env vars | Add to Vercel → Settings → Env Vars |
| Cloud Run 503 on startup | App crashes: missing env var or wrong PORT | Check: `gcloud run services logs tail mjrp-proxy` |
| Firebase deploy: "not in project" | .firebaserc missing or wrong project | `cat .firebaserc`, run `firebase use --add` |
| clasp push: script not found | .clasp.json has wrong scriptId | `clasp clone <correct-scriptId>` |
