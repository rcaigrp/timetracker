import json
import os
import tempfile
from datetime import datetime
from unittest.mock import patch

class MockTimeTracker:
    def __init__(self, filename='time_tracker.json'):
        self.filename = filename
        self.data = {}

    def _load_data(self):
        return self.data

    def save_data(self):
        pass

    def start_task(self, task_name):
        self.data[task_name] = {
            'start': datetime.now().isoformat(),
            'end': None
        }
        return True

    def stop_task(self, task_name):
        if task_name not in self.data:
            return False
        
        self.data[task_name]['end'] = datetime.now().isoformat()
        return True

    def list_tasks(self):
        return self.data

def test_criterion_1_start_task():
    tracker = MockTimeTracker()
    assert tracker.start_task('test_task') == True
    assert 'test_task' in tracker.data
    assert tracker.data['test_task']['end'] is None

def test_criterion_2_stop_task():
    tracker = MockTimeTracker()
    tracker.start_task('test_task')
    assert tracker.stop_task('test_task') == True
    assert tracker.data['test_task']['end'] is not None

def test_criterion_3_list_tasks():
    tracker = MockTimeTracker()
    tracker.start_task('task1')
    tracker.start_task('task2')
    tasks = tracker.list_tasks()
    assert len(tasks) == 2