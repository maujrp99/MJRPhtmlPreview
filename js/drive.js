// =============================================================
// drive.js — Google Drive Integration (OAuth, Picker, Upload)
// =============================================================

// BYOK State
let GOOGLE_CONFIG = JSON.parse(localStorage.getItem('mjrp_google_keys')) || { CLIENT_ID: '', API_KEY: '', APP_ID: '' };
let tokenClient;
let accessToken = null;
let gapiScriptLoaded = false;
let gisScriptLoaded = false;
let authClientInited = false;
let pickerInited = false;

// Callbacks from Google CDN scripts (called via onload in HTML)
function gapiLoaded() { gapiScriptLoaded = true; tryInitGoogle(); }
function gisLoaded() { gisScriptLoaded = true; tryInitGoogle(); }

async function tryInitGoogle() {
    const btnDrive = document.getElementById('btnDrive');
    if (!GOOGLE_CONFIG.CLIENT_ID || !GOOGLE_CONFIG.API_KEY || GOOGLE_CONFIG.CLIENT_ID.length < 5) return;

    // Init GIS Auth Client
    if (gisScriptLoaded && !authClientInited) {
        tokenClient = google.accounts.oauth2.initTokenClient({
            client_id: GOOGLE_CONFIG.CLIENT_ID,
            scope: 'https://www.googleapis.com/auth/drive.file',
            callback: '',
        });
        authClientInited = true;
    }

    // Init GAPI Picker
    if (gapiScriptLoaded && !pickerInited) {
        gapi.load('client:picker', async () => {
            await gapi.client.init({
                apiKey: GOOGLE_CONFIG.API_KEY,
                discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest']
            });
            pickerInited = true;
            maybeEnableDrive(btnDrive);
        });
    } else {
        maybeEnableDrive(btnDrive);
    }
}

function maybeEnableDrive(btnDrive) {
    if (authClientInited && pickerInited) {
        btnDrive.disabled = false;
        btnDrive.title = "Save to Google Drive Folder";
    }
}

function initDriveButton(btnDrive, htmlInput) {
    btnDrive.addEventListener('click', () => {
        const content = htmlInput.value;
        if (!content.trim()) {
            alert("The editor is empty. Paste some HTML first!");
            return;
        }

        tokenClient.callback = async (resp) => {
            if (resp.error !== undefined) { throw (resp); }
            accessToken = resp.access_token;
            createPicker(btnDrive, htmlInput);
        };

        if (accessToken === null) {
            tokenClient.requestAccessToken({ prompt: 'consent' });
        } else {
            tokenClient.requestAccessToken({ prompt: '' });
        }
    });
}

function createPicker(btnDrive, htmlInput) {
    const view = new google.picker.DocsView(google.picker.ViewId.FOLDERS)
        .setIncludeFolders(true)
        .setSelectFolderEnabled(true);

    const picker = new google.picker.PickerBuilder()
        .enableFeature(google.picker.Feature.NAV_HIDDEN)
        .setAppId(GOOGLE_CONFIG.APP_ID)
        .setOAuthToken(accessToken)
        .addView(view)
        .setDeveloperKey(GOOGLE_CONFIG.API_KEY)
        .setCallback((data) => pickerCallback(data, btnDrive, htmlInput))
        .build();

    picker.setVisible(true);
}

async function pickerCallback(data, btnDrive, htmlInput) {
    if (data[google.picker.Response.ACTION] === google.picker.Action.PICKED) {
        const doc = data[google.picker.Response.DOCUMENTS][0];
        const folderId = doc[google.picker.Document.ID];
        await uploadHtmlToDrive(folderId, btnDrive, htmlInput);
    }
}

async function uploadHtmlToDrive(folderId, btnDrive, htmlInput) {
    const DRIVE_ICON = '<svg class="icon" viewBox="0 0 24 24"><path d="M7.71,3.5L1.15,15L4.58,21L11.13,9.5M9.73,15L6.3,21H19.42L22.85,15M22.28,14L15.72,2.5H8.85L15.43,14H22.28Z"/></svg>';
    btnDrive.innerHTML = "Saving...";

    try {
        const content = htmlInput.value;
        const boundary = '-------314159265358979323846';
        const delimiter = "\r\n--" + boundary + "\r\n";
        const close_delim = "\r\n--" + boundary + "--";

        const now = new Date();
        const filename = "preview_" + now.getFullYear() + String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0') + "_" + String(now.getHours()).padStart(2, '0') + String(now.getMinutes()).padStart(2, '0') + ".html";

        const metadata = { name: filename, mimeType: 'text/html', parents: [folderId] };

        const multipartRequestBody =
            delimiter + 'Content-Type: application/json\r\n\r\n' + JSON.stringify(metadata) +
            delimiter + 'Content-Type: text/html\r\n\r\n' + content + close_delim;

        const request = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + accessToken,
                'Content-Type': 'multipart/related; boundary="' + boundary + '"'
            },
            body: multipartRequestBody
        });

        const response = await request.json();
        if (response.error) throw new Error(response.error.message);

        btnDrive.innerHTML = '<span style="color:var(--accent-green)">Saved!</span>';
        setTimeout(() => { btnDrive.innerHTML = DRIVE_ICON + ' Save'; }, 3000);

    } catch (error) {
        console.error("Error uploading to Drive:", error);
        alert("Failed to save to Drive. See console for details.");
        btnDrive.innerHTML = DRIVE_ICON + ' Save';
    }
}

// --- Settings Modal Logic ---
function initSettingsModal() {
    const btnSettings = document.getElementById('btnSettings');
    const settingsModal = document.getElementById('settingsModal');
    const btnSaveSettings = document.getElementById('btnSaveSettings');
    const btnCancelSettings = document.getElementById('btnCancelSettings');
    const inpClientId = document.getElementById('inpClientId');
    const inpApiKey = document.getElementById('inpApiKey');
    const inpAppId = document.getElementById('inpAppId');

    btnSettings.addEventListener('click', () => {
        inpClientId.value = GOOGLE_CONFIG.CLIENT_ID || '';
        inpApiKey.value = GOOGLE_CONFIG.API_KEY || '';
        inpAppId.value = GOOGLE_CONFIG.APP_ID || '';
        settingsModal.style.display = 'flex';
    });

    btnCancelSettings.addEventListener('click', () => {
        settingsModal.style.display = 'none';
    });

    btnSaveSettings.addEventListener('click', () => {
        GOOGLE_CONFIG = {
            CLIENT_ID: inpClientId.value.trim(),
            API_KEY: inpApiKey.value.trim(),
            APP_ID: inpAppId.value.trim()
        };
        localStorage.setItem('mjrp_google_keys', JSON.stringify(GOOGLE_CONFIG));
        settingsModal.style.display = 'none';
        tryInitGoogle();
    });
}
