from flask import Flask, request, jsonify
import json
import os
import requests

app = Flask(__name__)

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'settings.json')
ENTRIES_FILE = os.path.join(os.path.dirname(__file__), 'entries.json')

# Setup templates folder
app.template_folder = os.path.join(os.path.dirname(__file__), 'templates')

@app.route('/')
def index():
    # Serve the React frontend
    try:
        with open('templates/index.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return jsonify({'error': 'Frontend not found'}), 404

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        data = request.json
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(data, f)
        return jsonify(data)
    else:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return jsonify(json.load(f))
        return jsonify({'error': 'Settings not found'}), 400

@app.route('/api/entries', methods=['GET', 'POST'])
def entries():
    def load_json(path):
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_json(path, data):
        with open(path, 'w') as f:
            json.dump(data, f)

    if request.method == 'POST':
        data = request.json
        entries = load_json(ENTRIES_FILE)
        entries.append(data)
        save_json(ENTRIES_FILE, entries)
        return jsonify(data)
    else:
        return jsonify(load_json(ENTRIES_FILE))

@app.route('/api/projects')
def fetch_projects():
    def load_json(path):
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    settings = load_json(SETTINGS_FILE)
    if not settings or not settings.get('jira_url'):
        return jsonify([]), 400

    url = f"{settings['jira_url']}/rest/api/2/project"
    auth = (settings.get('username'), settings.get('api_key')) if settings.get('username') else None

    try:
        r = requests.get(url, auth=auth)
        if r.status_code == 200:
            return jsonify(r.json())
        else:
            return jsonify([]), r.status_code
    except requests.RequestException:
        return jsonify([]), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)