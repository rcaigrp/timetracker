import json
import os

class Storage:
    def __init__(self, db_path='data.json'):
        self.db_path = db_path
        self.data = self.load()

    def load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return []

    def save(self, data):
        with open(self.db_path, 'w') as f:
            json.dump(data, f)

    def add_entry(self, entry):
        self.data.append(entry)
        self.save(self.data)

    def get_entries(self):
        return self.data
