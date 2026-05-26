import json
import time
import random

class TimerEntry:
    def __init__(self, id, project, date, start_time, end_time, duration, notes):
        self.id = id
        self.project = project
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.notes = notes

    def to_dict(self):
        return {
            "id": self.id,
            "project": self.project,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["project"],
            data["date"],
            data["start_time"],
            data["end_time"],
            data["duration"],
            data["notes"]
        )

class Project:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"])

class Settings:
    def __init__(self, base_url, username, api_key):
        self.base_url = base_url
        self.username = username
        self.api_key = api_key

    def to_dict(self):
        return {
            "base_url": self.base_url,
            "username": self.username,
            "api_key": self.api_key
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["base_url"], data["username"], data["api_key"])

class Storage:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def load(self, key):
        return self.data.get(key)

class Networking:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.projects = []

    def fetch_projects(self):
        # Simulate fetching projects from Jira
        if self.settings and self.settings.base_url:
            self.projects = [
                Project("1", "Project A"),
                Project("2", "Project B")
            ]
            return self.projects
        return []

class App:
    def __init__(self):
        self.storage = Storage()
        self.networking = None
        self.settings = None
        self.timer_entries = []
        self.timer_running = False
        self.timer_start_time = None

    def load_entries(self):
        data = self.storage.load("timer_entries")
        if data:
            self.timer_entries = [TimerEntry.from_dict(e) for e in data]
        else:
            self.timer_entries = []

    def save_entries(self):
        self.storage.save("timer_entries", [e.to_dict() for e in self.timer_entries])

    def start_timer(self, project_name):
        self.timer_running = True
        self.timer_start_time = time.time()
        entry = TimerEntry(
            id=str(random.randint(1000, 9999)),
            project=project_name,
            date=time.strftime("%Y-%m-%d"),
            start_time=self.timer_start_time,
            end_time=None,
            duration=0,
            notes=""
        )
        self.timer_entries.append(entry)
        self.save_entries()

    def stop_timer(self):
        if self.timer_running:
            end_time = time.time()
            duration = end_time - self.timer_start_time
            if self.timer_entries:
                self.timer_entries[-1].end_time = end_time
                self.timer_entries[-1].duration = duration
                self.timer_entries[-1].notes = "Manual entry"
                self.save_entries()
            self.timer_running = False
            self.timer_start_time = None

    def get_elapsed_time(self):
        if self.timer_running:
            return time.time() - self.timer_start_time
        return 0

    def configure_settings(self, base_url, username, api_key):
        self.settings = Settings(base_url, username, api_key)
        self.storage.save("settings", self.settings.to_dict())
        self.networking = Networking(self.settings)

    def load_settings(self):
        data = self.storage.load("settings")
        if data:
            self.settings = Settings.from_dict(data)
            self.networking = Networking(self.settings)

    def fetch_projects(self):
        if self.networking:
            return self.networking.fetch_projects()
        return []

    def background_suspend(self):
        if self.timer_running:
            self.stop_timer()

    def background_resume(self):
        if self.settings:
            self.load_entries()
