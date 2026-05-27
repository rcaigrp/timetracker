#!/usr/bin/env python3

import json
from flask import Flask, request, jsonify
import os

class TimeTracker:
    def __init__(self, data_file="time_tracker.json"):
        self.data_file = data_file
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def start_timer(self, task_name):
        if task_name not in self.data:
            self.data[task_name] = {
                "start_time": None,
                "elapsed_time": 0,
                "is_running": False
            }
        
        if not self.data[task_name]["is_running"]:
            self.data[task_name]["start_time"] = self.get_current_timestamp()
            self.data[task_name]["is_running"] = True
            self.save_data()
            return True
        return False

    def stop_timer(self, task_name):
        if task_name in self.data and self.data[task_name]["is_running"]:
            end_time = self.get_current_timestamp()
            start_time = self.data[task_name]["start_time"]
            self.data[task_name]["elapsed_time"] += (end_time - start_time)
            self.data[task_name]["is_running"] = False
            self.data[task_name]["start_time"] = None
            self.save_data()
            return True
        return False

    def get_current_timestamp(self):
        import time
        return time.time()

    def list_tasks(self):
        return self.data

# Initialize Flask app
app = Flask(__name__)
time_tracker = TimeTracker()

@app.route('/start', methods=['POST'])
def start_task():
    data = request.get_json()
    task_name = data.get('task_name')
    if not task_name:
        return jsonify({'error': 'Task name is required'}), 400
    
    success = time_tracker.start_timer(task_name)
    if success:
        return jsonify({'message': f'Timer started for {task_name}'}), 200
    else:
        return jsonify({'error': f'Timer already running for {task_name}'}), 400

@app.route('/stop', methods=['POST'])
def stop_task():
    data = request.get_json()
    task_name = data.get('task_name')
    if not task_name:
        return jsonify({'error': 'Task name is required'}), 400
    
    success = time_tracker.stop_timer(task_name)
    if success:
        return jsonify({'message': f'Timer stopped for {task_name}'}), 200
    else:
        return jsonify({'error': f'Timer not running for {task_name}'}), 400

@app.route('/list', methods=['GET'])
def list_tasks():
    tasks = time_tracker.list_tasks()
    return jsonify(tasks), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)