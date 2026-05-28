from flask import Flask, jsonify, request
import json
import os
import time

app = Flask(__name__)

# Data storage
DATA_FILE = 'time_data.json'
CONFIG_FILE = 'config.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"logs": [], "settings": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        data = request.json
        # Store settings securely (in-memory for now, ideally env vars)
        settings = {"jira_url": data.get("url"), "username": data.get("username"), "api_key": data.get("api_key")}
        save_data({"logs": [], "settings": settings})
        return jsonify(success=True, settings=settings)
    else:
        data = load_data()
        return jsonify(data.get("settings", {}))

@app.route('/api/timer', methods=['GET', 'POST'])
def timer():
    global logs
    if request.method == 'POST':
        payload = request.json
        logs = load_data().get("logs", [])
        if payload.get("action") == "start":
            logs.append({"start": payload.get("timestamp", time.time()), "status": "running", "project": payload.get("project")})
        elif payload.get("action") == "stop":
            logs[-1]["end"] = payload.get("timestamp", time.time())
            logs[-1]["status"] = "stopped"
            save_data({"logs": logs, "settings": load_data().get("settings", {})})
        return jsonify(logs)
    return jsonify(load_data().get("logs", []))

@app.route('/api/jira/projects', methods=['GET'])
def jira_projects():
    settings = load_data().get("settings", {})
    if not settings.get("jira_url"):
        return jsonify([])
    
    url = settings.get("jira_url") + "/rest/api/2/project"
    # Construct auth header (Basic Auth)
    # In production, use environment variables for the API key
    auth_string = settings.get("api_key")
    headers = {"Authorization": f"Basic {auth_string}"}
    
    import requests
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            return jsonify(resp.json())
        else:
            return jsonify({"error": resp.text}), resp.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
