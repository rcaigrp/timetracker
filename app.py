from flask import Flask, request, jsonify
import json
import os
import uuid
from datetime import datetime

class Project:
    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    @classmethod
    def from_dict(cls, data):
        project = cls(data['name'])
        project.id = data['id']
        return project

class Timer:
    def __init__(self, project_id):
        self.project_id = project_id
        self.start_time = None
        self.stop_time = None
        self.elapsed_time = 0.0

    def to_dict(self):
        return {
            'project_id': self.project_id,
            'start_time': self.start_time,
            'stop_time': self.stop_time,
            'elapsed_time': self.elapsed_time
        }

    @classmethod
    def from_dict(cls, data):
        timer = cls(data['project_id'])
        timer.start_time = data.get('start_time')
        timer.stop_time = data.get('stop_time')
        timer.elapsed_time = data.get('elapsed_time', 0.0)
        return timer

class Settings:
    def __init__(self):
        self.jira_base_url = ""
        self.jira_username = ""
        self.jira_api_key = ""

    def to_dict(self):
        return {
            'jira_base_url': self.jira_base_url,
            'jira_username': self.jira_username,
            'jira_api_key': self.jira_api_key
        }

    @classmethod
    def from_dict(cls, data):
        settings = cls()
        settings.jira_base_url = data.get('jira_base_url', '')
        settings.jira_username = data.get('jira_username', '')
        settings.jira_api_key = data.get('jira_api_key', '')
        return settings

# Initialize Flask app
app = Flask(__name__)

# File paths for data persistence
PROJECTS_FILE = "projects.json"
TIMERS_FILE = "timers.json"
SETTINGS_FILE = "settings.json"

# Load existing data on startup
projects = load_projects()
timers = load_timers()
settings = load_settings()

def save_projects(projects):
    with open(PROJECTS_FILE, 'w') as f:
        json.dump([project.to_dict() for project in projects], f)

def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r') as f:
            data = json.load(f)
            return [Project.from_dict(item) for item in data]
    return []

def save_timers(timers):
    with open(TIMERS_FILE, 'w') as f:
        json.dump([timer.to_dict() for timer in timers], f)

def load_timers():
    if os.path.exists(TIMERS_FILE):
        with open(TIMERS_FILE, 'r') as f:
            data = json.load(f)
            return [Timer.from_dict(item) for item in data]
    return []

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings.to_dict(), f)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            data = json.load(f)
            return Settings.from_dict(data)
    return Settings()

@app.route('/', methods=['GET'])
def dashboard():
    return jsonify({'message': 'TimeTracker Dashboard'})

@app.route('/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    project = Project(data['name'])
    projects.append(project)
    save_projects(projects)
    return jsonify(project.to_dict()), 201

@app.route('/projects', methods=['GET'])
def get_projects():
    return jsonify([project.to_dict() for project in projects])

@app.route('/projects/<project_id>/start', methods=['POST'])
def start_timer(project_id):
    timer = Timer(project_id)
    timer.start_time = datetime.now().timestamp()
    timers.append(timer)
    save_timers(timers)
    return jsonify({'message': 'Timer started'}), 200

@app.route('/projects/<project_id>/stop', methods=['POST'])
def stop_timer(project_id):
    for timer in timers:
        if timer.project_id == project_id and timer.start_time and not timer.stop_time:
            timer.stop_time = datetime.now().timestamp()
            timer.elapsed_time += timer.stop_time - timer.start_time
            save_timers(timers)
            return jsonify({'message': 'Timer stopped', 'elapsed_time': timer.elapsed_time}), 200
    return jsonify({'error': 'Timer not found or already stopped'}), 404

@app.route('/projects/<project_id>/timer', methods=['GET'])
def get_timer(project_id):
    for timer in timers:
        if timer.project_id == project_id:
            return jsonify(timer.to_dict()), 200
    return jsonify({'error': 'Timer not found'}), 404

@app.route('/settings', methods=['POST'])
def set_settings():
    data = request.get_json()
    settings.jira_base_url = data['jira_base_url']
    settings.jira_username = data['jira_username']
    settings.jira_api_key = data['jira_api_key']
    save_settings(settings)
    return jsonify({'message': 'Settings saved'}), 200

@app.route('/settings', methods=['GET'])
def get_settings():
    return jsonify(settings.to_dict()), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)