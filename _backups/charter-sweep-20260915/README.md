# MJRPhtmlPreview

Paste HTML, preview it instantly, save to Google Drive or your Obsidian vault.

## What is this?

A client-side web app for previewing AI-generated HTML and saving it where you need it. No backend, no accounts — just paste, see, save.

## Quick Start

```bash
# Clone
git clone https://github.com/[user]/MJRPhtmlPreview.git
cd MJRPhtmlPreview

# Open directly (no build step needed for MVP)
open src/index.html
```

## Features

- **Paste & Preview**: Textarea + real-time iframe rendering
- **Save to Google Drive**: OAuth2 + folder picker (personal & work accounts)
- **Save Locally**: Download as .html for Obsidian vault or anywhere else

## Project Docs

- [VISION.md](VISION.md) — Purpose and aesthetic direction
- [CHARTER.md](CHARTER.md) — Scope, goals, and roadmap
- [docs/specs/constitution.md](docs/specs/constitution.md) — Technical rules

## Tech Stack

Single HTML/JS/CSS file. Client-side only. Google APIs for Drive integration.

## License

Personal project — not licensed for distribution.
