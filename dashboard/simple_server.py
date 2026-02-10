#!/usr/bin/env python3
"""
Simple Lotte Dashboard - No external dependencies
Uses only Python standard library
"""

import http.server
import socketserver
import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PORT = 8081
DB_PATH = Path(__file__).parent / 'dashboard.db'

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/':
            self.serve_dashboard()
        elif parsed.path == '/api/settings':
            self.serve_settings()
        elif parsed.path == '/api/logs':
            self.serve_logs()
        else:
            super().do_GET()
    
    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        if parsed.path == '/api/settings':
            self.save_settings(body)
        elif parsed.path == '/api/generate':
            self.trigger_generation(body)
        else:
            self.send_error(404)
    
    def serve_dashboard(self):
        html = self.get_html()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_settings(self):
        settings = self.load_settings()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(settings).encode())
    
    def serve_logs(self):
        logs = self.load_logs()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(logs).encode())
    
    def save_settings(self, body):
        data = json.loads(body)
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for key, value in data.items():
            c.execute('''INSERT INTO settings (key, value) VALUES (?, ?)
                        ON CONFLICT(key) DO UPDATE SET value=excluded.value''',
                      (key, str(value)))
        conn.commit()
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'saved'}).encode())
    
    def trigger_generation(self, body):
        data = json.loads(body)
        tier = data.get('tier', 'all')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        tiers = ['SFW', 'Suggestive', 'NSFW'] if tier == 'all' else [tier]
        for t in tiers:
            c.execute('INSERT INTO generation_logs (tier, status) VALUES (?, ?)',
                      (t, 'pending'))
        conn.commit()
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'started', 'tiers': tiers}).encode())
    
    def load_settings(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT key, value FROM settings')
        settings = {k: v for k, v in c.fetchall()}
        conn.close()
        
        # Defaults
        defaults = {
            'auto_generation': 'false',
            'schedule_time': '10:00',
            'sfw_enabled': 'true',
            'suggestive_enabled': 'true',
            'nsfw_enabled': 'true',
            'google_drive_enabled': 'true'
        }
        defaults.update(settings)
        return defaults
    
    def load_logs(self):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM generation_logs ORDER BY timestamp DESC LIMIT 10')
        logs = c.fetchall()
        conn.close()
        return logs
    
    def get_html(self):
        settings = self.load_settings()
        logs = self.load_logs()
        
        def toggle(name, checked):
            return f'<input type="checkbox" id="{name}" {"checked" if checked == "true" else ""}>'
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <title>Lotte Dashboard</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #eee;
            min-height: 100vh;
            padding: 2rem;
            margin: 0;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .card {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
        }}
        h2 {{
            color: #667eea;
            margin-top: 0;
        }}
        .row {{
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            padding: 1rem 2rem;
            border-radius: 8px;
            color: white;
            cursor: pointer;
            font-size: 1rem;
            width: 100%;
            margin-bottom: 0.5rem;
        }}
        input[type="time"] {{
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            padding: 0.5rem;
            border-radius: 6px;
        }}
        .log {{
            background: rgba(0,0,0,0.2);
            padding: 0.5rem;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Lotte Dashboard</h1>
        
        <div class="card">
            <h2>Settings Settings</h2>
            <div class="row">
                <span>Auto Generation</span>
                {toggle('auto_generation', settings.get('auto_generation'))}
            </div>
            <div class="row">
                <span>Schedule Time</span>
                <input type="time" id="schedule_time" value="{settings.get('schedule_time', '10:00')}">
            </div>
            <div class="row">
                <span>SFW Tier</span>
                {toggle('sfw_enabled', settings.get('sfw_enabled'))}
            </div>
            <div class="row">
                <span>Suggestive Tier</span>
                {toggle('suggestive_enabled', settings.get('suggestive_enabled'))}
            </div>
            <div class="row">
                <span>NSFW Tier</span>
                {toggle('nsfw_enabled', settings.get('nsfw_enabled'))}
            </div>
            <div class="row">
                <span>Google Drive</span>
                {toggle('google_drive_enabled', settings.get('google_drive_enabled'))}
            </div>
        </div>
        
        <div class="card">
            <h2>Manual Generate</h2>
            <button onclick="stopServer()">Stop Server</button>
            <button onclick="restartServer()">Restart Server</button>
            <button onclick="generate('all')">Generate All Tiers</button>
            <button onclick="generate('SFW')">Generate SFW Only</button>
            <button onclick="generate('NSFW')">Generate NSFW Only</button>
        </div>
        
        <div class="card        
        <div class="card">
        <div class="card">
            <h2>Documentation</h2>
            <div class="row"><a href="/docs/categories/explicit.md" style="color:#667eea">Explicit Category</a></div>
            <div class="row"><a href="/docs/categories/lingerie.md" style="color:#667eea">Lingerie & Intimate</a></div>
            <div class="row"><a href="/docs/categories/bedroom.md" style="color:#667eea">Bedroom & Morning</a></div>
            <div class="row"><a href="/docs/categories/bathroom.md" style="color:#667eea">Bathroom & Shower</a></div>
            <div class="row"><a href="/docs/categories/outfits.md" style="color:#667eea">Outfits & Costumes</a></div>
            <div class="row"><a href="/docs/categories/other.md" style="color:#667eea">Other Category</a></div>
        </div>

            <h2>Logs Recent Logs</h2>
            <div id="logs">
                {''.join([f'<div class="log">{log[1]} - {log[2]} - {log[4]}</div>' for log in logs])}
            </div>
        </div>
    </div>
    
    <script>
        function saveSetting(key, value) {{
            fetch('/api/settings', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{[key]: value}})
            }});
        }}
        
        function stopServer() {{
            fetch("/api/stop", {{method: "POST"}})
            .then(r => r.json())
            .then(data => alert("Server stopping... Refresh page to start again"));
        }}
        
        function restartServer() {{
            fetch("/api/restart", {{method: "POST"}})
            .then(r => r.json())
            .then(data => alert("Server restarting... Wait 3 seconds and refresh"));
        }}

        function generate(tier) {{
            fetch('/api/generate', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{tier: tier}})
            }})
            .then(r => r.json())
            .then(data => alert('Started: ' + data.tiers.join(', ')));
        }}
        
        // Auto-save toggles
        document.querySelectorAll('input[type="checkbox"]').forEach(cb => {{
            cb.addEventListener('change', () => saveSetting(cb.id, cb.checked));
        }});
        
        document.getElementById('schedule_time').addEventListener('change', function() {{
            saveSetting('schedule_time', this.value);
        }});
    </script>
</body>
</html>'''
        return html

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS generation_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        tier TEXT,
        status TEXT
    )''')
    
    # Insert defaults
    defaults = [
        ('auto_generation', 'false'),
        ('schedule_time', '10:00'),
        ('sfw_enabled', 'true'),
        ('suggestive_enabled', 'true'),
        ('nsfw_enabled', 'true'),
        ('google_drive_enabled', 'true')
    ]
    c.executemany('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', defaults)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"Lotte Dashboard running at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        httpd.serve_forever()

@app.route('/api/restart', methods=['POST'])
def restart_server():
    """Restart the server"""
    import os
    import sys
    import time
    
    def restart():
        time.sleep(1)
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    import threading
    threading.Thread(target=restart).start()
    
    return jsonify({'status': 'restarting'})

@app.route('/api/stop', methods=['POST'])
def stop_server():
    """Stop the server"""
    import sys
    import time
    
    def shutdown():
        time.sleep(1)
        sys.exit(0)
    
    import threading
    threading.Thread(target=shutdown).start()
    
    return jsonify({'status': 'stopping'})
