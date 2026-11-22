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
<style>
    body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; padding: 10px; }
    textarea { width: 100%; height: 120px; background-color: #161b22; color: #58a6ff; border: 1px solid #30363d; padding: 10px; box-sizing: border-box; font-family: monospace; }
    button { background-color: #1f6feb; color: white; border: none; padding: 12px 20px; cursor: pointer; font-weight: bold; margin-top: 10px; width: 100%; border-radius: 4px; }
    button:hover { background-color: #388bfd; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 11px; }
    th, td { border: 1px solid #30363d; padding: 6px; text-align: left; word-break: break-all; }
    th { background-color: #161b22; }
    .good { color: #3fb950; font-weight: bold; }
    .bad { color: #f85149; font-weight: bold; }
    .warn { color: #d29922; font-weight: bold; }
    .rap { color: #a371f7; font-weight: bold; }
    img { width: 35px; height: 35px; border-radius: 50%; border: 1px solid #30363d; }
</style>
</head>
<body>
<h3>R0bl0x F1lt3r</h3>
<p style="font-size: 11px; color: #8b949e;">Format: usn:pw:ip</p>
<textarea id="data" placeholder="Karpuzunxx:878889999:38.114.120.212"></textarea>
<br>
<button onclick="startFilter()">Mulai Filter</button>
<table id="resTable">
    <thead>
        <tr><th>No</th><th>Usn</th><th>Pw</th><th>Negara</th><th>Created</th><th>Avatar</th><th>Korblox</th><th>Korles</th><th>RAP / Ltd</th><th>Malivinus</th></tr>
    </thead>
    <tbody id="tbody"></tbody>
</table>

<script>
async function startFilter() {
    const lines = document.getElementById('data').value.split('\\n').filter(l => l.trim());
    const tbody = document.getElementById('tbody');
    tbody.innerHTML = '';

    let rowNum = 1;

    for (let line of lines) {
        let parts = line.split(':');
        if(parts.length >= 3) {
            let usn = parts[0].trim();
            let pw = parts[1].trim();
            let ip = parts[2].trim();
            
            let tr = document.createElement('tr');
            tr.innerHTML = `<td>${rowNum}</td><td>${usn}</td><td>${pw}</td><td>Proses...</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td>`;
            tbody.appendChild(tr);

            try {
                let res = await fetch('/filter', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({usn: usn, ip: ip})
                });
                
                let data = await res.json();
                
                if (data.status === 'Not Found') {
                    tr.innerHTML = `<td>${rowNum}</td><td>${usn}</td><td>${pw}</td><td>${data.country}</td><td>-</td><td>N/A</td><td class="bad">No</td><td class="bad">No</td><td>-</td><td class="bad">No</td>`;
                } else {
                    let imgTag = data.avatar ? `<img src="${data.avatar}">` : 'N/A';
                    
                    let korbloxTag = data.korblox ? `<span class="good">Yes</span>` : `<span class="bad">No</span>`;
                    let korlesTag = data.korles ? `<span class="good">Yes</span>` : `<span class="bad">No</span>`;
                    
                    let malivinusTag = data.malivinus ? `<span class="good">Yes</span>` : `<span class="bad">No</span>`;

                    let rapText = data.rap > 0 ? `<span class="rap">${data.rap}</span> / ${data.limiteds}` : `<span class="warn">Priv/None</span>`;

                    tr.innerHTML = `<td>${rowNum}</td><td>${usn}</td><td>${pw}</td><td>${data.country}</td><td>${data.created}</td><td>${imgTag}</td><td>${korbloxTag}</td><td>${korlesTag}</td><td>${rapText}</td><td>${malivinusTag}</td>`;
                }
            } catch (e) {
                tr.innerHTML = `<td>${rowNum}</td><td>${usn}</td><td>${pw}</td><td>Error</td><td>-</td><td>N/A</td><td class="bad">Error</td><td class="bad">Error</td><td>-</td><td class="bad">Error</td>`;
            }
            
            rowNum++;
        }
    }
}
</script>
</body>
</html>
"""

HEADLESS_IDS = [134082579, 15093053680] 
KORBLOX_IDS = [139607718, 139607917, 2988500]

# --- ID RESMI BUNDLE MALIVINIUS (ID 334) ---
MALIVINUS_IDS = [
    2807147467,       # Torso
    2807142069,       # Left Arm
    2807144777,       # Right Arm
    2807143328,       # Left Leg
    2807146071,       # Right Leg
    126200552021824   # Head
]

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
        
        if avatar_req.status_code == 200:
            assets = avatar_req.json().get('assets', [])
            for asset in assets:
                asset_id = asset.get('id')
                if asset_id in HEADLESS_IDS:
                    has_headless = True
                if asset_id in KORBLOX_IDS:
                    has_korblox = True
                # Cek apakah ID aset di avatar ada di dalam list MALIVINUS_IDS
                if asset_id in MALIVINUS_IDS:
                    has_malivinus = True
                    
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
            'malivinus': has_malivinus
        })
        
    except Exception as e:
        return jsonify({'status': 'Error', 'country': country_name})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
