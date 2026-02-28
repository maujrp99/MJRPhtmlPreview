// =============================================================
// preview.js — Preview Engine (Base Href, Input Detection, Styles)
// =============================================================

const EMPTY_PREVIEW = "<style>body{font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;height:95vh;color:#8b949e;margin:0;}</style><div>Paste your HTML or Markdown here...</div>";
const BASE_HREF = window.location.href.substring(0, window.location.href.lastIndexOf('/') + 1) + 'images/';

// --- Input Type Detection (FR04.1) ---
function detectInputType(text) {
    const trimmed = text.trim();
    if (!trimmed) return 'html';

    // Check for raw Mermaid diagrams (user pasted just the diagram without markdown wrapper)
    const mermaidStartPattern = /^(graph\s|flowchart\s|sequenceDiagram|gantt|classDiagram|stateDiagram|pie|erDiagram|journey|gitGraph|mindmap|timeline|quadrantChart)/i;
    if (mermaidStartPattern.test(trimmed)) return 'mermaid_raw';

    // Check for common HTML block-level tags at the start
    const htmlStartPattern = /^(<\!DOCTYPE|<html|<head|<body|<div|<section|<table|<nav|<header|<footer|<main|<article|<style|<script|<link|<meta|<span|<p\s|<p>|<ul|<ol|<li|<form|<input|<button|<canvas|<svg)/i;
    if (htmlStartPattern.test(trimmed)) return 'html';
    // Check for significant HTML tags in the first 500 chars (but not markdown with inline html)
    const sample = trimmed.substring(0, 500);
    const htmlTagCount = (sample.match(/<[a-z][a-z0-9]*[\s>]/gi) || []).length;
    // If there are many HTML tags, it's likely HTML
    if (htmlTagCount >= 3) return 'html';
    return 'markdown';
}

// --- Base Href Injection ---
function injectBaseHref(html) {
    if (/<base\s/i.test(html)) return html;
    if (/<head[^>]*>/i.test(html)) {
        return html.replace(/<head[^>]*>/i, `$&<base href="${BASE_HREF}">`);
    }
    return `<base href="${BASE_HREF}">` + html;
}

// --- Markdown Stylesheet (FR04.4) ---
const MD_STYLES = `<style>
    body {
        font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
        line-height: 1.6;
        max-width: 800px;
        margin: 0 auto;
        padding: 24px;
        color: #1f2328;
    }
    h1, h2, h3, h4, h5, h6 {
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
        line-height: 1.25;
    }
    h1 { font-size: 2em; border-bottom: 1px solid #d0d7de; padding-bottom: 8px; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #d0d7de; padding-bottom: 6px; }
    h3 { font-size: 1.25em; }
    code {
        background: #f6f8fa;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.875em;
        font-family: 'JetBrains Mono', monospace;
    }
    pre {
        background: #f6f8fa;
        padding: 16px;
        border-radius: 6px;
        overflow-x: auto;
        border: 1px solid #d0d7de;
    }
    pre code { background: none; padding: 0; }
    blockquote {
        border-left: 4px solid #58a6ff;
        padding: 8px 16px;
        margin: 16px 0;
        color: #656d76;
        background: #f6f8fa;
    }
    table { border-collapse: collapse; width: 100%; margin: 16px 0; }
    th, td { border: 1px solid #d0d7de; padding: 8px 12px; text-align: left; }
    th { background: #f6f8fa; font-weight: 600; }
    a { color: #58a6ff; }
    img { max-width: 100%; }
    hr { border: none; border-top: 1px solid #d0d7de; margin: 24px 0; }
    ul, ol { padding-left: 24px; }
    li { margin: 4px 0; }
</style>`;

function wrapWithMdStyles(html) {
    return MD_STYLES + html;
}

// --- Mermaid Lazy Load (FR04.3) ---
let mermaidLoaded = false;

function initMermaidIfNeeded(iframeDoc) {
    if (!iframeDoc) return;
    const mermaidBlocks = iframeDoc.querySelectorAll('code.language-mermaid');
    if (mermaidBlocks.length === 0) return;

    if (!mermaidLoaded) {
        const script = iframeDoc.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js';
        script.onload = () => {
            mermaidLoaded = true;
            renderMermaid(iframeDoc);
        };
        iframeDoc.head.appendChild(script);
    } else {
        // Re-inject mermaid into this iframe
        const script = iframeDoc.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js';
        script.onload = () => renderMermaid(iframeDoc);
        iframeDoc.head.appendChild(script);
    }
}

function renderMermaid(iframeDoc) {
    const blocks = iframeDoc.querySelectorAll('code.language-mermaid');
    blocks.forEach(block => {
        const pre = block.parentElement;
        const div = iframeDoc.createElement('div');
        div.className = 'mermaid';
        div.textContent = block.textContent;
        pre.replaceWith(div);
    });

    try {
        iframeDoc.defaultView.mermaid.initialize({ startOnLoad: false, theme: 'default' });
        iframeDoc.defaultView.mermaid.run();
    } catch (e) {
        console.warn('Mermaid render failed:', e);
    }
}

// --- Main Render Pipeline ---
function renderPreview(raw, previewFrame) {
    if (!raw.trim()) {
        previewFrame.srcdoc = EMPTY_PREVIEW;
        return;
    }

    const inputType = detectInputType(raw);

    if (inputType === 'html') {
        previewFrame.srcdoc = injectBaseHref(raw);
    } else {
        // Markdown pipeline
        let markdownContent = raw;
        if (inputType === 'mermaid_raw') {
            // Auto-wrap raw mermaid code in a markdown block so marked.js can parse it correctly
            markdownContent = '```mermaid\n' + raw.trim() + '\n```';
        }

        const parsedHtml = marked.parse(markdownContent);
        const styled = wrapWithMdStyles(parsedHtml);
        previewFrame.srcdoc = injectBaseHref(styled);

        // After iframe loads, check for mermaid blocks
        previewFrame.onload = () => {
            const iframeDoc = previewFrame.contentDocument;
            if (iframeDoc) initMermaidIfNeeded(iframeDoc);
        };
    }
}
