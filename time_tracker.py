import json
import os
from datetime import datetime, timedelta
from typing import List, Optional

class Project:
    def __init__(self, name: str):
        self.id = str(hash(name) % (10**8))  # Simple ID generation
        self.name = name
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
    @property
    def duration(self) -> timedelta:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return datetime.now() - self.start_time
        return timedelta(0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None
        }

    @classmethod
    def from_dict(cls, data: dict):
        project = cls(data['name'])
        project.id = data['id']
        if data.get('start_time'):
            project.start_time = datetime.fromisoformat(data['start_time'])
        if data.get('end_time'):
            project.end_time = datetime.fromisoformat(data['end_time'])
        return project

class StorageManager:
    FILE_NAME = 'time_entries.json'
    
    @staticmethod
    def save_projects(projects: List[Project]) -> None:
        data = [p.to_dict() for p in projects]
        with open(StorageManager.FILE_NAME, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_projects() -> List[Project]:
        try:
            with open(StorageManager.FILE_NAME, 'r') as f:
                data = json.load(f)
                return [Project.from_dict(item) for item in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

class TimeTracker:
    def __init__(self):
        self.projects = StorageManager.load_projects()
        
    def start_project(self, name: str) -> None:
        # Check if project already exists
        existing_project = next((p for p in self.projects if p.name == name), None)
        if existing_project and not existing_project.end_time:
            print(f"Project '{name}' is already running.")
            return
        
        # Create new project or restart existing one
        if existing_project:
            self.projects.remove(existing_project)
            
        project = Project(name)
        project.start_time = datetime.now()
        self.projects.append(project)
        StorageManager.save_projects(self.projects)
        print(f"Started tracking '{name}' at {project.start_time}")

    def stop_project(self) -> None:
        running_project = next((p for p in self.projects if p.start_time and not p.end_time), None)
        if not running_project:
            print("No project is currently running.")
            return
        
        running_project.end_time = datetime.now()
        StorageManager.save_projects(self.projects)
        print(f"Stopped tracking '{running_project.name}' after {self.format_duration(running_project.duration)}")

    def list_projects(self) -> None:
        if not self.projects:
            print("No projects tracked yet.")
            return
        
        for project in self.projects:
            duration = project.duration
            status = "Running" if project.start_time and not project.end_time else "Completed"
            print(f"{project.name}: {self.format_duration(duration)} ({status})")

    @staticmethod
    def format_duration(duration: timedelta) -> str:
        total_seconds = int(duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_running_project(self) -> Optional[Project]:
        return next((p for p in self.projects if p.start_time and not p.end_time), None)
