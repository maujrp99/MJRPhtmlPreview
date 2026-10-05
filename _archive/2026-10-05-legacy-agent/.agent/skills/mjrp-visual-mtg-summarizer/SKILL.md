---
name: mjrp-visual-mtg-summarizer
description: >
  Transform meeting notes into 4 structured summaries + a Mermaid diagram + a self-contained HTML visual infographic following CI&T brand guidelines. Accepts pasted transcripts, uploaded files, URLs, or Notion page references.
  Trigger: summarize meeting, meeting notes, meeting summary, reunião, resumo de reunião, summarize transcript, meeting recap, infographic meeting, visual summary, meeting infographic, KO meeting, NotebookLM meeting.
---

# Visual Meeting Summarizer

Transform raw meeting notes into structured summaries and a branded visual infographic. All outputs are generated as separate files — never all at once in chat.

---

## §0 — Input Protocol

**Accept any of these input forms:**
- Pasted transcript text
- Uploaded file (txt, md, pdf, docx)
- URL or shared link → **attempt to access it before declaring no access.** Try silently a second time if the first fails. Never respond "I don't have access" as the first answer to a link.
- Notion page reference → use the `notion-query-meeting-notes` tool to fetch the content

**If content is unavailable after all attempts:** state clearly what was tried and why you could not proceed. Never fabricate meeting content. A summary built on invented content is worse than no summary.

**Before generating outputs**, confirm:
- What is the meeting name/title? (used in filenames)
- What is today's date? (used in filenames — format: `dd-MMM-yy`, e.g. `21-Apr-26`)

If the user didn't provide these, infer from the content or ask once.

---

## §1 — Output Map

Generate the following files **separately and in order**, presenting each one before moving to the next:

| # | File | Format | Description |
|---|------|--------|-------------|
| 1 | `summary-thematic.md` | Markdown | Thematic Model — content-focused |
| 2 | `summary-cornell.md` | Markdown | Adapted Cornell Model — learning-focused |
| 3 | `summary-executive.md` | Markdown | Direct Executive Model — action-focused |
| 4 | `summary-qa.md` | Markdown | Q&A Model — clarification-focused |
| 5 | `notebooklm-prompt.md` | Markdown | Ready-to-paste NotebookLM infographic prompt |
| 6 | `{meeting-name}_{dd-MMM-yy}.html` | HTML | Self-contained visual infographic (CI&T branded) |
| 7 | `diagram.mermaid` | Mermaid | Visual flow diagram — **only when content has a clear process, timeline, or decision flow** |

**Save the HTML file to:** `/Users/mpedroso/CintVibe/KOunitedPortal/KOunitedVault/Meeting-Notes/HTML pages/`
All other files are presented inline unless the user requests saving them.

**Only generate models that fit the content.** If a meeting had no questions or demos, skip the Q&A model and explain why. Don't force structure onto content that doesn't have it.

---

## §2 — Summary Models

Every summary starts with a **single concise executive context paragraph**: what the meeting was about, why it happened, and which people were involved (name their roles in relation to the topics they raised).

---

### Model 1 — Thematic
*Best for: brainstorming, workshops, strategy sessions with multiple distinct topics.*

```
## [Meeting Title] — Thematic Summary

[Executive context paragraph]

### Topic A: [Name]
[Summary of discussion points and any divergent opinions]

### Topic B: [Name]
[Key insights and ideas generated]

### Topic C: [Name]
[Critical dates, commitments, or constraints mentioned]

### Conclusion
[General group sentiment and closing remarks]
```

---

### Model 2 — Adapted Cornell
*Best for: training sessions, retrospectives, post-mortems.*

```
## [Meeting Title] — Cornell Summary

[Executive context paragraph]

### Key Points
[Central keywords, concepts, and names discussed]

### Detailed Notes
[Full body: specific details, nuances, quotes worth preserving]

### Final Summary
[3–5 line synthesis capturing the essence of the meeting]
```

---

### Model 3 — Direct Executive
*Best for: quick syncs, project alignments, status updates.*

```
## [Meeting Title] — Executive Summary

[Executive context paragraph]

**Meeting Objective:** [One sentence on why the meeting happened]

**Key Decisions:**
1. [Decision]
2. [Decision]

**Action Items:**
| Task | Assignee | Deadline |
|------|----------|----------|
| [Task] | [Name] | [Date or TBD] |

**Next Steps:**
[What happens immediately after this meeting]
```

---

