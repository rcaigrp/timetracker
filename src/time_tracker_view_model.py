import json
import time
import os

class TimeTrackerViewModel:
    def __init__(self, storage_path='storage.json'):
        self.storage_path = storage_path
        self.projects = []
        self.timer = None
        self.config = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                self.projects = data.get('projects', [])
                self.timer = data.get('timer', None)
                self.config = data.get('config', {})

    def save_data(self):
        data = {
            'projects': self.projects,
            'timer': self.timer,
            'config': self.config
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f)

    def start_timer(self):
        self.timer = {
            'start_time': time.time(),
            'end_time': None,
            'duration': 0,
            'project': None
        }
        self.save_data()

    def pause_timer(self):
        if self.timer and self.timer['end_time'] is None:
            self.timer['end_time'] = time.time()
            self.timer['duration'] += self.timer['end_time'] - self.timer['start_time']
            self.timer['start_time'] = self.timer['end_time']
            self.save_data()

    def stop_timer(self):
        if self.timer:
            self.timer['end_time'] = time.time()
            self.timer['duration'] += self.timer['end_time'] - self.timer['start_time']
            self.timer['start_time'] = None
            self.timer['end_time'] = self.timer['end_time']
            self.projects.append({
                'id': len(self.projects) + 1,
                'project': self.timer.get('project', 'Unknown'),
                'date': time.strftime('%Y-%m-%d'),
                'duration': self.timer['duration'],
                'notes': ''
            })
            self.timer = None
            self.save_data()

    def add_project(self, name):
        self.projects.append({
            'id': len(self.projects) + 1,
            'project': name,
            'date': time.strftime('%Y-%m-%d'),
            'duration': 0,
            'notes': ''
        })
        self.save_data()

    def get_elapsed_time(self):
        if self.timer and self.timer['end_time'] is None:
            return time.time() - self.timer['start_time']
        elif self.timer:
            return self.timer['duration']
        return 0

    def set_config(self, base_url, username, api_key):
        self.config = {
            'base_url': base_url,
            'username': username,
            'api_key': api_key
        }
        self.save_data()

    def get_config(self):
        return self.config
