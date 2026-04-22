// =============================================================
// app.js — Bootstrap & Event Wiring
// =============================================================
// No DOMContentLoaded needed — this script loads at end of <body>,
// so all DOM elements are already available.

// DOM References
const htmlInput = document.getElementById('htmlInput');
const previewFrame = document.getElementById('previewFrame');
const btnClear = document.getElementById('btnClear');
const btnDrive = document.getElementById('btnDrive');
const btnOpen = document.getElementById('btnOpen');
const fileInput = document.getElementById('fileInput');
const fileNameLabel = document.getElementById('fileNameLabel');
const btnEdit = document.getElementById('btnEdit');

// --- Initialize Modules ---
initSettingsModal();       // drive.js
initDriveButton(btnDrive, htmlInput);  // drive.js
initExportButtons(htmlInput, previewFrame); // export.js
tryInitGoogle();           // drive.js

// --- Core: Real-time Preview ---
htmlInput.addEventListener('input', () => {
    renderPreview(htmlInput.value, previewFrame); // preview.js
});

// --- Clear Editor ---
btnClear.addEventListener('click', () => {
    htmlInput.value = '';
    previewFrame.srcdoc = EMPTY_PREVIEW; // preview.js constant
    fileNameLabel.textContent = '';
    htmlInput.focus();
});

// --- File Picker (M5) ---
btnOpen.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    fileNameLabel.textContent = file.name;

    const reader = new FileReader();
    reader.onload = (event) => {
        const content = event.target.result;
        htmlInput.value = content;
        renderPreview(content, previewFrame);
    };
    reader.readAsText(file);
    
    // Reset input so the same file can be selected again
    fileInput.value = '';
});

// --- Fullscreen Preview Toggle ---
const mainEl = document.querySelector('main');
const btnToggleView = document.getElementById('btnToggleView');
const btnBackToEditor = document.getElementById('btnBackToEditor');
const previewToolbar = document.getElementById('previewToolbar');

btnToggleView.addEventListener('click', () => {
    mainEl.classList.add('fullscreen-preview');
    previewToolbar.style.display = 'flex';
});

btnBackToEditor.addEventListener('click', () => {
    mainEl.classList.remove('fullscreen-preview');
    previewToolbar.style.display = 'none';
});

// --- Visual Edit Toggle ---
// Implemented via initEditMode in preview.js
if (typeof initEditMode === 'function') {
    initEditMode(btnEdit, previewFrame, htmlInput);
}

// Focus on editor
htmlInput.focus();

console.log('[MJRPhtmlPreview] All modules initialized successfully.');
