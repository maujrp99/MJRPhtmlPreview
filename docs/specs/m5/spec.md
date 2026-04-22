# Specification: M5 — Load & Edit

**Status**: Draft
**Date**: 2026-04-21
**Milestone**: M5

## Problem Statement
The current workflow requires users to manually copy and paste content into the editor. If a user needs to change or replace content (e.g., updating data, rewriting sections, or tweaking a template) while looking at the rendered preview, they must find the corresponding code in the raw source. This creates unnecessary friction, especially when the goal is a visual tweak rather than a code-level change.

## User Stories
- **[US-11]**: As a developer, I want to load an HTML/Markdown file from my disk via a file picker, so I don't have to copy-paste.
- **[US-12]**: As a developer, I want to select and edit/replace any text content directly in the preview, so I can tweak the visual output without being forced to hunt through the source code.

## Requirements

### Functional
- **[FR05.1] Content Loading**: A button in the toolbar must trigger a native file picker filtered for `.html`, `.htm`, and `.md` files.
- **[FR05.2] Post-Load Flow**: Loading a file must replace the editor content and trigger an immediate preview update.
- **[FR05.3] Edit Mode Toggle**: A dedicated "Edit/View" toggle must exist in the toolbar.
- **[FR05.4] Visual Editing**: In "Edit Mode", the entire body of the preview iframe must be editable (`contentEditable = true`).
- **[FR05.5] In-Place Interaction**: Users must be able to select any text range and replace it by typing.
- **[FR05.6] State Synchronization**: Disabling "Edit Mode" must serialize the current iframe DOM and update the textarea source code.
- **[FR05.7] Markdown Caution**: If the input is Markdown, enabling "Edit Mode" must warn the user that edits will convert the output to HTML.

### Non-Functional
- **[NFR05.1] UI Indicator**: There must be a clear visual indicator (e.g., border highlight or status badge) when "Edit Mode" is active.
- **[NFR05.2] Structual Integrity**: The sync process must only update the text content and preserve the underlying HTML structure/styles as much as possible (DOM serialization).
- **[NFR05.3] Performance**: Context switching between Edit/View modes must be near-instant.

## Success Criteria
- [ ] Users can load a 50KB HTML file via file picker in under 2 seconds.
- [ ] Users can edit a paragraph in the preview and see the changes reflected in the textarea when they exit Edit Mode.
- [ ] Exported files include the visual edits made in Edit Mode.

## Out of Scope
- Full WYSIWYG features (adding images, changing fonts, drag-and-drop).
- Undoing individual edits (browser default undo in contentEditable is the baseline).
- Syncing edits back to the local file on disk (read-only for picker).

## Open Questions
- Should we force a "Save" or "Apply" step when exiting Edit Mode, or is it automatic?
- How do we handle complex layouts where `contentEditable` might break styling (e.g., heavily nested divs with absolute positioning)?
