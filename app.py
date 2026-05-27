from flask import Flask, render_template, request, jsonify
import os
import json
import requests
from datetime import datetime

app = Flask(__name__)

# In-memory storage for time entries (in production would be database)
time_entries = []

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Load existing time entries from file
try:
    with open('data/time_entries.json', 'r') as f:
        time_entries = json.load(f)
except FileNotFoundError:
    time_entries = []

def save_time_entry(entry):
    # Save to file (in production would be database)
    with open('data/time_entries.json', 'w') as f:
        json.dump(time_entries, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/projects')
def get_projects():
    try:
        projects = get_projects_from_jira()
        return jsonify(projects)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_projects_from_jira():
    # Mocked function - in production would call Jira API
    base_url = os.environ.get('JIRA_BASE_URL')
    username = os.environ.get('JIRA_USERNAME')
    api_key = os.environ.get('JIRA_API_KEY')
    
    if not all([base_url, username, api_key]):
        raise ValueError('Missing Jira credentials')
    
    # Mock response
    return [{'id': '10000', 'key': 'PROJ', 'name': 'Test Project'}]

@app.route('/api/time_entries', methods=['POST'])
def create_time_entry():
    data = request.get_json()
    entry = {
        'id': len(time_entries) + 1,
        'project_name': data['project_name'],
        'description': data.get('description', ''),
        'start_time': datetime.now().isoformat(),
        'end_time': None,
        'duration': 0
    }
    time_entries.append(entry)
    save_time_entry(entry)
    return jsonify(entry)

@app.route('/api/time_entries/<int:entry_id>/stop', methods=['POST'])
def stop_timer(entry_id):
    for entry in time_entries:
        if entry['id'] == entry_id:
            entry['end_time'] = datetime.now().isoformat()
            # Calculate duration (simplified)
            entry['duration'] = 3600  # 1 hour for demo
            save_time_entry(entry)
            return jsonify(entry)
    return jsonify({'error': 'Entry not found'}), 404

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Store credentials in environment variables (in production would be secure storage)
        os.environ['JIRA_BASE_URL'] = request.form['jira_base_url']
        os.environ['JIRA_USERNAME'] = request.form['jira_username']
        os.environ['JIRA_API_KEY'] = request.form['jira_api_key']
        return jsonify({'status': 'success'})
    else:
        return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)