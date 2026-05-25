import json
import os
from typing import List, Dict

class LocalStorage:
    def __init__(self, db_path: str = "time_tracker_data.json"):
        self.db_path = db_path
        self.data = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {"entries": [], "settings": {}}

    def save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_entry(self, entry: Dict):
        self.data["entries"].append(entry)
        self.save()

    def get_entries(self) -> List[Dict]:
        return self.data["entries"]

    def update_settings(self, settings: Dict):
        self.data["settings"].update(settings)
        self.save()

    def get_settings(self) -> Dict:
        return self.data["settings"]
