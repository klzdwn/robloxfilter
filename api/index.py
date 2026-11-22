from flask import Flask, request, jsonify, render_template_string
import requests
import time

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
        max-width: 1200px;
    }

    .header { margin-bottom: 20px; }
    .header h2 { font-size: 22px; font-weight: 700; color: #fff; }
    .header p { font-size: 13px; color: var(--text-muted); margin-top: 5px; }

    .input-group {
        background: var(--panel-bg);
        padding: 15px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        margin-bottom: 20px;
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
        padding: 12px 20px; 
        cursor: pointer; 
        font-weight: 600; 
        margin-top: 12px; 
        width: 100%; 
        border-radius: 8px; 
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        transition: background-color 0.2s, transform 0.1s;
    }
    button:hover:not(:disabled) { background-color: var(--primary-hover); }
    button:active:not(:disabled) { transform: scale(0.98); }
    button:disabled { background-color: #475569; cursor: not-allowed; opacity: 0.7; }

    .table-wrapper {
        width: 100%;
        overflow-x: auto;
        background: var(--panel-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Scrollbar kustom */
    .table-wrapper::-webkit-scrollbar { height: 8px; }
    .table-wrapper::-webkit-scrollbar-track { background: var(--bg-color); border-radius: 4px; }
    .table-wrapper::-webkit-scrollbar-thumb { background: #475569; border-radius: 4px; }
    .table-wrapper::-webkit-scrollbar-thumb:hover { background: #64748b; }

    table { 
        width: 100%; 
        border-collapse: collapse; 
        font-size: 13px; 
        white-space: nowrap; /* Mencegah teks turun ke bawah */
    }

    th, td { 
        padding: 12px 15px; 
        text-align: left; 
        border-bottom: 1px solid var(--border-color); 
    }

    th { 
        background-color: #0b1120; 
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        font-size: 11px;
        letter-spacing: 0.5px;
    }

    tr:last-child td { border-bottom: none; }
    tr:hover td { background-color: rgba(255, 255, 255, 0.02); }

    /* Styling untuk status Yes/No */
    .badge {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
        text-align: center;
        min-width: 45px;
    }
    .badge-yes { background-color: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-no { background-color: rgba(239, 68, 68, 0.15); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.3); }
    .badge-warn { background-color: rgba(245, 158, 11, 0.15); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.3); }
    
    .rap-text { color: var(--purple); font-weight: 600; }
    
    img { 
        width: 38px; 
        height: 38px; 
        border-radius: 50%; 
        border: 2px solid var(--border-color); 
        object-fit: cover;
        display: block;
    }

    /* Animasi Loading */
    .loading-text { color: var(--warning); font-style: italic; font-size: 12px; }
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

    <div class="table-wrapper">
        <table id="resTable">
            <thead>
                <tr>
                    <th>No</th><th>Usn</th><th>Pw</th><th>Negara</th><th>Created</th>
                    <th>Avatar</th><th>Korblox</th><th>Korles</th><th>RAP / Ltd</th>
                    <th>Malivinus</th><th>8Bit Crown</th>
                </tr>
            </thead>
            <tbody id="tbody">
                <!-- Data akan masuk ke sini -->
            </tbody>
        </table>
    </div>
</div>

<script>
async function startFilter() {
    const btn = document.getElementById('filterBtn');
    const lines = document.getElementById('data').value.split('\\n').filter(l => l.trim());
    const tbody = document.getElementById('tbody');
    
    if(lines.length === 0) return alert("Masukkan data terlebih dahulu!");
    
    tbody.innerHTML = '';
    btn.disabled = true;
    btn.innerText = "Memproses...";

    let rowNum = 1;

    for (let line of lines) {
        let parts = line.split(':');
        if(parts.length >= 3) {
            let usn = parts[0].trim();
            let pw = parts[1].trim();
            let ip = parts[2].trim();
            
            let tr = document.createElement('tr');
            // Render baris loading
            tr.innerHTML = `<td>${rowNum}</td><td>${usn}</td><td>${pw}</td><td colspan="8" class="loading-text">Mengecek data...</td>`;
            tbody.appendChild(tr);

            try {
                let res = await fetch('/filter', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({usn: usn, ip: ip})
                });
                
                let data = await res.json();
                
                if (data.status === 'Not Found') {
                    tr.innerHTML = `<td>${rowNum}</td><td>${usn}</td><td>${pw}</td><td>${data.country}</td><td>-</td><td>N/A</td><td><span class="badge badge-no">No</span></td><td><span class="badge badge-no">No</span></td><td>-</td><td><span class="badge badge-no">No</span></td><td><span class="badge badge-no">No</span></td>`;
                } else {
                    let imgTag = data.avatar ? `<img src="${data.avatar}" loading="lazy">` : 'N/A';
                    
                    let korbloxTag = data.korblox ? `<span class="badge badge-yes">Yes</span>` : `<span class="badge badge-no">No</span>`;
                    let korlesTag = data.korles ? `<span class="badge badge-yes">Yes</span>` : `<span class="badge badge-no">No</span>`;
                    let malivinusTag = data.malivinus ? `<span class="badge badge-yes">Yes</span>` : `<span class="badge badge-no">No</span>`;
                    let crownTag = data.crown_8bit ? `<span class="badge badge-yes">Yes</span>` : `<span class="badge badge-no">No</span>`;

                    let rapText = data.rap > 0 ? `<span class="rap-text">${data.rap.toLocaleString()}</span> / ${data.limiteds}` : `<span class="badge badge-warn">Priv/None</span>`;

                    tr.innerHTML = `<td>${rowNum}</td><td style="font-weight:600;">${usn}</td><td>${pw}</td><td>${data.country}</td><td>${data.created}</td><td>${imgTag}</td><td>${korbloxTag}</td><td>${korlesTag}</td><td>${rapText}</td><td>${malivinusTag}</td><td>${crownTag}</td>`;
                }
            } catch (e) {
                tr.innerHTML = `<td>${rowNum}</td><td>${usn}</td><td>${pw}</td><td colspan="8" style="color:var(--danger);">Terjadi kesalahan sistem.</td>`;
            }
            
            rowNum++;
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
        
        rap_val = 0
        ltd_val = 0
        try:
            roli_req = requests.get(f'https://api.rolimons.com/players/v1/playerinfo/{user_id}', timeout=5)
            if roli_req.status_code == 200:
                roli_data = roli_req.json()
                if roli_data.get('success'):
                    rap_val = roli_data.get('rap', 0)
                    ltd_val = roli_data.get('num_limiteds', 0)
        except Exception:
            pass
                
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
