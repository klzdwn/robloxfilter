from flask import Flask, request, jsonify, render_template_string
import requests
import time
import rolimons
import ipaddress # <-- Tambahan untuk cek IPv6

app = Flask(__name__)

# ... (Bagian HTML_PAGE tetap sama persis seperti yang kamu kirim sebelumnya) ...
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
        padding: 15px 10px; 
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .container {
        width: 100%;
        max-width: 1000px;
    }

    .header { margin-bottom: 15px; text-align: center; }
    .header h2 { font-size: 20px; font-weight: 700; color: #fff; }
    .header p { font-size: 12px; color: var(--text-muted); margin-top: 5px; }

    .input-group {
        background: var(--panel-bg);
        padding: 12px;
        border-radius: 10px;
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    textarea { 
        width: 100%; 
        height: 90px; 
        background-color: #0b1120; 
        color: #60a5fa; 
        border: 1px solid var(--border-color); 
        border-radius: 6px;
        padding: 10px; 
        font-family: 'Inter', monospace; 
        font-size: 12px;
        resize: vertical;
        margin-bottom: 10px;
    }
    textarea:focus { outline: none; border-color: var(--primary); }

    .btn-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
    }

    button, .btn-upload { 
        background-color: var(--primary); 
        color: white; 
        border: none; 
        padding: 10px 12px; 
        cursor: pointer; 
        font-weight: 600; 
        border-radius: 6px; 
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 38px;
        width: 100%;
    }

    button:hover:not(:disabled), .btn-upload:hover { background-color: var(--primary-hover); }
    button:disabled { background-color: #475569; cursor: not-allowed; opacity: 0.7; }
    
    .btn-warning { background-color: var(--warning); color: #000; }
    .btn-warning:hover:not(:disabled) { background-color: #d97706; }
    
    .btn-success { background-color: var(--success); }
    .btn-success:hover:not(:disabled) { background-color: #059669; }

    input[type="file"] { display: none; }

    .warning-text {
        display: flex;
        align-items: flex-start;
        justify-content: center;
        gap: 6px;
        font-size: 11px;
        color: var(--warning);
        margin-top: 12px;
        text-align: left;
    }
    .warning-text .icon { font-size: 12px; line-height: 1.2;}

    .table-wrapper {
        width: 100%;
        background: var(--panel-bg);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        overflow: hidden; 
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 11px;
    }

    th, td {
        padding: 8px 6px;
        border-bottom: 1px solid var(--border-color);
        text-align: left;
        vertical-align: middle;
    }

    th {
        background-color: #0b1120;
        color: var(--text-muted);
        font-weight: 600;
        font-size: 10px;
        text-transform: uppercase;
        white-space: nowrap; 
    }

    th.col-ip { 
        text-align: center; 
        padding-left: 15px; 
    }

    tr:hover { background-color: rgba(255, 255, 255, 0.02); }

    .col-num { width: 20px; text-align: center; color: var(--text-muted); }
    .col-avatar { width: 35px; text-align: center; padding: 4px;}
    .col-avatar img { width: 28px; height: 28px; border-radius: 50%; border: 1px solid var(--border-color); object-fit: cover; }
    .col-usn { font-weight: 600; color: #fff; word-break: break-all; max-width: 80px;}
    .col-pw { color: var(--text-muted); word-break: break-all; max-width: 70px;}
    .col-ip { color: var(--warning); max-width: 60px; word-break: break-word; text-align: center;}
    
    .col-status { min-width: 100px; line-height: 1.3;}
    .status-line { display: block; white-space: nowrap; font-size: 10px;}
    .status-label { color: var(--text-muted); }
    
    .col-rap { text-align: right; font-weight: bold; white-space: nowrap;}

    .txt-yes { color: var(--success); font-weight: 700; }
    .txt-no { color: var(--danger); }
    .txt-rap { color: var(--purple); }
    
    .txt-error { 
        color: var(--danger); 
        font-style: italic; 
        font-weight: 500;
        font-size: 10px;
    }

    .date-mobile { 
        display: block; 
        font-size: 9px; 
        color: var(--text-muted); 
        margin-top: 3px; 
        font-weight: 400;
        white-space: nowrap;
    }

    .col-date { display: none; }
    @media (min-width: 600px) {
        .col-date { display: table-cell; color: var(--text-muted); }
        th, td { padding: 10px 8px; font-size: 12px; }
        .col-usn { max-width: none; }
        .col-pw { max-width: none; }
        .col-ip { text-align: left; width: auto;}
        .date-mobile { display: none; } 
    }

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
        text-align: center; transform: translateY(20px); transition: transform 0.3s ease;
    }
    .modal-overlay.active .modal-box { transform: translateY(0); }
    .modal-icon { font-size: 30px; margin-bottom: 10px; }
    .modal-title { font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 8px; }
    .modal-message { font-size: 13px; color: var(--text-muted); margin-bottom: 20px; line-height: 1.4; }
    .modal-btn {
        background: var(--primary); color: white; border: none;
        padding: 8px 15px; border-radius: 6px; font-weight: 600;
        font-size: 13px; cursor: pointer; width: 100%;
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
        
        <div class="btn-grid">
            <label for="fileInput" class="btn-upload">📁 Upload .txt</label>
            <input type="file" id="fileInput" accept=".txt" onchange="handleFileUpload(event)">
            
            <button id="filterBtn" onclick="startFilter()">Mulai Filter</button>
            <button id="pauseBtn" class="btn-warning" onclick="pauseFilter()" disabled>Jeda</button>
            <button id="resumeBtn" class="btn-success" onclick="resumeFilter()" disabled>Lanjutkan</button>
        </div>

        <div class="warning-text">
            <span class="icon">⚠️</span> 
            <span>Tetap stay di website. Jika keluar, sistem akan menerapkan fitur jeda otomatis.</span>
        </div>
    </div>

    <div class="table-wrapper">
        <table id="resultTable">
            <thead>
                <tr>
                    <th class="col-num">#</th>
                    <th class="col-avatar">PFP</th>
                    <th class="col-usn">USN</th>
                    <th class="col-pw">PW</th>
                    <th class="col-ip">Negara</th>
                    <th class="col-date">Created</th>
                    <th class="col-status">Status Item</th>
                    <th class="col-rap">RAP</th>
                </tr>
            </thead>
            <tbody id="tableBody"></tbody>
        </table>
    </div>
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
let isPaused = false; 
let isStopped = false; 
let currentAbortController = null;

let currentLines = [];
let currentIndex = 0;

document.addEventListener("visibilitychange", function() {
    if (document.hidden) { 
        isPaused = true; 
    } else { 
        if (!isStopped) {
            isPaused = false; 
        }
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

function pauseFilter() {
    isPaused = true; 
    isStopped = true; 
    updateButtons();
}

function resumeFilter() {
    if (isProcessing && isPaused) {
        isPaused = false;
        isStopped = false;
        updateButtons();
    } else if (!isProcessing && currentIndex < currentLines.length) {
        isStopped = false;
        isPaused = false;
        isProcessing = true;
        updateButtons();
        processQueue();
    }
}

function updateButtons() {
    const btnFilter = document.getElementById('filterBtn');
    const btnPause = document.getElementById('pauseBtn');
    const btnResume = document.getElementById('resumeBtn');
    
    if (isProcessing) {
        btnFilter.disabled = true;
        btnFilter.innerText = "Proses...";
        btnPause.disabled = isPaused; 
        
        if (isPaused) {
            btnResume.disabled = false; 
        } else {
            btnResume.disabled = true;
        }
    } else {
        btnFilter.disabled = false;
        btnFilter.innerText = "Mulai Filter";
        btnPause.disabled = true;
        
        if (currentIndex < currentLines.length) {
            btnResume.disabled = false;
        } else {
            btnResume.disabled = true;
        }
    }
}

function startFilter() {
    if (isProcessing) return;
    
    currentLines = document.getElementById('data').value.split('\\n').filter(l => l.trim());
    if(currentLines.length === 0) {
        showModal("Data Kosong", "Masukkan data terlebih dahulu!");
        return;
    }
    
    document.getElementById('tableBody').innerHTML = '';
    currentIndex = 0; 
    isStopped = false;
    isPaused = false;
    isProcessing = true;
    currentAbortController = null;
    
    updateButtons();
    processQueue();
}

async function processQueue() {
    const tableBody = document.getElementById('tableBody');

    for (let i = currentIndex; i < currentLines.length; i++) {
        currentIndex = i; 

        if (!isProcessing) break; 

        while (isPaused && isProcessing) {
            await new Promise(resolve => setTimeout(resolve, 500)); 
        }
        if (!isProcessing) break; 

        let line = currentLines[i];
        let parts = line.split(':');
        
        if(parts.length >= 3) {
            let usn = parts[0].trim();
            let pw = parts[1].trim();
            let ip = parts[2].trim();
            let numStr = (i + 1).toString(); 
            
            let isEmail = usn.includes('@'); 

            let tr = document.createElement('tr');
            tr.id = `row-${i}`; 
            tr.innerHTML = `
                <td class="col-num">${numStr}</td>
                <td class="col-avatar">⏳</td>
                <td class="col-usn">${usn}</td>
                <td class="col-pw">${pw}</td>
                <td class="col-ip" colspan="4" style="color:var(--warning);">Loading...</td>
            `;
            tableBody.appendChild(tr);

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
                
                if (data.status === 'Not Found' || isEmail) {
                    let errorMsg = isEmail ? "Maaf data tidak ditemukan karena pakai email" : "Banned / Not Found";
                    tr.innerHTML = `
                        <td class="col-num">${numStr}</td>
                        <td class="col-avatar"><div style="display:flex; justify-content:center; align-items:center; width:28px; height:28px; background:#0b1120; border-radius:50%; color:var(--danger); font-size:10px; margin:auto;">X</div></td>
                        <td class="col-usn" style="color:var(--danger)">${usn}</td>
                        <td class="col-pw">${pw}</td>
                        <td colspan="4" class="txt-error">${errorMsg}</td>
                    `;
                } else {
                    let imgTag = data.avatar ? `<img src="${data.avatar}">` : `-`;
                    
                    let statusKorblox = data.korblox ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    let statusKorles = data.korles ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    let statusMali = data.malivinus ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    let status8bit = data.crown_8bit ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    
                    let statusHtml = `
                        <span class="status-line"><span class="status-label">Korblox:</span> ${statusKorblox}</span>
                        <span class="status-line"><span class="status-label">Korles:</span> ${statusKorles}</span>
                        <span class="status-line"><span class="status-label">Malivinus:</span> ${statusMali}</span>
                        <span class="status-line"><span class="status-label">8bit crown:</span> ${status8bit}</span>
                    `;

                    let rapText = data.rap > 0 ? `<span class="txt-rap">${data.rap.toLocaleString()}</span>` : `<span class="txt-no" style="font-size:10px;">Priv</span>`;

                    tr.innerHTML = `
                        <td class="col-num">${numStr}</td>
                        <td class="col-avatar">${imgTag}</td>
                        <td class="col-usn">${usn}</td>
                        <td class="col-pw">${pw}</td>
                        <td class="col-ip">
                            ${data.country}
                            <span class="date-mobile">${data.created}</span>
                        </td>
                        <td class="col-date">${data.created}</td>
                        <td class="col-status">${statusHtml}</td>
                        <td class="col-rap">${rapText}</td>
                    `;
                }
            } catch (e) {
                if (e.name === 'AbortError') {
                    tr.remove(); 
                    break; 
                } else {
                    tr.innerHTML = `
                        <td class="col-num">${numStr}</td>
                        <td class="col-avatar">X</td>
                        <td class="col-usn" style="color:var(--danger)">${usn}</td>
                        <td class="col-pw">${pw}</td>
                        <td colspan="4" class="txt-error">Koneksi terputus.</td>
                    `;
                }
            }
        }
    }
    
    if (isProcessing && currentIndex >= currentLines.length - 1) {
        isProcessing = false;
        isStopped = false;
        currentIndex = currentLines.length; 
        updateButtons();
    } else if (!isProcessing) {
        updateButtons();
    }
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
        # Pakai ipinfo.io yang lebih stabil
        ip_req = requests.get(f'https://ipinfo.io/{ip_addr}/json', timeout=5)
        if ip_req.status_code == 200:
            data_ip = ip_req.json()
            country_name = data_ip.get('country', 'Unknown')
            
            # (Opsional) Ubah kode negara jadi nama negara
            if country_name == 'ID': country_name = 'Indonesia'
            elif country_name == 'US': country_name = 'United States'
            elif country_name == 'PH': country_name = 'Philippines'
            # dst...
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
        
        time.sleep(0.1)
        
        info_req = session.get(f'https://users.roblox.com/v1/users/{user_id}')
        created_date = "Unknown"
        if info_req.status_code == 200:
            created_raw = info_req.json().get('created', '')
            if created_raw:
                created_date = created_raw.split('T')[0]

        time.sleep(0.1)
        
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
                    
        time.sleep(0.1)
        
        thumb_req = session.get(f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png&isCircular=true')
        avatar_url = None
        if thumb_req.status_code == 200:
            thumb_data = thumb_req.json().get('data', [])
            if thumb_data:
                avatar_url = thumb_data[0].get('imageUrl')
        
        time.sleep(0.1)
        
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
