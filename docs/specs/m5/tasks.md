# Tasks: M5 — Load & Edit

**Status**: Completed
**Plan Reference**: [plan.md](file:///Users/mpedroso/0.MyPetProjects/MJRPhtmlPreview/docs/specs/m5/plan.md)

## Pre-Implementation
- [x] Confirm spec.md and plan.md are APPROVED (Gate 1 & 2 ✅)
- [x] Ensure `dev` branch is clean

## Implementation: UI Structure & Styling
- [x] [T-05.1] Add toolbar elements: `#btnOpen`, `#btnEdit` and filename placeholder `#fileNameLabel`. [US-11, US-12]
- [x] [T-05.2] Add `<input type="file" id="fileInput" accept=".html,.htm,.md" hidden>` to `index.html`. [US-11]
- [x] [T-05.3] Define CSS for `.editing-active` (green border) and `.editing-badge` (absolute overlay) in `index.html`. [NFR05.1]

## Implementation: File Picker (US-11)
- [x] [T-05.4] In `js/app.js`, link `#btnOpen` click to trigger `#fileInput`. [US-11]
- [x] [T-05.5] In `js/app.js`, handle file selection via `FileReader.readAsText()`. [US-11]
- [x] [T-05.6] Update editor content and trigger live preview refresh after load. [US-11]
- [x] [T-05.7] Update file name indicator in UI if a file is loaded. [US-11]

## Implementation: Inline Visual Edit (US-12)
- [x] [T-05.8] In `js/preview.js`, create `toggleEditMode(forceState)` function. [US-12]
- [x] [T-05.9] Handle `contentEditable = true/false` on `iframe.contentDocument.body`. [US-12]
- [x] [T-05.10] Apply/Remove visual editing cues (CSS class/badge/cursor type). [US-12, AC-95]
- [x] [T-05.11] Implement synchronization logic: serialize `innerHTML` to `textarea.value` (Ensuring structural integrity). [US-12, FR05.6, AC-99]
- [x] [T-05.12] Add user confirmation/warning for Markdown -> HTML conversion. [US-12, FR05.7]

## Verification & Polish
- [x] [T-05.13] Manual Test: Verify HTML/MD load via picker.
- [x] [T-05.14] Manual Test: Verify visual edit synchronization (multi-paragraph selection & replace).
- [x] [T-05.15] Manual Test: Verify export (Local/PDF/PNG) with edited content.
- [x] [T-05.16] Regression: Ensure Google Drive save still functions correctly.

## Documentation
- [x] Update `ROADMAP.md` and `CHARTER.md` status if needed.
- [x] Update `SESSION_HISTORY.md`.
- [x] Final Commit: `feat: implement file loader and inline editing (M5)`
