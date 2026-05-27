#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify, session
import requests
import json
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename

class TimeTrackerApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'your-secret-key-here'
        
        # In-memory storage (in production would use database)
        self.projects = []
        self.logs = []
        self.settings = {}
        self.timer_data = {}
        
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/')
        def dashboard():
            return render_template('dashboard.html', projects=self.projects, logs=self.logs)
        
        @self.app.route('/projects', methods=['POST'])
        def create_project():
            project_data = {
                'id': len(self.projects) + 1,
                'name': request.form['name'],
                'description': request.form.get('description', ''),
                'created_at': datetime.now().isoformat()
            }
            self.projects.append(project_data)
            return jsonify(project_data), 201
        
        @self.app.route('/timer/start', methods=['POST'])
        def start_timer():
            project_id = int(request.form['project_id'])
            self.timer_data[project_id] = {
                'start_time': datetime.now(),
                'is_running': True
            }
            return jsonify({'status': 'started'})
        
        @self.app.route('/timer/stop', methods=['POST'])
        def stop_timer():
            project_id = int(request.form['project_id'])
            if project_id in self.timer_data and self.timer_data[project_id]['is_running']:
                end_time = datetime.now()
                duration = (end_time - self.timer_data[project_id]['start_time']).total_seconds()
                
                log_entry = {
                    'id': len(self.logs) + 1,
                    'project_id': project_id,
                    'duration': duration,
                    'start_time': self.timer_data[project_id]['start_time'].isoformat(),
                    'end_time': end_time.isoformat()
                }
                self.logs.append(log_entry)
                
                self.timer_data[project_id]['is_running'] = False
                return jsonify({'status': 'stopped', 'duration': duration})
            return jsonify({'status': 'error'}), 400
        
        @self.app.route('/settings', methods=['POST'])
        def save_settings():
            self.settings['jira_base_url'] = request.form['jira_base_url']
            self.settings['username'] = request.form['username']
            self.settings['api_key'] = request.form['api_key']
            return jsonify({'status': 'saved'})
        
        @self.app.route('/settings')
        def get_settings():
            return jsonify(self.settings)
        
        @self.app.route('/jira/projects')
        def fetch_jira_projects():
            if not self.settings.get('jira_base_url') or not self.settings.get('api_key'):
                return jsonify({'error': 'Jira settings not configured'}), 400
            
            try:
                # This would be the real API call in production
                # For testing, we'll mock this
                headers = {
                    'Authorization': f'Basic {self.settings["api_key"]}',
                    'Accept': 'application/json'
                }
                response = requests.get(f'{self.settings["jira_base_url"]}/rest/api/2/project', headers=headers)
                return jsonify(response.json())
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/logs')
        def get_logs():
            return jsonify(self.logs)

# Create the app instance
app_instance = TimeTrackerApp()
app = app_instance.app

if __name__ == '__main__':
    app.run(debug=True)