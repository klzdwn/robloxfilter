from flask import Flask, request, jsonify, render_template_string
import requests
import time
import rolimons

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
        --bg-color: #0b1120;
        --panel-bg: #151e2e;
        --text-main: #e2e8f0;
        --text-muted: #64748b;
        --border-color: #1e293b;
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
        padding: 15px 10px; 
        display: flex;
        flex-direction: column;
        align-items: center;
        font-size: 12px;
    }

    .container {
        width: 100%;
        max-width: 750px;
    }

    .header { margin-bottom: 15px; text-align: center; }
    .header h2 { font-size: 18px; font-weight: 700; color: #fff; letter-spacing: 0.5px;}
    .header p { font-size: 11px; color: var(--text-muted); margin-top: 3px; }

    .input-group {
        background: var(--panel-bg);
        padding: 12px;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    textarea { 
        width: 100%; 
        height: 80px; 
        background-color: #0b1120; 
        color: #93c5fd; 
        border: 1px solid var(--border-color); 
        border-radius: 6px;
        padding: 10px; 
        font-family: 'Inter', monospace; 
        font-size: 11px;
        resize: vertical;
        transition: border-color 0.2s;
        margin-bottom: 8px;
    }
    textarea:focus { outline: none; border-color: var(--primary); }

    .btn-group {
        display: flex;
        gap: 6px;
    }

    button, .btn-upload { 
        background-color: var(--primary); 
        color: white; 
        border: none; 
        padding: 8px 12px; 
        cursor: pointer; 
        font-weight: 600; 
        border-radius: 5px; 
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        transition: all 0.2s;
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 34px;
    }

    button:hover:not(:disabled), .btn-upload:hover { background-color: var(--primary-hover); }
    button:disabled { background-color: #334155; cursor: not-allowed; opacity: 0.7; }
    .btn-danger { background-color: var(--danger); }
    .btn-danger:hover:not(:disabled) { background-color: #dc2626; }

    input[type="file"] { display: none; }

    /* --- PERINGATAN DI BAWAH TOMBOL --- */
    .warning-text {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
        font-size: 10px;
        color: var(--warning);
        margin-top: 10px;
        text-align: center;
        opacity: 0.8;
    }

    /* --- LIST ELEGAN & KECIL --- */
    .results-list {
        display: flex;
        flex-direction: column;
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        overflow: hidden;
    }

    .result-row {
        padding: 10px 12px;
        border-bottom: 1px solid #1e293b;
        display: flex;
        flex-direction: column;
        gap: 6px;
    }
    .result-row:last-child { border-bottom: none; }
    .result-row:hover { background: #1a2436; }

    .row-top {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 5px;
        color: #fff;
    }
    
    .row-number {
        color: var(--text-muted);
        font-size: 11px;
        font-weight: 600;
        margin-right: 2px;
        min-width: 15px;
    }

    .main-text { font-weight: 600; color: #f8fafc; font-size: 12px;}
    .label-text { color: var(--text-muted); font-weight: 400; font-size: 11px; }
    
    .row-bottom {
        display: flex;
        align-items: center;
        gap: 10px;
        padding-left: 18px;
    }

    .row-avatar {
        width: 24px;
        height: 24px;
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
        gap: 8px;
        flex: 1;
        font-size: 10px;
    }

    .stat-item {
        display: flex;
        align-items: center;
        gap: 3px;
        color: #475569;
        font-weight: 500;
    }
    .stat-item b { font-weight: 600; color: #64748b;}
    
    .stat-yes { color: var(--success); font-weight: 600;}
    .stat-yes b { color: var(--success); }
    .stat-rap { color: var(--purple); font-weight: 600;}
    .stat-rap b { color: var(--purple); }
    
    .date-text { color: #94a3b8; }

    .not-found-box {
        display: flex;
        align-items: center;
        gap: 8px;
        color: var(--danger);
        font-weight: 600;
        font-size: 11px;
        padding-left: 18px;
    }

    .modal-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(3px);
        display: flex; align-items: center; justify-content: center;
        z-index: 9999; opacity: 0; visibility: hidden; transition: all 0.2s ease;
    }
    .modal-overlay.active { opacity: 1; visibility: visible; }
    .modal-box {
        background: var(--panel-bg); border: 1px solid var(--border-color);
        border-radius: 8px; padding: 15px; max-width: 280px; width: 90%;
        text-align: center; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        transform: translateY(10px); transition: transform 0.2s ease;
    }
    .modal-overlay.active .modal-box { transform: translateY(0); }
    .modal-icon { font-size: 24px; margin-bottom: 8px; }
    .modal-title { font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 5px; }
    .modal-message { font-size: 11px; color: var(--text-muted); margin-bottom: 15px; line-height: 1.4; }
    .modal-btn {
        background: var(--primary); color: white; border: none;
        padding: 8px 15px; border-radius: 5px; font-weight: 600;
        font-size: 11px; cursor: pointer; width: 100%;
    }

    @media (max-width: 600px) {
        .btn-group { flex-direction: column; }
        .country-text { margin-left: 0; width: 100%; display: block; }
    }

</style>
</head>
<body>

<div class="container">
    <div class="header">
        <h2>R0bl0x F1lt3r</h2>
        <p>usn:pw:ip</p>
    </div>

    <div class="input-group">
        <textarea id="data" placeholder="kalzatore:99999999:38.114.120.212"></textarea>
        
        <div class="btn-group">
            <label for="fileInput" class="btn-upload">📁 Upload .txt</label>
            <input type="file" id="fileInput" accept=".txt" onchange="handleFileUpload(event)">
            <button id="filterBtn" onclick="startFilter()">Mulai Filter</button>
            <button id="stopBtn" class="btn-danger" onclick="stopFilter()" disabled>Stop</button>
        </div>

        <!-- TEKS PERINGATAN BARU -->
        <div class="warning-text">
            <span>ℹ️</span> Tetap stay di website. Jika keluar, sistem akan menerapkan fitur jeda otomatis.
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
let isPaused = false;

document.addEventListener("visibilitychange", function() {
    if (document.hidden) {
        isPaused = true; 
    } else {
        isPaused = false; 
    }
});

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
    isPaused = false;
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

        while (isPaused && isProcessing) {
            await new Promise(resolve => setTimeout(resolve, 500)); 
        }
        if (!isProcessing) break; 

        let parts = line.split(':');
        if(parts.length >= 3) {
            let usn = parts[0].trim();
            let pw = parts[1].trim();
            let ip = parts[2].trim();
            let numStr = counter.toString(); 
            
            let row = document.createElement('div');
            row.className = 'result-row';
            row.innerHTML = `
                <div class="row-top">
                    <span class="row-number">${numStr}.</span>
                    <span class="label-text">USN:</span> <span class="main-text">${usn}</span> <span class="label-text">| PW:</span> <span class="main-text">${pw}</span>
                    <span class="label-text" style="color:var(--warning); margin-left:auto;">Loading...</span>
                </div>
            `;
            resultsContainer.appendChild(row);
            counter++;

            try {
                currentAbortController = new AbortController();
                const signal = currentAbortController.signal;

                let res = await fetch('/filter', {
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
                                <span class="stat-item date-text">📅 ${data.created}</span>
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
                            <span class="main-text" style="color:var(--danger)">Koneksi terputus (Error Jaringan).</span>
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
