---
description: Systematic debugging protocol
---

# Debug Protocol v2.0

**Purpose**: Systematic process for tracking, finding, fixing, and documenting issues.
**Trigger**: A reported bug or critical failure.

## The Golden Rules
1. Follow the development rules in `docs/specs/constitution.md`.

## 1. Intake (Grounding)

1. **Grounding**: Load project context via `onboarding_protocol.md` if not already loaded.
2. **Log**: Add entry to `docs/sessions/DEBUG_LOG.md` using the canonical format below.

   #### DEBUG_LOG.md Format
   ```markdown
   # Debug Log
   > Last Update: YYYY-MM-DD
   > Next Issue #: [N+1]

   ## Issue Index
   | # | Status | Summary | Date | Files Modified |
   |---|--------|---------|------|----------------|
   | #003 | 🔴 Active | [Short description] | YYYY-MM-DD | TBD |
   | #002 | ✅ Resolved | [Short description] | YYYY-MM-DD | file1.js, file2.js |
   | #001 | ✅ Resolved | [Short description] | YYYY-MM-DD | file3.js |

   ## Active Issues

   ### #003: [Title]
   - **Reported**: YYYY-MM-DD
   - **Symptom**: [What the user sees]
   - **Root Cause**: [TBD until analysis complete]
   - **Fix**: [TBD until implementation complete]
   - **Files Modified**: [TBD — fill on resolution]
   - **Related**: [#NNN if related to a past issue]

   ## Resolved Issues

   ### #002: [Title]
   - **Reported**: YYYY-MM-DD | **Resolved**: YYYY-MM-DD
   - **Root Cause**: [What caused it]
   - **Fix**: [What was done]
   - **Files Modified**: `path/file1.js`, `path/file2.js`
   - **Commit**: `fix(<scope>): <description>`
   ```

   **Rules**:
   - **Sequential numbering**: Issues are #001, #002, #003... NEVER reuse a number
   - **Next Issue #**: Keep the counter at the top for quick reference
   - **Files Modified**: MANDATORY — fill on resolution, include in Issue Index
   - **Related**: Cross-reference related issues (e.g., "#003 is a regression of #001")
   - Update Last Update timestamp on every change
   - New issues → Active Issues + Issue Index
   - Resolved issues → move to Resolved section (newest first)
   - Keep Resolved sections for history (never delete)
3. **Reproduce**: Confirm the issue.

## 2. Analysis (The "Why")

1. **Consult Architecture**: Check `docs/specs/arch.md` to understand *intended* behavior. Review `docs/specs/constitution.md` for relevant patterns.
2. **Holistic Impact Analysis**: What is the overall impact of the potential fix? Have you checked all relevant architecture and spec documents to ensure you have the big picture and awareness of all functionalities that may be impacted?
3. After thorough analysis: **Hypothesis**: Formulate a theory.
4. **Plan**: Describe the fix.
   - *Check*: If fix requires changing a Core Pattern → **STOP**. Write an ADR first (`docs/architecture/`).

## 3. Implementation

0. Follow `docs/specs/constitution.md` and `docs/specs/arch.md`.
1. **Apply Fix**: Implement with componentization and modularity reuse whenever possible, following architecture patterns. If not possible, try to modularize the fix.
2. **Legacy Code**: If the fix replaces code, clean it and add deleted/replaced code to the debug log.
3. **Code Check**: Confirm no architecture layer violations.

## 4. Verification (The "Safety Net")

1. **Happy Path**: Verify the fix works.
2. **Regression Check**: Run `regression_protocol.md` for the affected area.
3. **Test Suite**: Run the project's automated tests.

## 5. Closure (The "Definition of Done")

1. **Log Resolution**: Update `docs/sessions/DEBUG_LOG.md` with:
   - Root Cause.
   - Solution.
   - Files Modified.
2. **Update Documentation**: If you changed how something works, update the relevant spec/arch documents.
3. **Commit**: `fix: <description>` following Conventional Commits.
4. **User Confirmation**: Ask the user to verify.