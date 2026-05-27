from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = 'time_tracker.json'

@app.route('/')
def index():
    return jsonify({"message": "TimeTracker API Running", "status": "ok"})

@app.route('/time-entries', methods=['GET', 'POST'])
def manage_entries():
    if request.method == 'POST':
        # Manual entry logic
        entry = request.json
        entries = load_entries()
        entries.append(entry)
        save_entries(entries)
        return jsonify(entry), 201
    return jsonify(load_entries())

@app.route('/settings', methods=['POST'])
def save_settings():
    settings = request.json
    with open('settings.json', 'w') as f:
        json.dump(settings, f)
    return jsonify({"success": True, "message": "Settings saved"})

@app.route('/jira/projects', methods=['GET'])
def fetch_jira_projects():
    # Simulating Jira API fetch
    # In real app, this would use requests.get with auth
    return jsonify([
        {"id": "PROJ1", "name": "Project A"},
        {"id": "PROJ2", "name": "Project B"}
    ])

def load_entries():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                return json.load(f)
        except:
            return []
    return []

def save_entries(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

if __name__ == '__main__':
    app.run(debug=True, port=5000)