### Model 4 — Q&A
*Best for: product demos, feedback sessions, client FAQs.*

```
## [Meeting Title] — Q&A Summary

[Executive context paragraph]

**Presentation:** [Summary of the proposal, demo, or pitch presented]

**Questions & Answers:**
- **[Name] asked:** [Question] → [Summarized answer]
- **[Name] asked:** [Question] → [Summarized answer]

**Concerns Raised:**
[Friction points or open issues that still need resolution]

**Additional Resources:**
[Links, docs, or materials mentioned during the meeting]
```

---

## §3 — NotebookLM Prompt

Generate a ready-to-paste prompt the user can drop into NotebookLM to create a visual infographic. The prompt should:
- Reference the meeting by name
- Request a visual infographic using CI&T brand (Red `#E31B23`, Onyx `#1A1A1A`, Teal `#00B2BB`)
- Request Montserrat/Poppins for headings, Open Sans/Inter for body
- Use the Thematic Model structure for content and the Cornell Model for the executive intro and takeaways
- Ask for a modular card-based layout with high-contrast white space

---

## §4 — HTML Visual Infographic

Generate a **pure, self-contained HTML5/CSS3 file** with no external dependencies. All styles inside `<style>`, all icons as inline SVGs. No React, no JSX, no CDN links.

**Filename:** `{meeting-name}_{dd-MMM-yy}.html`
*(e.g. `KO-United-Sprint-Review_21-Apr-26.html`)*

**Save to:** `/Users/mpedroso/CintVibe/KOunitedPortal/KOunitedVault/Meeting-Notes/HTML pages/`

### Content structure (inside the HTML):
- **Header/Hero:** Meeting title, date, attendees list
- **Executive Intro:** Cornell Model executive paragraph (learning-focused intro)
- **Main Body:** Thematic Model cards (one card per topic) + Q&A Model section (if applicable)
- **Takeaways:** Cornell Model key takeaways and final synthesis
- **Action Items:** Executive Model action items table (if applicable)

### CI&T Red-Line Enterprise Styleguide (embed verbatim):

```css
/* === CI&T RED-LINE ENTERPRISE IDENTITY === */

/* Palette */
--color-primary: #E31B23;      /* CI&T Red — critical data, active UI */
--color-secondary: #1A1A1A;    /* Deep Onyx — headings, backgrounds */
--color-accent: #00B2BB;       /* Teal/Cyan — AI intelligence, collaboration */
--color-bg: #FFFFFF;
--color-surface: #F5F5F5;
--color-border: #E0E0E0;
--color-text: #2D2D2D;
--color-text-muted: #6B6B6B;

/* Typography */
--font-heading: 'Montserrat', 'Poppins', system-ui, sans-serif;
--font-body: 'Open Sans', 'Inter', system-ui, sans-serif;
--font-weight-heading: 800;    /* Extra Bold */
--font-weight-body: 400;

/* Layout */
/* Modular grid structure — anchored with strong vertical lines, airy enough for dense content */
/* Card-based layout, high-contrast white space between sections */
/* Maximum content width: 1200px, centered */
```

**Design rules:**
- Use `--color-primary` (#E31B23) for section headers, key data points, and active UI accents
- Use `--color-secondary` (#1A1A1A) for heavy headings and dark backgrounds
- Use `--color-accent` (#00B2BB) for AI/collaboration elements, highlights, and tags
- Card components have `border-left: 4px solid var(--color-primary)` as a structural accent
- Action items table uses alternating `#F5F5F5` / `#FFFFFF` rows
- All sections separated by generous white space — minimum `48px` between sections

---

## §5 — Mermaid Diagram

Generate only when the meeting content contains a **clear process flow, decision tree, timeline, or sequential steps**. Skip silently if the content is purely conversational or doesn't have a logical sequence.

If generated, use:
- `flowchart TD` for processes and decisions
- `timeline` for milestone/date-heavy content
- `sequenceDiagram` for multi-party interactions

---

## §6 — Delivery Sequence

1. Announce the meeting title and date you're using for filenames — confirm with user if uncertain
2. Generate and present Model 1 (Thematic) → wait briefly for user reaction before continuing, or proceed if user asked for all at once
3. Generate and present Models 2, 3, 4 in sequence
4. Generate and present NotebookLM prompt (§3)
5. Generate Mermaid diagram if applicable (§5)
6. Generate HTML infographic (§4) → save to the specified path → present the file link
7. Confirm what was saved where
