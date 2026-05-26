import json
import os

class TimerStorage:
    def __init__(self, db_path="timer_data.json"):
        self.db_path = db_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return []

    def save_entry(self, entry):
        self.data.append(entry)
        self._save()

    def _save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f)
