#!/usr/bin/env python3
"""BLF static server with gzip + Cache-Control + contact form capture"""
import http.server
import gzip
import io
import json
import os
import sys
import time

PORT = 8091
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
SUBMISSIONS_FILE = os.path.join(DIRECTORY, 'contact_submissions.json')

class BLFHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        path = self.translate_path(self.path)
        if path.endswith(('.html', '.htm')):
            self.send_header('Cache-Control', 'public, max-age=3600')
        elif path.endswith(('.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif', '.ico', '.css', '.js')):
            self.send_header('Cache-Control', 'public, max-age=86400')
        else:
            self.send_header('Cache-Control', 'public, max-age=3600')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def do_POST(self):
        if self.path.rstrip('/') == '/api/contact':
            try:
                length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(length) if length else b'{}'
                data = json.loads(body.decode('utf-8'))
                data['received_at'] = time.strftime('%Y-%m-%dT%H:%M:%S%z')
                # Append to submissions file
                subs = []
                if os.path.isfile(SUBMISSIONS_FILE):
                    try:
                        with open(SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
                            subs = json.load(f)
                    except Exception:
                        subs = []
                subs.append(data)
                with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(subs, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(b'{"ok":true}')))
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                body = json.dumps({'ok': False, 'error': str(e)}).encode('utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            return
        self.send_response(404)
        self.end_headers()

    def do_GET(self):
        accept_encoding = self.headers.get('Accept-Encoding', '')
        path = self.translate_path(self.path)
        
        # Resolve directory to index.html
        if os.path.isdir(path):
            path = os.path.join(path, 'index.html')
        
        if 'gzip' in accept_encoding.lower() and os.path.isfile(path):
            ext = os.path.splitext(path)[1].lower()
            compressible = {'.html', '.htm', '.css', '.js', '.json', '.xml', '.svg', '.txt'}
            if ext in compressible:
                try:
                    with open(path, 'rb') as f:
                        data = f.read()
                    buf = io.BytesIO()
                    with gzip.GzipFile(fileobj=buf, mode='wb') as gz:
                        gz.write(data)
                    compressed = buf.getvalue()
                    if len(compressed) < len(data):
                        self.send_response(200)
                        self.send_header('Content-Type', self.guess_type(path))
                        self.send_header('Content-Encoding', 'gzip')
                        self.send_header('Content-Length', str(len(compressed)))
                        self.end_headers()
                        self.wfile.write(compressed)
                        return
                except Exception:
                    pass
        
        super().do_GET()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    server = http.server.HTTPServer(('127.0.0.1', port), BLFHandler)
    print(f"BLF server running on http://127.0.0.1:{port} with gzip+cache", flush=True)
    server.serve_forever()
