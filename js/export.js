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

    // Download HTML (renders Markdown to HTML if needed)
    btnDownload.addEventListener('click', () => {
        const raw = htmlInput.value;
        if (!raw.trim()) { alert("The editor is empty. Paste some content first!"); return; }

        // If input is Markdown, download the rendered HTML with styles
        let content;
        if (detectInputType(raw) === 'markdown') {
            const parsedHtml = marked.parse(raw);
            content = '<!DOCTYPE html>\n<html>\n<head><meta charset="UTF-8">\n<title>Preview</title>\n</head>\n<body>\n' + wrapWithMdStyles(parsedHtml) + '\n</body>\n</html>';
        } else {
            content = raw;
        }

        const blob = new Blob([content], { type: 'text/html' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `preview_${generateTimestamp()}.html`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
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
            a.href = imgData;
            a.download = `preview_${generateTimestamp()}.png`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            btnPng.innerHTML = origIcon;
        } catch (err) {
            console.error("Error generating PNG:", err);
            alert("Failed to generate PNG image.");
            btnPng.innerHTML = origIcon;
        }
    });
}
