from flask import Flask, request, jsonify, render_template_string
import requests
import time
import cloudscraper # --- TAMBAHAN BARU ---

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

    /* --- STYLING CARD --- */
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

    .card-header {
        display: flex;
        align-items: center;
        gap: 15px;
        border-bottom: 1px solid var(--border-color);
        padding-bottom: 12px;
    }

    .card-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 2px solid var(--border-color);
        object-fit: cover;
        background: #0b1120;
    }

    .card-user-info { flex: 1; overflow: hidden; }
    .card-username { font-size: 16px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .card-password { font-size: 12px; color: var(--text-muted); margin-top: 3px; font-family: monospace; }

    .card-body {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
    }
    
    .info-box { background: #0b1120; padding: 8px 12px; border-radius: 8px; border: 1px solid #1e293b; }
    .info-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
    .info-value { font-size: 13px; font-weight: 600; margin-top: 2px; color: #cbd5e1; }
    .info-value.rap-val { color: var(--purple); }
    .info-value.warn { color: var(--warning); }

    .card-footer {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: auto; /* Dorong ke bawah */
    }

    /* --- BADGES (Stiker Status) --- */
    .status-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-weight: 600;
        background: #0b1120;
        padding: 6px 10px;
        border-radius: 6px;
        border: 1px solid var(--border-color);
    }
    .status-item span { color: var(--text-muted); font-weight: 400; }

    /* Warna Badge */
    .badge-yes { color: var(--success); border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.1); }
    .badge-no { color: var(--danger); border-color: rgba(239, 68, 68, 0.4); background: rgba(239, 68, 68, 0.1); }
    
    /* Loading & Error State */
    .loading-box { text-align: center; padding: 20px; color: var(--warning); font-style: italic; font-size: 14px; }
    .error-box { color: var(--danger); font-weight: bold; }

</style>
</head>
<body>

<div class="container">
    <div class="header">
        <h2>R0bl0x F1lt3r</h2>
        <p>Format Input: <b>usn:pw:ip</b></p>
    </div>

    <div class="input-group">
        <textarea id="data" placeholder="Karpuzunxx:878889999:38.114.120.212"></textarea>
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
                <div class="card-header">
                    <div class="card-avatar" style="display:flex; align-items:center; justify-content:center;">⏳</div>
                    <div class="card-user-info">
                        <div class="card-username">${usn}</div>
                        <div class="card-password">${pw}</div>
                    </div>
                </div>
                <div class="loading-box">Mengecek data & inventory...</div>
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
                        <div class="card-header">
                            <div class="card-avatar" style="display:flex; align-items:center; justify-content:center; color:var(--danger);">X</div>
                            <div class="card-user-info">
                                <div class="card-username">${usn}</div>
                                <div class="card-password">${pw}</div>
                            </div>
                        </div>
                        <div class="error-box">Username tidak ditemukan / Banned.</div>
                    `;
                } else {
                    let imgTag = data.avatar ? `<img src="${data.avatar}" class="card-avatar" loading="lazy">` : `<div class="card-avatar" style="display:flex; align-items:center; justify-content:center;">N/A</div>`;
                    
                    // Fungsi Helper untuk Badge
                    const getBadge = (status) => status 
                        ? `<div class="status-item badge-yes">Yes</div>` 
                        : `<div class="status-item badge-no">No</div>`;

                    let rapHtml = data.rap > 0 
                        ? `<div class="info-value rap-val">${data.rap.toLocaleString()} / ${data.limiteds}</div>` 
                        : `<div class="info-value warn">Priv / None</div>`;

                    card.innerHTML = `
                        <div class="card-header">
                            ${imgTag}
                            <div class="card-user-info">
                                <div class="card-username">${usn}</div>
                                <div class="card-password">${pw}</div>
                            </div>
                        </div>
                        
                        <div class="card-body">
                            <div class="info-box">
                                <div class="info-label">Negara</div>
                                <div class="info-value">${data.country}</div>
                            </div>
                            <div class="info-box">
                                <div class="info-label">Dibuat</div>
                                <div class="info-value">${data.created}</div>
                            </div>
                            <div class="info-box" style="grid-column: span 2;">
                                <div class="info-label">RAP / Limiteds</div>
                                ${rapHtml}
                            </div>
                        </div>

                        <div class="card-footer">
                            <div class="status-item ${data.korblox ? 'badge-yes' : 'badge-no'}"><span>Korblox:</span> ${data.korblox ? 'Yes' : 'No'}</div>
                            <div class="status-item ${data.korles ? 'badge-yes' : 'badge-no'}"><span>Korles:</span> ${data.korles ? 'Yes' : 'No'}</div>
                            <div class="status-item ${data.malivinus ? 'badge-yes' : 'badge-no'}"><span>Malivinus:</span> ${data.malivinus ? 'Yes' : 'No'}</div>
                            <div class="status-item ${data.crown_8bit ? 'badge-yes' : 'badge-no'}"><span>8Bit Crown:</span> ${data.crown_8bit ? 'Yes' : 'No'}</div>
                        </div>
                    `;
                }
            } catch (e) {
                card.innerHTML = `
                    <div class="card-header">
                        <div class="card-username">${usn}</div>
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
        
        # --- BAGIAN RAP ROLIMONS YANG DIGANTI KE CLOUDSCRAPER ---
        rap_val = 0
        ltd_val = 0
        try:
            # Inisialisasi cloudscraper (bypass Cloudflare)
            scraper = cloudscraper.create_scraper()
            roli_req = scraper.get(f'https://api.rolimons.com/players/v1/playerinfo/{user_id}', timeout=5)
            
            if roli_req.status_code == 200:
                roli_data = roli_req.json()
                if roli_data.get('success'):
                    rap_val = roli_data.get('rap', 0)
                    ltd_val = roli_data.get('num_limiteds', 0)
        except Exception as e:
            print(f"Log Error RAP: {e}") # Biar kelihatan di Vercel Logs kalau gagal
        # --------------------------------------------------------
                
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
