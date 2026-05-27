from flask import Flask, jsonify, request
import os
import json
import requests
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'time_tracker.json'

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {'entries': [], 'settings': {'jira_url': '', 'api_key': ''}}
    return {'entries': [], 'settings': {'jira_url': '', 'api_key': ''}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/timer/start', methods=['POST'])
def start_timer():
    data = request.json
    entry = {
        'id': len(load_data()['entries']) + 1,
        'project': data.get('project'),
        'start_time': datetime.now().isoformat(),
        'active': True
    }
    current = load_data()
    current['entries'].append(entry)
    save_data(current)
    return jsonify(entry)

@app.route('/timer/stop', methods=['POST'])
def stop_timer():
    entries = load_data()['entries']
    if not entries:
        return jsonify({'error': 'No active timer'}), 400
    entry = entries[-1]
    entry['end_time'] = datetime.now().isoformat()
    entry['active'] = False
    current = load_data()
    current['entries'][-1] = entry
    save_data(current)
    return jsonify(entry)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    data = load_data()
    if request.method == 'POST':
        data['settings'] = request.json
        save_data(data)
        return jsonify({'status': 'saved', 'settings': data['settings']})
    return jsonify(data['settings'])

@app.route('/jira/projects', methods=['GET'])
def jira_projects():
    settings = load_data()['settings']
    jira_url = settings.get('jira_url')
    api_key = settings.get('api_key')
    
    headers = {'Authorization': f'Basic {api_key}'}
    response = requests.get(f'{jira_url}/rest/api/3/search', headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
