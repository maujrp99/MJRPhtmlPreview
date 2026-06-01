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

// --- File Loader Helper ---
function loadAndRenderFile(file) {
    const name = file.name.toLowerCase();
    if (!name.endsWith('.html') && !name.endsWith('.htm') && !name.endsWith('.md')) {
        alert("Formato de arquivo não suportado! Por favor, utilize um arquivo HTML, HTM ou Markdown (.md).");
        return;
    }

    fileNameLabel.textContent = file.name;

    const reader = new FileReader();
    reader.onload = (event) => {
        const content = event.target.result;
        htmlInput.value = content;
        renderPreview(content, previewFrame);
    };
    reader.readAsText(file);
}

// --- File Picker (Modern & Classic Fallback) ---
btnOpen.addEventListener('click', async () => {
    if (window.showOpenFilePicker) {
        try {
            const [fileHandle] = await window.showOpenFilePicker({
                types: [{
                    description: 'HTML/Markdown Documents',
                    accept: {
                        'text/html': ['.html', '.htm'],
                        'text/markdown': ['.md']
                    }
                }],
                id: 'mjrp_document_picker',
                multiple: false
            });
            const file = await fileHandle.getFile();
            loadAndRenderFile(file);
        } catch (err) {
            // AbortError is thrown when user cancels the dialog, which is expected
            if (err.name !== 'AbortError') console.error("File System Picker error:", err);
        }
    } else {
        // Fallback for browsers that don't support showOpenFilePicker (e.g. Firefox)
        fileInput.click();
    }
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;

    loadAndRenderFile(file);
    
    // Reset input so the same file can be selected again
    fileInput.value = '';
});

// --- Drag & Drop Support ---
const dragOverlay = document.getElementById('dragOverlay');
let dragCounter = 0; // Ensures visual transitions are smooth with nested elements

// Prevent default browser drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    window.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
    }, false);
});

window.addEventListener('dragenter', () => {
    dragCounter++;
    dragOverlay.style.display = 'flex';
}, false);

window.addEventListener('dragleave', () => {
    dragCounter--;
    if (dragCounter === 0) {
        dragOverlay.style.display = 'none';
    }
}, false);

window.addEventListener('drop', (e) => {
    dragCounter = 0;
    dragOverlay.style.display = 'none';

    if (e.dataTransfer && e.dataTransfer.files.length > 0) {
        const file = e.dataTransfer.files[0];
        loadAndRenderFile(file);
    }
}, false);

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
