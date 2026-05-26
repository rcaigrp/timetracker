import json
import os
from typing import List, Dict

class Storage:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.entries_file = os.path.join(data_dir, "entries.json")
        self.settings_file = os.path.join(data_dir, "settings.json")

    def save_entry(self, entry: Dict):
        entries = self.load_entries()
        entries.append(entry)
        with open(self.entries_file, 'w') as f:
            json.dump(entries, f)

    def load_entries(self) -> List[Dict]:
        if not os.path.exists(self.entries_file):
            return []
        with open(self.entries_file, 'r') as f:
            return json.load(f)

    def save_settings(self, settings: Dict):
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def load_settings(self) -> Dict:
        if not os.path.exists(self.settings_file):
            return {}
        with open(self.settings_file, 'r') as f:
            return json.load(f)
