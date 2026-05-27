import json
import sys
from datetime import datetime

class TimerService:
    def __init__(self, filename='time_tracker.json'):
        self.filename = filename
        self.current_project = None
        self.is_running = False
        self.start_time = None
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=2)

    def start_timer(self, project_name):
        self.current_project = project_name
        self.is_running = True
        self.start_time = datetime.now()

    def stop_timer(self):
        if self.is_running and self.current_project:
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            
            if self.current_project not in self.data:
                self.data[self.current_project] = {'total_seconds': 0}
            
            self.data[self.current_project]['total_seconds'] += duration
            self.save_data()
            
            self.is_running = False
            self.current_project = None
            self.start_time = None
