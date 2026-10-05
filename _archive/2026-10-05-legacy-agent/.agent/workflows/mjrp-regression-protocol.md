---
description: Regression and Safety Protocol
---

# Regression Protocol v1.0

**Purpose**: Ensure new changes do not break existing functionality.
**Trigger**: After implementing any code change (fix or feature), BEFORE requesting user validation.

## 1. Compliance Check (The Golden Rule)

> **Golden Rule**: Always verify your work before declaring it done.

### Step 1: The Build Check
Always ensure the application builds successfully.
```bash
# Run your project's build command
npm run build  # or equivalent
```
- **Fail**: Stop and fix build errors.
- **Pass**: Proceed.

### Step 2: The Specific Check (Low/Medium Risk)
Identify the area you touched and execute targeted verification.
- **Reference**: Consult the project's regression checklist (below) or `docs/specs/spec.md` for expected behaviors.
- **Action**: Find the relevant feature area and verify its core flows.
- **Log**: Note successful verification.

#### Regression Checklist Template (Modular by Tags)

Organize your project's checklist by feature tags. The agent can run a specific tag (`[CORE]` only for smoke) or all tags for full regression.

```markdown
## Regression Checklist: [Project Name]
> **Usage**: Ask the agent to "Run the [TAG] checklist" or "Run full regression".

### 🔴 [CORE] Core Loop (Must Pass — Smoke Test)
- [ ] App loads without crash
- [ ] Primary user flow works end-to-end
- [ ] Data persists after reload
- [ ] Navigation forward/back works
- [ ] No console errors on main flows

### 🟡 [MODULE_A] [Feature/Module Name]
- [ ] [Primary flow for this module]
- [ ] [Secondary flow]
- [ ] [Edge case: empty state]
- [ ] [Edge case: error state]
- [ ] [Data integrity check]

### 🟡 [MODULE_B] [Feature/Module Name]
- [ ] [Primary flow]
- [ ] [Toggle/mode switch]
- [ ] [CRUD operations]
- [ ] [No stale data after changes]

### 🟢 [AUTOMATED] Automated Suite
\`\`\`bash
npm test              # Unit Tests
npm run test:e2e      # Browser Flows
\`\`\`
```

**Tag conventions**:
- `[CORE]`: Always run. The minimum "app is not broken" check.
- `[MODULE_X]`: Run when that feature area was touched.
- `[AUTOMATED]`: Run the full automated suite.
- Add tags as features grow. Keep each tag focused on ONE feature area.

Save as `docs/specs/regression_checklist.md` or `docs/manual/regression_checklist.md`.

### Step 3: The Full Suite (High Risk)
**Trigger**:
- You modified Core Logic (entry points, state management, routing).
- You refactored a shared component.
- You are unsure of the impact.

**Action**:
1. **Ask the User**:
   > "I have modified core logic. Should I run the Full Regression Checklist or the full Automated Suite?"
2. **If Full Regression**: Execute all known critical flows manually.
3. **If Automated Suite**: Run the full test suite.

## 2. Reporting

When confirming completion to the user, follow this format:
```markdown
**Verification Complete**
1. **Build**: Passed.
2. **Specific Check**: Executed [area] verification.
   - [Flow 1]: OK
   - [Flow 2]: OK
3. **Risk Level**: Low/Medium/High (reason).
```

## 3. Maintenance

If you find a bug during regression that is NOT related to your change:
1. Do not fix it immediately (scope creep).
2. Log it in `docs/sessions/DEBUG_LOG.md`.
3. Continue verification of *your* change.
