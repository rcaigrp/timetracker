import json
import sys
from datetime import datetime

class TimeTracker:
    def __init__(self, filename='time_tracker.json'):
        self.filename = filename
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

    def start_task(self, task_name):
        if task_name in self.data:
            print(f"Task '{task_name}' is already running.")
            return False
        
        self.data[task_name] = {
            'start': datetime.now().isoformat(),
            'end': None
        }
        self.save_data()
        print(f"Started task: {task_name}")
        return True

    def stop_task(self, task_name):
        if task_name not in self.data:
            print(f"Task '{task_name}' not found.")
            return False
        
        if self.data[task_name]['end'] is not None:
            print(f"Task '{task_name}' is already stopped.")
            return False
        
        self.data[task_name]['end'] = datetime.now().isoformat()
        self.save_data()
        print(f"Stopped task: {task_name}")
        return True

    def list_tasks(self):
        if not self.data:
            print("No tasks recorded.")
            return
        
        for task_name, times in self.data.items():
            start = datetime.fromisoformat(times['start'])
            end = datetime.fromisoformat(times['end']) if times['end'] else None
            duration = "Running" if not end else str(end - start)
            print(f"{task_name}: {duration}")

    def run(self):
        if len(sys.argv) < 2:
            print("Usage: python main.py [start|stop|list] [task_name]")
            return
        
        command = sys.argv[1]
        
        if command == 'start' and len(sys.argv) > 2:
            self.start_task(sys.argv[2])
        elif command == 'stop' and len(sys.argv) > 2:
            self.stop_task(sys.argv[2])
        elif command == 'list':
            self.list_tasks()
        else:
            print("Usage: python main.py [start|stop|list] [task_name]")

if __name__ == "__main__":
    tracker = TimeTracker()
    tracker.run()