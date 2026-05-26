import json
import os
from typing import List, Dict

class StorageManager:
    """
    Secure storage layer for TimeTracker.
    Uses JSON file for persistence.
    """
    def __init__(self, db_path: str = "time_tracker_data.json"):
        self.db_path = db_path
        self.data = self._load()

    def _load(self) -> Dict:
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {
            "entries": [],
            "projects": [],
            "settings": {}
        }

    def _save(self) -> None:
        with open(self.db_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def add_entry(self, entry: Dict) -> None:
        self.data["entries"].append(entry)
        self._save()

    def get_entries(self) -> List[Dict]:
        return self.data["entries"]

    def clear_entries(self) -> None:
        self.data["entries"] = []
        self._save()

    def add_project(self, project: Dict) -> None:
        self.data["projects"].append(project)
        self._save()

    def get_projects(self) -> List[Dict]:
        return self.data["projects"]

    def set_setting(self, key: str, value: str) -> None:
        self.data["settings"][key] = value
        self._save()

    def get_setting(self, key: str) -> str:
        return self.data["settings"].get(key)
