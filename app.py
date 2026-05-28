import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

CONFIG_FILE = "settings.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

@app.route('/')
def dashboard():
    return jsonify({"message": "TimeTracker Dashboard", "status": "active"})

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    config = load_config()
    if request.method == 'POST':
        save_config(request.json)
        return jsonify({"status": "saved", "config": request.json}), 201
    return jsonify(config)

@app.route('/api/jira/projects', methods=['GET'])
def jira_projects():
    config = load_config()
    # AC 4: Requires config to proceed
    if not config.get('url'):
        return jsonify({"error": "Jira URL not configured"}), 400
    # In a real app, this would make the HTTP request
    return jsonify({"projects": [{"name": "Test Project", "key": "TP"}]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
