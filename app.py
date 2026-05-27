from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATA_FILE = 'timer_data.json'

# Load existing data or create empty structure
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'projects': [], 'active_project': None}

# Save data to file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', data=data)

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = load_data()
    project_name = request.json.get('name')
    if not project_name:
        return jsonify({'error': 'Project name is required'}), 400
    
    new_project = {
        'id': len(data['projects']),
        'name': project_name,
        'start_time': None,
        'end_time': None,
        'duration': 0,
        'is_active': False
    }
    data['projects'].append(new_project)
    save_data(data)
    return jsonify(new_project)

@app.route('/api/projects/<int:project_id>/start', methods=['POST'])
def start_project(project_id):
    data = load_data()
    for project in data['projects']:
        if project['id'] == project_id:
            project['start_time'] = datetime.now().isoformat()
            project['is_active'] = True
            data['active_project'] = project_id
            save_data(data)
            return jsonify(project)
    return jsonify({'error': 'Project not found'}), 404

@app.route('/api/projects/<int:project_id>/stop', methods=['POST'])
def stop_project(project_id):
    data = load_data()
    for project in data['projects']:
        if project['id'] == project_id:
            if project['start_time']:
                end_time = datetime.now()
                start_time = datetime.fromisoformat(project['start_time'])
                duration = (end_time - start_time).total_seconds()
                project['duration'] += duration
                project['end_time'] = end_time.isoformat()
                project['is_active'] = False
                data['active_project'] = None
                save_data(data)
                return jsonify(project)
    return jsonify({'error': 'Project not found or not started'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)