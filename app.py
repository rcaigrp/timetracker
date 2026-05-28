import json
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_data():
    try:
        with open('time_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open('time_data.json', 'w') as f:
        json.dump(data, f)

SETTINGS = {
    'jira_url': os.environ.get('JIRA_URL', 'http://localhost:8080'),
    'username': os.environ.get('JIRA_USER', 'admin'),
    'api_key': os.environ.get('JIRA_API', '1234')
}

@app.route('/api/time', methods=['GET'])
def get_time_entries():
    entries = load_data()
    return jsonify(entries)

@app.route('/api/time', methods=['POST'])
def add_time_entry():
    data = request.json
    entry = {
        'id': len(load_data()) + 1,
        'project': data.get('project'),
        'description': data.get('description'),
        'duration': data.get('duration'),
        'start_time': data.get('start_time'),
        'end_time': data.get('end_time')
    }
    entries = load_data()
    entries.append(entry)
    save_data(entries)
    return jsonify(entry), 201

@app.route('/api/jira/projects', methods=['GET'])
def fetch_jira_projects():
    jira_url = SETTINGS.get('jira_url')
    auth = (SETTINGS.get('username'), SETTINGS.get('api_key'))
    headers = {'Accept': 'application/json'}
    
    response = requests.get(f"{jira_url}/rest/api/2/project", headers=headers, auth=auth)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch projects'}), response.status_code

@app.route('/api/settings', methods=['POST'])
def update_settings():
    global SETTINGS
    data = request.json
    SETTINGS.update(data)
    return jsonify(SETTINGS)

if __name__ == '__main__':
    app.run(debug=True, port=5000)