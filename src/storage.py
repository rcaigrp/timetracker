import json
import os

class StorageManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.entries_file = os.path.join(data_dir, 'entries.json')
        self.settings_file = os.path.join(data_dir, 'settings.json')
        self._load_entries()
        self._load_settings()

    def _load_entries(self):
        if os.path.exists(self.entries_file):
            with open(self.entries_file, 'r') as f:
                self.entries = json.load(f)
        else:
            self.entries = []

    def save_entries(self):
        with open(self.entries_file, 'w') as f:
            json.dump(self.entries, f)

    def add_entry(self, entry):
        self.entries.append(entry)
        self.save_entries()

    def get_entries(self):
        return self.entries

    def _load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}

    def save_settings(self, base_url, username, api_key):
        self.settings = {
            'base_url': base_url,
            'username': username,
            'api_key': api_key
        }
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f)

    def get_settings(self):
        return self.settings
