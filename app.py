import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

CONFIG = {"jira_url": None, "api_key": None, "username": None}
if os.path.exists('settings.json'):
    try:
        with open('settings.json', 'r') as f:
            CONFIG.update(json.load(f))
    except: pass

def get_jira_client():
    if not CONFIG.get('jira_url') or not CONFIG.get('api_key'):
        return None
    return requests.Session()

@app.route('/')
def index():
    return 'TimeTracker API Running'

@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'GET':
        return jsonify(CONFIG)
    else:
        CONFIG.update(request.json)
        with open('settings.json', 'w') as f:
            json.dump(CONFIG, f)
        return jsonify(CONFIG)

@app.route('/api/projects', methods=['GET'])
def fetch_projects():
    client = get_jira_client()
    if not client:
        return jsonify([])
    # Call Jira API for projects
    try:
        response = client.get(f"{CONFIG['jira_url']}/rest/api/2/project")
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify([]), 500
    except Exception as e:
        return jsonify([]), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)