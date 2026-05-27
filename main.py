from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os

class Project(BaseModel):
    id: Optional[int] = None
    name: str


class TimeEntry(BaseModel):
    id: Optional[int] = None
    project_id: int
    start_time: str
    end_time: Optional[str] = None
    duration: Optional[int] = None


class Settings(BaseModel):
    jira_base_url: str
    jira_username: str
    jira_api_token: str


app = FastAPI()

# In-memory storage for demonstration (in real app, use database)
projects = []
time_entries = []
settings = None

@app.get("/")
def read_root():
    return {"message": "TimeTracker API is running"}

@app.get("/projects", response_model=List[Project])
def get_projects():
    return projects

@app.post("/projects", response_model=Project)
def create_project(project: Project):
    project.id = len(projects) + 1
    projects.append(project)
    return project

@app.get("/time_entries", response_model=List[TimeEntry])
def get_time_entries():
    return time_entries

@app.post("/time_entries", response_model=TimeEntry)
def create_time_entry(entry: TimeEntry):
    entry.id = len(time_entries) + 1
    time_entries.append(entry)
    return entry

@app.get("/settings")
def get_settings():
    if settings is None:
        raise HTTPException(status_code=404, detail="Settings not configured")
    return settings

@app.post("/settings")
def set_settings(new_settings: Settings):
    global settings
    settings = new_settings
    return {"message": "Settings saved successfully"}

# Mock Jira API integration
@app.get("/jira/projects")
def get_jira_projects():
    if settings is None:
        raise HTTPException(status_code=400, detail="Jira settings not configured")
    # In a real implementation, this would call the actual Jira API
    return {"projects": [{"id": 1, "name": "Project Alpha"}, {"id": 2, "name": "Project Beta"}]}
