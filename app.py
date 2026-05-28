import json
import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = 'time_tracker.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'logs': [], 'settings': {'jira_url': '', 'username': '', 'api_key': ''}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

data = load_data()

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(data['logs'])

@app.route('/api/logs', methods=['POST'])
def add_log():
    new_log = request.json
    data['logs'].append(new_log)
    save_data(data)
    return jsonify(new_log), 201

@app.route('/api/settings', methods=['GET'])
def get_settings():
    return jsonify(data['settings'])

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    settings = request.json
    data['settings'].update(settings)
    save_data(data)
    return jsonify(data['settings'])

@app.route('/api/projects', methods=['GET'])
def fetch_projects():
    settings = data['settings']
    if not settings.get('jira_url') or not settings.get('api_key'):
        return jsonify({'error': 'Jira configuration missing'}), 400

    url = f"{settings['jira_url']}/rest/api/3/project"
    headers = {
        'Authorization': f"Basic {settings['api_key']}",
        'Accept': 'application/json'
    }
    
    import requests
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Failed to fetch from Jira'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True, port=5000)
