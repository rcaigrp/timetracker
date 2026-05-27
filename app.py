import http.server
import json
import os
from urllib.parse import urlparse, parse_qs

PORT = 5000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(BASE_DIR, 'settings.json')
LOGS_PATH = os.path.join(BASE_DIR, 'time_logs.json')

class TimeTrackerHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Suppress default logging

    def _set_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def write_json(self, data):
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == '/api/time-logs':
            self._set_headers()
            logs = load_time_logs()
            self.write_json(logs)
            
        elif path == '/api/jira/projects':
            settings = load_settings()
            # Basic auth header simulation for Jira
            auth_header = {"Authorization": "Basic " + settings.get('api_key', '')}
            # In a real scenario, we would call the external API here.
            # For this standalone version, we return a mock response or settings data.
            self._set_headers()
            response = {"message": "Jira integration endpoint. Requires external API call."}
            self.write_json(response)
            
        elif path == '/api/settings':
            self._set_headers()
            settings = load_settings()
            self.write_json(settings)
            
        else:
            self._set_headers(404)
            self.write_json({"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        
        if path == '/api/time-logs':
            self._set_headers()
            # Read JSON body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            logs = load_time_logs()
            logs.append({
                'task': data.get('task'),
                'duration': data.get('duration'),
                'date': data.get('date')
            })
            save_time_logs(logs)
            self.write_json(logs[-1])
            
        elif path == '/api/settings':
            self._set_headers()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body)
            
            with open(SETTINGS_PATH, 'w') as f:
                json.dump(data, f)
            self.write_json({"status": "success"})
            
        else:
            self._set_headers(404)
            self.write_json({"error": "Not found"})

# Data Persistence

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    return {"jira_url": "", "api_key": "", "username": ""}

def load_time_logs():
    if os.path.exists(LOGS_PATH):
        with open(LOGS_PATH, 'r') as f:
            return json.load(f)
    return []

def save_time_logs(logs):
    with open(LOGS_PATH, 'w') as f:
        json.dump(logs, f)

# Server Setup

def run(server_class=http.server.HTTPServer, handler_class=TimeTrackerHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Serving TimeTracker API on port {PORT}')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()

if __name__ == "__main__":
    run()