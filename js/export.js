// =============================================================
// export.js — File Export (Download HTML, PDF, PNG)
// =============================================================

function generateTimestamp() {
    const now = new Date();
    return now.getFullYear().toString() +
        String(now.getMonth() + 1).padStart(2, '0') +
        String(now.getDate()).padStart(2, '0') + '_' +
        String(now.getHours()).padStart(2, '0') +
        String(now.getMinutes()).padStart(2, '0');
}

function initExportButtons(htmlInput, previewFrame) {
    const btnDownload = document.getElementById('btnDownload');
    const btnPdf = document.getElementById('btnPdf');
    const btnPng = document.getElementById('btnPng');

    // Download (HTML as .html, Markdown as .md)
    btnDownload.addEventListener('click', async () => {
        const content = htmlInput.value;
        if (!content.trim()) { alert("The editor is empty. Paste some content first!"); return; }

        const inputType = detectInputType(content);
        const isMarkdown = inputType === 'markdown' || inputType === 'mermaid_raw';
        const mimeType = isMarkdown ? 'text/markdown' : 'text/html';
        const ext = isMarkdown ? 'md' : 'html';
        const defaultFilename = `preview_${generateTimestamp()}.${ext}`;

        const blob = new Blob([content], { type: mimeType });

        // Modern API: Opens OS Save Dialog (Chrome, Edge, Safari 15.2+)
        if (window.showSaveFilePicker) {
            try {
                const handle = await window.showSaveFilePicker({
                    suggestedName: defaultFilename,
                    types: [{
                        description: isMarkdown ? 'Markdown Document' : 'HTML Document',
                        accept: { [mimeType]: [`.${ext}`] },
                    }],
                });
                const writable = await handle.createWritable();
                await writable.write(blob);
                await writable.close();
                return; // Successfully saved via native picker
            } catch (err) {
                // If user cancels the dialog, it throws an AbortError. We just silently return.
                if (err.name !== 'AbortError') console.error("File System API error:", err);
                return;
            }
        }

        // Fallback for browsers that don't support showSaveFilePicker (e.g., Firefox)
        const userFileName = prompt("Enter file name:", defaultFilename);
        if (!userFileName) return; // User cancelled

        // Ensure it has the correct extension
        const finalFilename = userFileName.endsWith(`.${ext}`) ? userFileName : `${userFileName}.${ext}`;

        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = finalFilename;
        document.body.appendChild(a);
        a.click();
        
        // Defer cleanup
        setTimeout(() => {
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }, 100);
    });

    // PDF via native print
    btnPdf.addEventListener('click', () => {
        const content = htmlInput.value;
        if (!content.trim()) { alert("The editor is empty. Paste some HTML first!"); return; }
        previewFrame.contentWindow.focus();
        previewFrame.contentWindow.print();
    });

    // PNG via html2canvas
    btnPng.addEventListener('click', async () => {
        const content = htmlInput.value;
        if (!content.trim()) { alert("The editor is empty. Paste some HTML first!"); return; }

        const origIcon = btnPng.innerHTML;
        try {
            btnPng.innerHTML = "Wait...";
            const iframeDoc = previewFrame.contentDocument || previewFrame.contentWindow.document;
            const canvas = await html2canvas(iframeDoc.body, {
                useCORS: true, allowTaint: true, backgroundColor: null
            });

            const imgData = canvas.toDataURL('image/png');
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = imgData;
            a.download = `preview_${generateTimestamp()}.png`;
            document.body.appendChild(a);
            a.click();
            setTimeout(() => {
                document.body.removeChild(a);
            }, 100);
            btnPng.innerHTML = origIcon;
        } catch (err) {
            console.error("Error generating PNG:", err);
            alert("Failed to generate PNG image.");
            btnPng.innerHTML = origIcon;
        }
    });
}
