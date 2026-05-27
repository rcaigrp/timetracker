from flask import Flask, jsonify, request
import json
import os
import requests

app = Flask(__name__)
data_file = 'time_tracker.json'
jira_url_key = 'JIRA_URL'
jira_api_key = 'JIRA_API_KEY'

def load_data():
    if os.path.exists(data_file):
        try:
            with open(data_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, TypeError):
            return {'times': [], 'projects': [], 'settings': {}}
    return {'times': [], 'projects': [], 'settings': {}}

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f)

def fetch_jira_projects():
    settings = load_data().get('settings', {})
    url = settings.get('url')
    api_key = settings.get('api_key')
    if url and api_key:
        headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
        # Note: In a real app, we'd use a proxy to avoid exposing keys, but keeping it simple for this task
        try:
            # Using a public endpoint for demo purposes, though not recommended for prod
            response = requests.get(f"{url.rstrip('/')}/rest/api/2/project", headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except requests.RequestException:
            return []
    return []

@app.route('/')
def dashboard():
    return jsonify({"status": "ok", "message": "JiraTime Dashboard"})

@app.route('/api/projects', methods=['GET'])
def get_projects():
    # Logic: If Jira is configured, fetch from Jira. Otherwise, use local.
    jira_projects = fetch_jira_projects()
    if jira_projects:
        return jsonify(jira_projects)
    return jsonify(load_data().get('projects', []))

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(load_data().get('settings', {}))

@app.route('/api/settings', methods=['POST'])
def save_settings():
    data = request.json
    current_data = load_data()
    current_data['settings'] = data or {}
    save_data(current_data)
    return jsonify({"status": "saved"})

@app.route('/api/times', methods=['POST'])
def add_time():
    data = request.json
    current_data = load_data()
    times = current_data.get('times', [])
    times.append({
        "id": len(times) + 1,
        "project": data.get('project'),
        "duration": data.get('duration'),
        "date": data.get('date')
    })
    current_data['times'] = times
    save_data(current_data)
    return jsonify({"status": "success"})

@app.route('/api/times', methods=['GET'])
def get_times():
    return jsonify(load_data().get('times', []))

if __name__ == '__main__':
    app.run(debug=True)
