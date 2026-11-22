from flask import Flask, request, jsonify, render_template_string
import requests
import time
import rolimons  # --- TAMBAHAN BARU ---

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>R0bl0x F1lt3r</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    :root {
        --bg-color: #0f172a;
        --panel-bg: #1e293b;
        --text-main: #e2e8f0;
        --text-muted: #94a3b8;
        --border-color: #334155;
        --primary: #3b82f6;
        --primary-hover: #2563eb;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --purple: #a855f7;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body { 
        background-color: var(--bg-color); 
        color: var(--text-main); 
        font-family: 'Inter', sans-serif; 
        padding: 20px 15px; 
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .container {
        width: 100%;
        max-width: 850px;
    }

    .header { margin-bottom: 20px; }
    .header h2 { font-size: 22px; font-weight: 700; color: #fff; }
    .header p { font-size: 13px; color: var(--text-muted); margin-top: 5px; }

    .input-group {
        background: var(--panel-bg);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-bottom: 25px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    textarea { 
        width: 100%; 
        height: 100px; 
        background-color: #0b1120; 
        color: #60a5fa; 
        border: 1px solid var(--border-color); 
        border-radius: 8px;
        padding: 12px; 
        font-family: 'Inter', monospace; 
        font-size: 13px;
        resize: vertical;
        transition: border-color 0.2s;
        margin-bottom: 10px;
    }
    textarea:focus { outline: none; border-color: var(--primary); }

    .btn-group {
        display: flex;
        gap: 8px;
        margin-top: 5px;
    }

    button, .btn-upload { 
        background-color: var(--primary); 
        color: white; 
        border: none; 
        padding: 12px 15px; 
        cursor: pointer; 
        font-weight: 600; 
        border-radius: 6px; 
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        transition: all 0.2s, transform 0.1s;
        flex: 1;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        box-sizing: border-box;
        height: 42px;
    }

    button:hover:not(:disabled), .btn-upload:hover { background-color: var(--primary-hover); }
    button:active:not(:disabled), .btn-upload:active { transform: scale(0.98); }
    button:disabled { background-color: #475569; cursor: not-allowed; opacity: 0.7; }

    .btn-danger { background-color: var(--danger); }
    .btn-danger:hover:not(:disabled) { background-color: #dc2626; }

    input[type="file"] { display: none; }

    /* --- LAYOUT LIST SIMPEL --- */
    .results-list {
        display: flex;
        flex-direction: column;
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        overflow: hidden;
    }

    .result-row {
        padding: 12px 15px;
        border-bottom: 1px solid var(--border-color);
        display: flex;
        flex-direction: column;
        gap: 8px;
        transition: background 0.2s;
    }
    .result-row:last-child { border-bottom: none; }
    .result-row:hover { background: #1e293b; }

    /* Baris Atas */
    .row-top {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        color: #fff;
    }
    
    /* NOMOR URUT DIPERBARUI: Tanpa kotak biru, abu-abu */
    .row-number {
        color: var(--text-muted);
        font-size: 12px;
        font-weight: 600;
        margin-right: 4px;
        flex-shrink: 0;
    }

    .main-text { font-weight: 600; color: #fff; }
    .label-text { color: var(--text-muted); font-weight: 400; font-size: 12px; }
    .country-text { color: var(--warning); font-weight: 500; font-size: 12px; margin-left: auto; }
    
    /* Baris Bawah */
    .row-bottom {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-left: 20px;
    }

    .row-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        border: 1px solid var(--border-color);
        object-fit: cover;
        background: #0b1120;
        flex-shrink: 0;
    }

    .row-info {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 10px;
        flex: 1;
        font-size: 11px;
    }

    /* Teks Status Minimalis */
    .stat-item {
        display: flex;
        align-items: center;
        gap: 4px;
        color: var(--text-muted);
    }
    .stat-item b { font-weight: 600; }
    .stat-yes { color: var(--success); }
    .stat-rap { color: var(--purple); }

    /* Status Not Found */
    .not-found-box {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--danger);
        font-weight: 600;
        font-size: 12px;
        padding-left: 20px;
    }

    /* Custom Modal */
    .modal-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(4px);
        display: flex; align-items: center; justify-content: center;
        z-index: 9999; opacity: 0; visibility: hidden; transition: all 0.3s ease;
    }
    .modal-overlay.active { opacity: 1; visibility: visible; }
    .modal-box {
        background: var(--panel-bg); border: 1px solid var(--border-color);
        border-radius: 12px; padding: 20px; max-width: 300px; width: 90%;
        text-align: center; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        transform: translateY(20px); transition: transform 0.3s ease;
    }
    .modal-overlay.active .modal-box { transform: translateY(0); }
    .modal-icon { font-size: 30px; margin-bottom: 10px; }
    .modal-title { font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 8px; }
    .modal-message { font-size: 13px; color: var(--text-muted); margin-bottom: 20px; line-height: 1.4; }
    .modal-btn {
        background: var(--primary); color: white; border: none;
        padding: 8px 15px; border-radius: 6px; font-weight: 600;
        font-size: 13px; cursor: pointer; width: 100%; transition: background 0.2s;
    }
    .modal-btn:hover { background: var(--primary-hover); }

    @media (max-width: 600px) {
        .btn-group { flex-direction: column; }
        .row-top { font-size: 12px; }
        .country-text { margin-left: 0; width: 100%; display: block; margin-top: 2px; }
        .row-bottom { padding-left: 0; }
        .not-found-box { padding-left: 0; }
    }

</style>
</head>
<body>

<div class="container">
    <div class="header">
        <h2>R0bl0x F1lt3r</h2>
        <p>Format Input: <b>usn:pw:ip</b></p>
    </div>

    <div class="input-group">
        <textarea id="data" placeholder="kalzatore:99999999:38.114.120.212"></textarea>
        
        <div class="btn-group">
            <label for="fileInput" class="btn-upload">📁 Upload .txt</label>
            <input type="file" id="fileInput" accept=".txt" onchange="handleFileUpload(event)">
            <button id="filterBtn" onclick="startFilter()">Mulai Filter</button>
            <button id="stopBtn" class="btn-danger" onclick="stopFilter()" disabled>Stop</button>
        </div>
    </div>

    <div id="results" class="results-list"></div>
</div>

<div class="modal-overlay" id="customModal">
    <div class="modal-box">
        <div class="modal-icon">⚠️</div>
        <div class="modal-title" id="modalTitle">Peringatan</div>
        <div class="modal-message" id="modalMessage">Pesan peringatan.</div>
        <button class="modal-btn" onclick="closeModal()">Oke</button>
    </div>
</div>

<script>
let isProcessing = false;
let currentAbortController = null;

function showModal(title, message) {
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalMessage').innerText = message;
    document.getElementById('customModal').classList.add('active');
}

function closeModal() {
    document.getElementById('customModal').classList.remove('active');
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('data').value = e.target.result;
    };
    reader.readAsText(file);
    event.target.value = '';
}

function stopFilter() {
    if (currentAbortController) currentAbortController.abort();
    isProcessing = false;
    updateButtons();
}

function updateButtons() {
    const btnFilter = document.getElementById('filterBtn');
    const btnStop = document.getElementById('stopBtn');
    
    if (isProcessing) {
        btnFilter.disabled = true;
        btnFilter.innerText = "Proses...";
        btnStop.disabled = false;
    } else {
        btnFilter.disabled = false;
        btnFilter.innerText = "Mulai Filter";
        btnStop.disabled = true;
    }
}

// Fungsi Fetch dengan Auto-Retry (Mengatasi error saat pindah app)
async function fetchWithRetry(url, options, retries = 3, backoff = 1000) {
    try {
        const res = await fetch(url, options);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        return res;
    } catch (e) {
        if (retries > 0 && e.name !== 'AbortError') {
            await new Promise(resolve => setTimeout(resolve, backoff));
            return fetchWithRetry(url, options, retries - 1, backoff * 1.5);
        }
        throw e;
    }
}

async function startFilter() {
    if (isProcessing) return;
    
    const lines = document.getElementById('data').value.split('\\n').filter(l => l.trim());
    const resultsContainer = document.getElementById('results');
    
    if(lines.length === 0) {
        showModal("Data Kosong", "Masukkan data terlebih dahulu!");
        return;
    }
    
    resultsContainer.innerHTML = '';
    isProcessing = true;
    updateButtons();

    let counter = 1;

    for (let line of lines) {
        if (!isProcessing) break;

        let parts = line.split(':');
        if(parts.length >= 3) {
            let usn = parts[0].trim();
            let pw = parts[1].trim();
            let ip = parts[2].trim();
            let numStr = counter.toString(); // Hapus angka 0 di depan
            
            // Loading Row
            let row = document.createElement('div');
            row.className = 'result-row';
            row.innerHTML = `
                <div class="row-top">
                    <span class="row-number">${numStr}.</span>
                    <span class="label-text">USN:</span> <span class="main-text">${usn}</span> <span class="label-text">| PW:</span> <span class="main-text">${pw}</span>
                    <span class="country-text">Loading...</span>
                </div>
            `;
            resultsContainer.appendChild(row);
            counter++;

            try {
                currentAbortController = new AbortController();
                const signal = currentAbortController.signal;

                // GUNAKAN fetchWithRetry
                let res = await fetchWithRetry('/filter', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({usn: usn, ip: ip}),
                    signal: signal
                });
                
                let data = await res.json();
                
                if (data.status === 'Not Found') {
                    row.innerHTML = `
                        <div class="row-top">
                            <span class="row-number" style="color:var(--danger)">${numStr}.</span>
                            <span class="label-text" style="color:var(--danger)">USN:</span> <span class="main-text" style="color:var(--danger)">${usn}</span> <span class="label-text">| PW:</span> <span class="main-text" style="color:var(--danger)">${pw}</span>
                        </div>
                        <div class="not-found-box">
                            <div class="row-avatar" style="display:flex; align-items:center; justify-content:center; color:var(--danger); font-size:10px;">X</div>
                            <span>Banned / Not Found</span>
                        </div>
                    `;
                } else {
                    let imgTag = data.avatar ? `<img src="${data.avatar}" class="row-avatar" loading="lazy">` : `<div class="row-avatar" style="display:flex; align-items:center; justify-content:center;">N/A</div>`;
                    
                    let korblox = data.korblox ? `<span class="stat-item stat-yes">● Korblox: <b>Yes</b></span>` : `<span class="stat-item">○ Korblox: <b>No</b></span>`;
                    let korles = data.korles ? `<span class="stat-item stat-yes">● Korles: <b>Yes</b></span>` : `<span class="stat-item">○ Korles: <b>No</b></span>`;
                    let mali = data.malivinus ? `<span class="stat-item stat-yes">● Malivinus: <b>Yes</b></span>` : `<span class="stat-item">○ Malivinus: <b>No</b></span>`;
                    let bit8 = data.crown_8bit ? `<span class="stat-item stat-yes">● 8Bit: <b>Yes</b></span>` : `<span class="stat-item">○ 8Bit: <b>No</b></span>`;
                    
                    let rapText = data.rap > 0 ? `<span class="stat-item stat-rap">● RAP: <b>${data.rap.toLocaleString()}</b></span>` : `<span class="stat-item">○ RAP: <b>Priv/None</b></span>`;

                    row.innerHTML = `
                        <div class="row-top">
                            <span class="row-number">${numStr}.</span>
                            <span class="label-text">USN:</span> <span class="main-text">${usn}</span> <span class="label-text">| PW:</span> <span class="main-text">${pw}</span> <span class="label-text">| IP:</span> <span class="main-text">${data.country}</span>
                        </div>
                        <div class="row-bottom">
                            ${imgTag}
                            <div class="row-info">
                                <span class="stat-item" style="color:var(--text-main); font-weight:500;">📅 ${data.created}</span>
                                ${korblox}
                                ${korles}
                                ${mali}
                                ${bit8}
                                ${rapText}
                            </div>
                        </div>
                    `;
                }
            } catch (e) {
                if (e.name === 'AbortError') {
                    row.innerHTML = `
                        <div class="row-top">
                            <span class="row-number" style="color:var(--warning)">${numStr}.</span>
                            <span class="label-text" style="color:var(--warning)">Dibatalkan.</span>
                        </div>
                    `;
                    break;
                } else {
                    row.innerHTML = `
                        <div class="row-top">
                            <span class="row-number" style="color:var(--danger)">${numStr}.</span>
                            <span class="main-text" style="color:var(--danger)">Gagal terhubung ke server (Error Jaringan).</span>
                        </div>
                    `;
                }
            }
            currentAbortController = null;
        }
    }
    
    isProcessing = false;
    updateButtons();
}
</script>
</body>
</html>
"""

# --- HEADLESS ---
HEADLESS_IDS = [
    15093053680, 131592085, 134082453, 134082473, 134082507, 
    134082533, 134082557, 131929448, 11573370910, 23452365716, 
    134082579, 134082613, 201
]

# --- KORBLOX ---
KORBLOX_IDS = [139607718, 139607917, 2988500]

# --- MALIVINUS ---
MALIVINUS_IDS = [
    2807147467, 2807142069, 2807144777, 
    2807143328, 2807146071, 126200552021824
]

# --- 8-BIT ROYAL CROWN ---
EIGHT_BIT_CROWN_IDS = [10159600649, 85696590060559]

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/filter', methods=['POST'])
def filter_account():
    data = request.json
    usn = data.get('usn')
    ip_addr = data.get('ip')
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'application/json'
    })
    
    country_name = "Unknown"
    if ip_addr:
        try:
            ip_req = requests.get(f'http://ip-api.com/json/{ip_addr}?fields=status,country', timeout=5)
            if ip_req.status_code == 200 and ip_req.json().get('status') == 'success':
                country_name = ip_req.json().get('country', 'Unknown')
        except Exception:
            country_name = "IP Error"
    
    try:
        user_req = session.post('https://users.roblox.com/v1/usernames/users', json={
            'usernames': [usn],
            'excludeBannedUsers': False
        })
        
        if user_req.status_code != 200 or not user_req.json().get('data'):
            return jsonify({'status': 'Not Found', 'country': country_name})
            
        user_data = user_req.json()['data'][0]
        user_id = user_data['id']
        
        time.sleep(0.2)
        
        info_req = session.get(f'https://users.roblox.com/v1/users/{user_id}')
        created_date = "Unknown"
        if info_req.status_code == 200:
            created_raw = info_req.json().get('created', '')
            if created_raw:
                created_date = created_raw.split('T')[0]

        time.sleep(0.2)
        
        avatar_req = session.get(f'https://avatar.roblox.com/v1/users/{user_id}/avatar')
        
        has_headless = False
        has_korblox = False
        has_malivinus = False
        has_crown_8bit = False
        
        if avatar_req.status_code == 200:
            assets = avatar_req.json().get('assets', [])
            for asset in assets:
                asset_id = asset.get('id')
                if asset_id in HEADLESS_IDS:
                    has_headless = True
                if asset_id in KORBLOX_IDS:
                    has_korblox = True
                if asset_id in MALIVINUS_IDS:
                    has_malivinus = True
                if asset_id in EIGHT_BIT_CROWN_IDS: 
                    has_crown_8bit = True
                    
        time.sleep(0.2)
        
        thumb_req = session.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=true')
        avatar_url = None
        if thumb_req.status_code == 200:
            thumb_data = thumb_req.json().get('data', [])
            if thumb_data:
                avatar_url = thumb_data[0].get('imageUrl')
        
        time.sleep(0.2)
        
        # --- BAGIAN RAP ROLIMONS DENGAN LIBRARY ---
        rap_val = 0
        ltd_val = 0
        try:
            player_info = rolimons.player.get_player_info(user_id)
            
            if player_info and 'rap' in player_info:
                rap_val = player_info['rap']
                ltd_val = player_info.get('num_limiteds', 0)
        except Exception as e:
            print(f"Log Error RAP: {e}") 
        # -------------------------------------------------------------------
                
        return jsonify({
            'status': 'Found',
            'country': country_name,
            'created': created_date,
            'avatar': avatar_url,
            'korblox': has_korblox,
            'korles': has_korblox and has_headless,
            'rap': rap_val,
            'limiteds': ltd_val,
            'malivinus': has_malivinus,
            'crown_8bit': has_crown_8bit
        })
        
    except Exception as e:
        return jsonify({'status': 'Error', 'country': country_name})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
