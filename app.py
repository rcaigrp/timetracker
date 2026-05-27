from flask import Flask, request, jsonify, render_template_string
import json
import os
import time
from datetime import datetime


class TimeTracker:
    def __init__(self, data_file='time_tracker.json'):
        self.data_file = data_file
        self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'projects': [],
                'timers': {},
                'settings': {}
            }
    
    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def create_project(self, name):
        project = {
            'id': len(self.data['projects']),
            'name': name
        }
        self.data['projects'].append(project)
        self.save_data()
        return project
    
    def start_timer(self, project_id):
        if project_id not in self.data['timers']:
            self.data['timers'][project_id] = {
                'start_time': time.time(),
                'elapsed': 0,
                'is_running': True
            }
            self.save_data()
        return self.data['timers'][project_id]
    
    def stop_timer(self, project_id):
        if project_id in self.data['timers'] and self.data['timers'][project_id]['is_running']:
            timer = self.data['timers'][project_id]
            timer['elapsed'] += time.time() - timer['start_time']
            timer['is_running'] = False
            self.save_data()
        return self.data['timers'].get(project_id)
    
    def get_timer(self, project_id):
        return self.data['timers'].get(project_id)
    
    def get_projects(self):
        return self.data['projects']
    
    def set_settings(self, settings):
        self.data['settings'] = settings
        self.save_data()
    
    def get_settings(self):
        return self.data['settings']


app = Flask(__name__)
time_tracker = TimeTracker()

@app.route('/')
def dashboard():
    projects = time_tracker.get_projects()
    return render_template_string('''
    <html>
        <head><title>Time Tracker</title></head>
        <body>
            <h1>Time Tracker Dashboard</h1>
            <ul>
                {% for project in projects %}
                <li>{{ project.name }}</li>
                {% endfor %}
            </ul>
        </body>
    </html>
    ''', projects=projects)

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = time_tracker.create_project(data['name'])
    return jsonify(project), 201

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = time_tracker.get_projects()
    return jsonify(projects)

@app.route('/api/timer/start/<int:project_id>', methods=['POST'])
def start_timer(project_id):
    timer = time_tracker.start_timer(project_id)
    return jsonify(timer)

@app.route('/api/timer/stop/<int:project_id>', methods=['POST'])
def stop_timer(project_id):
    timer = time_tracker.stop_timer(project_id)
    return jsonify(timer)

@app.route('/api/timer/<int:project_id>', methods=['GET'])
def get_timer(project_id):
    timer = time_tracker.get_timer(project_id)
    return jsonify(timer)

@app.route('/api/settings', methods=['POST'])
def set_settings():
    data = request.get_json()
    time_tracker.set_settings(data)
    return jsonify({'status': 'success'})

@app.route('/api/settings', methods=['GET'])
def get_settings():
    settings = time_tracker.get_settings()
    return jsonify(settings)
