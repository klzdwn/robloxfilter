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
        max-width: 1000px;
    }

    .header { margin-bottom: 20px; text-align: center; }
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
        gap: 10px;
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
        height: 40px;
    }

    button:hover:not(:disabled), .btn-upload:hover { background-color: var(--primary-hover); }
    button:active:not(:disabled), .btn-upload:active { transform: scale(0.98); }
    button:disabled { background-color: #475569; cursor: not-allowed; opacity: 0.7; }

    .btn-danger { background-color: var(--danger); }
    .btn-danger:hover:not(:disabled) { background-color: #dc2626; }

    input[type="file"] { display: none; }

    /* --- PERINGATAN DI BAWAH TOMBOL --- */
    .warning-text {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 5px;
        font-size: 11px;
        color: var(--warning);
        margin-top: 12px;
        text-align: center;
        opacity: 0.9;
    }

    /* --- TABEL (GRID) STYLING --- */
    .table-wrapper {
        width: 100%;
        overflow-x: auto; /* Agar bisa di-scroll ke kanan di HP */
        background: var(--panel-bg);
        border-radius: 10px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    table {
        width: 100%;
        min-width: 800px; /* Lebar minimum agar tidak gepeng */
        border-collapse: collapse;
        font-size: 12px;
        text-align: left;
    }

    th {
        background-color: #0b1120;
        color: var(--text-muted);
        font-weight: 600;
        padding: 12px 10px;
        border-bottom: 2px solid var(--border-color);
        white-space: nowrap;
    }

    td {
        padding: 10px;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-main);
        vertical-align: middle;
    }

    tr:hover { background-color: rgba(255, 255, 255, 0.02); }

    /* Kolom Spesifik */
    .col-num { width: 30px; text-align: center; color: var(--text-muted); font-weight: 600; }
    .col-usn { font-weight: 600; color: #fff; max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
    .col-pw { color: var(--text-muted); max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
    .col-ip { color: var(--warning); font-weight: 500; }
    .col-date { color: var(--text-muted); white-space: nowrap;}
    .col-avatar { width: 40px; text-align: center;}
    .col-avatar img { width: 32px; height: 32px; border-radius: 50%; border: 1px solid var(--border-color); object-fit: cover; }
    .col-status { white-space: nowrap; }
    
    /* Badge Warna */
    .txt-yes { color: var(--success); font-weight: 700; }
    .txt-no { color: var(--danger); font-weight: 500; }
    .txt-rap { color: var(--purple); font-weight: 700; }
    .txt-error { color: var(--danger); font-weight: 600; font-size: 11px;}

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

        <!-- Teks Peringatan Fixed -->
        <div class="warning-text">
            <span>ℹ️</span> Tetap stay di website. Jika keluar, sistem akan menerapkan fitur jeda otomatis.
        </div>
    </div>

    <!-- TABEL WRAPPER -->
    <div class="table-wrapper">
        <table id="resultTable">
            <thead>
                <tr>
                    <th class="col-num">No</th>
                    <th>USN</th>
                    <th>PW</th>
                    <th>Negara (IP)</th>
                    <th>Created</th>
                    <th>Avatar</th>
                    <th>Status</th>
                    <th>RAP</th>
                </tr>
            </thead>
            <tbody id="tableBody">
                <!-- Baris akan dimasukkan lewat JS -->
            </tbody>
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
    const tableBody = document.getElementById('tableBody');
    
    if(lines.length === 0) {
        showModal("Data Kosong", "Masukkan data terlebih dahulu!");
        return;
    }
    
    tableBody.innerHTML = '';
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
            
            // Cek apakah input berupa email
            let isEmail = usn.includes('@'); 

            // Buat baris Loading
            let tr = document.createElement('tr');
            tr.innerHTML = `
                <td class="col-num">${numStr}</td>
                <td class="col-usn">${usn}</td>
                <td class="col-pw">${pw}</td>
                <td class="col-ip" colspan="4" style="color:var(--warning);">Loading...</td>
            `;
            tableBody.appendChild(tr);
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
                
                // Jika Not Found ATAU input berupa email
                if (data.status === 'Not Found' || isEmail) {
                    let errorMsg = isEmail ? "Maaf data tidak ditemukan karena pakai email" : "Banned / Not Found";
                    tr.innerHTML = `
                        <td class="col-num" style="color:var(--danger)">${numStr}</td>
                        <td class="col-usn" style="color:var(--danger)">${usn}</td>
                        <td class="col-pw">${pw}</td>
                        <td colspan="5" class="txt-error">${errorMsg}</td>
                    `;
                } else {
                    let imgTag = data.avatar ? `<img src="${data.avatar}">` : `N/A`;
                    
                    let statusKorblox = data.korblox ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    let statusKorles = data.korles ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    let statusMali = data.malivinus ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    let status8bit = data.crown_8bit ? `<span class="txt-yes">Yes</span>` : `<span class="txt-no">No</span>`;
                    
                    // Gabungkan status dalam satu kolom
                    let statusHtml = `
                        <div style="line-height: 1.4;">
                            <span style="color:var(--text-muted); font-size:10px;">Korblox:</span> ${statusKorblox}<br>
                            <span style="color:var(--text-muted); font-size:10px;">Korles:</span> ${statusKorles}<br>
                            <span style="color:var(--text-muted); font-size:10px;">Mali:</span> ${statusMali}<br>
                            <span style="color:var(--text-muted); font-size:10px;">8Bit:</span> ${status8bit}
                        </div>
                    `;

                    let rapText = data.rap > 0 ? `<span class="txt-rap">${data.rap.toLocaleString()}</span>` : `<span class="txt-no">Priv/None</span>`;

                    tr.innerHTML = `
                        <td class="col-num">${numStr}</td>
                        <td class="col-usn">${usn}</td>
                        <td class="col-pw">${pw}</td>
                        <td class="col-ip">${data.country}</td>
                        <td class="col-date">${data.created}</td>
                        <td class="col-avatar">${imgTag}</td>
                        <td class="col-status">${statusHtml}</td>
                        <td class="col-rap">${rapText}</td>
                    `;
                }
            } catch (e) {
                if (e.name === 'AbortError') {
                    tr.innerHTML = `
                        <td class="col-num" style="color:var(--warning)">${numStr}</td>
                        <td colspan="7" style="color:var(--warning);">Dibatalkan.</td>
                    `;
                    break;
                } else {
                    tr.innerHTML = `
                        <td class="col-num" style="color:var(--danger)">${numStr}</td>
                        <td class="col-usn" style="color:var(--danger)">${usn}</td>
                        <td class="col-pw">${pw}</td>
                        <td colspan="5" class="txt-error">Koneksi terputus (Error Jaringan).</td>
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
