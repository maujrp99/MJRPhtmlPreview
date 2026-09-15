---
description: Protocol for setting up the development environment after project scaffolding. Covers remote repo, dependencies, linting, CI/CD, external services, and verification.
---

# Environment Setup Protocol

**When to run**: After the project scaffold is created (folder structure, SpecKit placeholders, AI configs) and before Discovery begins. The goal is to make the project runnable — not just documented.

**Pre-requisites**: constitution.md exists with the tech stack defined. VISION.md and CHARTER.md exist. Folder structure is in place.

---

## Step 1: Remote Repository

Set up the remote repository so all AI tools and collaborators can access it.

**Actions:**
1. Create the remote repo:
   ```bash
   gh repo create [project-name] --private --source=. --push
   ```
   (Use `--public` if it's an open-source project. Check CHARTER.md for guidance.)

2. Set up branch protection on `main`:
   - Require pull request reviews (if team > 1)
   - Require status checks to pass (once CI is configured)

3. Push existing commits:
   ```bash
   git push -u origin main
   ```

4. Create the `dev` branch:
   ```bash
   git checkout -b dev
   git push -u origin dev
   ```

**Verification**: `gh repo view` shows the repo with correct visibility and branches.

---

## Step 2: Dependency Management

Initialize the package manager and install base dependencies from the tech stack defined in constitution.md.

**For Node.js/TypeScript projects:**
```bash
npm init -y
# or: yarn init -y / pnpm init

# Install core dependencies from constitution.md
npm install [framework] [styling] [etc.]

# Install dev dependencies
npm install -D typescript @types/node [linters] [test-framework]
```

**For Python projects:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install [framework] [dependencies]
pip freeze > requirements.txt
```

**For monorepos:**
Set up the workspace configuration (npm workspaces, Turborepo, Nx, etc.) as defined in constitution.md.

**Verification**: `npm install && npm run build` (or equivalent) succeeds without errors.

---

## Step 3: Linting & Formatting

Configure code quality tools to enforce the standards from constitution.md. Consistency matters more than specific rules — pick a standard and stick with it.

**Common setups:**

- **ESLint + Prettier** (JS/TS):
  ```bash
  npm install -D eslint prettier eslint-config-prettier
  ```
  Create `.eslintrc.json` and `.prettierrc` aligned with constitution.md standards.

- **Black + Ruff** (Python):
  ```bash
  pip install black ruff
  ```
  Create `pyproject.toml` with formatting rules.

- **EditorConfig** (all projects):
  Create `.editorconfig` for consistent editor behavior across the team.

Add lint scripts to package.json (or Makefile):
```json
{
  "scripts": {
    "lint": "eslint src/",
    "format": "prettier --write src/",
    "lint:fix": "eslint src/ --fix"
  }
}
```

**Verification**: `npm run lint` (or equivalent) runs without configuration errors.

---

## Step 4: CI/CD Pipeline

Set up automated checks that run on every push and pull request.

**Basic GitHub Actions workflow** (`.github/workflows/ci.yml`):
```yaml
name: CI
on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main, dev]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4  # or setup-python, etc.
        with:
          node-version: '20'  # match constitution.md
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

Adapt the workflow to the tech stack in constitution.md. The pipeline should enforce at minimum: lint, test, and build.

**Verification**: Push a commit and confirm the workflow runs (even if tests are empty stubs for now).

---

## Step 5: External Services

Provision any services the project depends on. Document each one.

**Common services to set up:**
- **Database**: Firebase/Supabase/Postgres — create the project/instance, get connection strings
- **Authentication**: Auth provider setup (Firebase Auth, Auth0, Supabase Auth)
- **Hosting**: Vercel/Netlify/Firebase Hosting — connect to the repo
- **APIs**: Register for any third-party APIs needed, get API keys
- **Storage**: S3/GCS/Firebase Storage for file uploads

**Critical rules:**
- Never commit secrets. Use `.env` files locally and environment variables in CI.
- Add `.env` to `.gitignore` immediately.
- Create a `.env.example` with placeholder values so others know what's needed.
- Document each service in the README under a "Services" section.

```bash
# Example .env.example
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
API_KEY=your-api-key-here
AUTH_SECRET=your-secret-here
```

**Verification**: Each service is accessible with the configured credentials.

---

## Step 6: Local Development Verification

This is the "green light" step. Everything must work end-to-end locally.

**Checklist:**
- [ ] `git clone [repo-url] && cd [project]` works
- [ ] Dependencies install cleanly (`npm install` / `pip install -r requirements.txt`)
- [ ] Dev server starts (`npm run dev` / `python manage.py runserver`)
- [ ] Linting runs (`npm run lint`)
- [ ] Tests run (even if empty): `npm test` / `pytest`
- [ ] Build succeeds: `npm run build`
- [ ] External services are reachable from local environment

If any step fails, fix it before proceeding. The environment must be solid before Discovery begins.

---

## Step 7: Developer Onboarding Check

Verify that the README contains enough information for a new developer (human or AI) to get started.

**README should include:**
- Project description (link to VISION.md)
- Prerequisites (Node version, Python version, etc.)
- Setup instructions (clone, install, configure .env, run)
- Available scripts/commands
- Link to CHARTER.md for scope
- Link to docs/specs/ for technical details

**The test**: Could someone with zero context about this project clone the repo and have it running in under 10 minutes by following the README?

---

## Commit

After all steps are complete:
```bash
git add -A
git commit -m "chore: environment setup

- Remote repo configured on GitHub
- Dependencies installed per constitution.md
- Linting and formatting configured
- CI/CD pipeline active
- External services provisioned
- Local dev verified"
```

---

## Brownfield Adaptation

For Brownfield projects, this protocol focuses on **verifying and documenting** what already exists rather than creating from scratch:

1. **Remote Repo**: Likely already exists. Verify branch model matches what constitution.md says.
2. **Dependencies**: Audit existing deps. Document in constitution.md. Update outdated ones cautiously.
3. **Linting**: If not configured, add it gradually (don't lint the entire legacy codebase at once — configure to only lint new/modified files).
4. **CI/CD**: If missing, add it. If exists, verify it covers lint + test + build.
5. **External Services**: Document existing services in README and .env.example.
6. **Verification**: Same checklist — everything must work.
7. **Onboarding**: Update README to reflect the current state.
