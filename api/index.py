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
        max-width: 1000px;
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
        height: 120px; 
        background-color: #0b1120; 
        color: #60a5fa; 
        border: 1px solid var(--border-color); 
        border-radius: 8px;
        padding: 12px; 
        font-family: 'Inter', monospace; 
        font-size: 13px;
        resize: vertical;
        transition: border-color 0.2s;
    }
    textarea:focus { outline: none; border-color: var(--primary); }

    button { 
        background-color: var(--primary); 
        color: white; 
        border: none; 
        padding: 14px 20px; 
        cursor: pointer; 
        font-weight: 600; 
        margin-top: 12px; 
        width: 100%; 
        border-radius: 8px; 
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        transition: background-color 0.2s, transform 0.1s;
    }
    button:hover:not(:disabled) { background-color: var(--primary-hover); }
    button:active:not(:disabled) { transform: scale(0.98); }
    button:disabled { background-color: #475569; cursor: not-allowed; opacity: 0.7; }

    /* --- LAYOUT GRID UNTUK CARD --- */
    .results-grid {
        display: grid;
        grid-template-columns: 1fr; /* Mobile: 1 kolom */
        gap: 15px;
    }

    @media (min-width: 768px) {
        .results-grid {
            grid-template-columns: repeat(auto-fill, minmax(450px, 1fr)); /* PC: Grid */
        }
    }

    /* --- STYLING CARD BARU (2 BARIS) --- */
    .card {
        background: var(--panel-bg);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        gap: 15px;
        transition: transform 0.2s, border-color 0.2s;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }
    .card:hover { border-color: #475569; transform: translateY(-2px); }

    /* Baris Atas: Text Info */
    .card-top-row {
        display: flex;
        flex-direction: column;
        gap: 4px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 12px;
    }
    .top-main-info {
        font-size: 15px;
        font-weight: 600;
        color: #fff;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .top-sub-info {
        font-size: 12px;
        color: var(--text-muted);
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .top-sub-info span { color: #cbd5e1; font-weight: 500;}

    /* Baris Bawah: Profile & Badges */
    .card-bottom-row {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .card-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid var(--border-color);
        object-fit: cover;
        background: #0b1120;
        flex-shrink: 0;
    }

    .card-footer {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        flex: 1;
    }

    /* --- BADGES (Stiker Status) --- */
    .status-item {
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 11px;
        font-weight: 600;
        background: #0b1120;
        padding: 4px 8px;
        border-radius: 6px;
        border: 1px solid var(--border-color);
    }
    .status-item span { color: var(--text-muted); font-weight: 400; }

    /* Warna Badge */
    .badge-yes { color: var(--success); border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.1); }
    .badge-no { color: var(--danger); border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1); }
    .badge-rap { color: var(--purple); border-color: rgba(168, 85, 247, 0.4); background: rgba(168, 85, 247, 0.1); }
    
    /* Loading & Error State */
    .loading-box { text-align: center; padding: 20px; color: var(--warning); font-style: italic; font-size: 14px; }
    .error-box { color: var(--danger); font-weight: bold; font-size: 13px; margin-top: 5px;}

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
        <button id="filterBtn" onclick="startFilter()">Mulai Filter</button>
    </div>

    <!-- Container untuk Card -->
    <div id="results" class="results-grid"></div>
</div>

<script>
async function startFilter() {
    const btn = document.getElementById('filterBtn');
    const lines = document.getElementById('data').value.split('\\n').filter(l => l.trim());
    const resultsContainer = document.getElementById('results');
    
    if(lines.length === 0) return alert("Masukkan data terlebih dahulu!");
    
    resultsContainer.innerHTML = '';
    btn.disabled = true;
    btn.innerText = "Memproses...";

    for (let line of lines) {
        let parts = line.split(':');
        if(parts.length >= 3) {
            let usn = parts[0].trim();
            let pw = parts[1].trim();
            let ip = parts[2].trim();
            
            // Buat Card Loading
            let card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <div class="card-top-row">
                    <div class="top-main-info">${usn} : ${pw} : ${ip}</div>
                    <div class="top-sub-info">Mengecek data...</div>
                </div>
                <div class="card-bottom-row">
                    <div class="card-avatar" style="display:flex; align-items:center; justify-content:center;">⏳</div>
                    <div class="loading-box" style="padding:0; text-align:left;">Memuat inventory...</div>
                </div>
            `;
            resultsContainer.appendChild(card);

            try {
                let res = await fetch('/filter', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({usn: usn, ip: ip})
                });
                
                let data = await res.json();
                
                if (data.status === 'Not Found') {
                    card.innerHTML = `
                        <div class="card-top-row">
                            <div class="top-main-info">${usn} : ${pw} : ${ip}</div>
                            <div class="top-sub-info" style="color:var(--danger);">Username tidak ditemukan (Banned/Email)</div>
                        </div>
                        <div class="card-bottom-row">
                            <div class="card-avatar" style="display:flex; align-items:center; justify-content:center; color:var(--danger);">X</div>
                        </div>
                    `;
                } else {
                    let imgTag = data.avatar ? `<img src="${data.avatar}" class="card-avatar" loading="lazy">` : `<div class="card-avatar" style="display:flex; align-items:center; justify-content:center;">N/A</div>`;
                    
                    // Format RAP
                    let rapText = data.rap > 0 ? `${data.rap.toLocaleString()} RAP / ${data.limiteds} Ltd` : `Priv / None`;
                    let rapClass = data.rap > 0 ? 'badge-rap' : 'badge-no';

                    card.innerHTML = `
                        <!-- BARIS ATAS: USN, PW, IP, TANGGAL -->
                        <div class="card-top-row">
                            <div class="top-main-info" title="${usn}:${pw}:${ip}">${usn} : ${pw} : ${ip}</div>
                            <div class="top-sub-info">
                                <div>Negara: <span>${data.country}</span></div>
                                <div>Dibuat: <span>${data.created}</span></div>
                                <div>RAP: <span style="color:var(--purple)">${rapText}</span></div>
                            </div>
                        </div>

                        <!-- BARIS BAWAH: PROFILE & BADGES -->
                        <div class="card-bottom-row">
                            ${imgTag}
                            <div class="card-footer">
                                <div class="status-item ${data.korblox ? 'badge-yes' : 'badge-no'}"><span>Korblox:</span> ${data.korblox ? 'Yes' : 'No'}</div>
                                <div class="status-item ${data.korles ? 'badge-yes' : 'badge-no'}"><span>Korles:</span> ${data.korles ? 'Yes' : 'No'}</div>
                                <div class="status-item ${data.malivinus ? 'badge-yes' : 'badge-no'}"><span>Malivinus:</span> ${data.malivinus ? 'Yes' : 'No'}</div>
                                <div class="status-item ${data.crown_8bit ? 'badge-yes' : 'badge-no'}"><span>8Bit Crown:</span> ${data.crown_8bit ? 'Yes' : 'No'}</div>
                            </div>
                        </div>
                    `;
                }
            } catch (e) {
                card.innerHTML = `
                    <div class="card-top-row">
                        <div class="top-main-info">${usn} : ${pw} : ${ip}</div>
                    </div>
                    <div class="error-box">Terjadi kesalahan jaringan.</div>
                `;
            }
        }
    }
    
    btn.disabled = false;
    btn.innerText = "Mulai Filter";
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
