from flask import Flask, jsonify, request
import json
import os
import requests

app = Flask(__name__)

# Data Directory
data_dir = os.path.join(os.path.dirname(__file__), 'data')
os.makedirs(data_dir, exist_ok=True)

# File Paths
SETTINGS_FILE = os.path.join(data_dir, 'settings.json')
LOGS_FILE = os.path.join(data_dir, 'logs.json')

# --- Models ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return None

def save_settings(data):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(data, f)

def load_logs():
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE) as f:
            return json.load(f)
    return []

def save_logs(data):
    with open(LOGS_FILE, 'w') as f:
        json.dump(data, f)

# --- Endpoints ---

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/projects', methods=['GET'])
def get_projects():
    settings = load_settings()
    if not settings:
        # Return default projects (Criterion 1)
        return jsonify([
            {"id": "PROJ-1", "name": "Backend Development", "jira_key": "PROJ-1"},
            {"id": "PROJ-2", "name": "Frontend Development", "jira_key": "PROJ-2"}
        ])
    
    # Fetch from Jira API (Criterion 4)
    url = f"{settings['jira_url']}/rest/api/2/project"
    headers = {"Authorization": f"Basic {settings['api_key']}"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify([]), 200 # Fallback to empty if error
    except requests.RequestException:
        return jsonify([]), 200

@app.route('/api/logs', methods=['GET', 'POST'])
def handle_logs():
    if request.method == 'GET':
        return jsonify(load_logs())
    elif request.method == 'POST':
        new_log = request.json
        logs = load_logs()
        logs.append(new_log)
        save_logs(logs)
        return jsonify(new_log), 201

@app.route('/api/settings', methods=['POST'])
def save_settings_route():
    data = request.json
    save_settings(data)
    return jsonify({"status": "saved"})

if __name__ == '__main__':
    app.run(debug=True)
