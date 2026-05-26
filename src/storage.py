import json
import os

class Storage:
    def __init__(self, filepath='entries.json'):
        self.filepath = filepath
        self.entries = self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.entries, f)

    def add_entry(self, entry):
        self.entries.append(entry)
        self.save()

    def get_entries(self):
        return self.entries

    def clear(self):
        self.entries = []
        self.save()
