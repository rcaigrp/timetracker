from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

data_file = 'time_tracker.json'

def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            return json.load(f)
    return {'entries': [], 'jira_config': {}}

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f)

@app.route('/api/time-entries', methods=['GET', 'POST'])
def time_entries():
    data = load_data()
    if request.method == 'POST':
        entry = request.json
        data['entries'].append(entry)
        save_data(data)
        return jsonify(entry), 201
    return jsonify(data['entries'])

@app.route('/api/settings', methods=['POST'])
def settings():
    config = request.json
    data = load_data()
    data['jira_config'] = config
    save_data(data)
    return jsonify(config)

@app.route('/api/projects', methods=['GET'])
def projects():
    # In production, this would call Jira API
    # For now, we return a placeholder or fetch from config
    if load_data()['jira_config']:
        return jsonify(['JIRA-PROJECT-1']) # Mock return
    return jsonify([])

@app.route('/')
def index():
    return '<h1>TimeTracker API Running</h1>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
