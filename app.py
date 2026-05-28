from flask import Flask, request, jsonify
import json
import os
import datetime

app = Flask(__name__)

SETTINGS_FILE = 'time_tracker.json'

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE) as f:
                return jsonify(json.load(f))
        return jsonify({'jira_url': '', 'username': '', 'api_key': ''}), 404

    elif request.method == 'POST':
        data = request.json
        save_settings(data)
        return jsonify({'status': 'success'}), 201

@app.route('/api/projects', methods=['GET'])
def fetch_projects():
    settings = get_settings()
    # Implementation for fetching from Jira
    return jsonify([])

@app.route('/api/entries', methods=['GET', 'POST'])
def entries():
    # Implementation for timer and logs
    return jsonify([])

def save_settings(data):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(data, f)

def cut_off(date_string):
    # Fixed cut_off function
    if not date_string:
        return None
    try:
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    except:
        return None

def get_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return {}

if __name__ == '__main__':
    app.run(debug=True)
