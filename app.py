from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import os
from datetime import datetime
import requests

class Project(BaseModel):
    id: Optional[int] = None
    name: str
    key: str

    class Config:
        orm_mode = True

class TimeEntry(BaseModel):
    id: Optional[int] = None
    project_key: str
    task_name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    
    class Config:
        orm_mode = True

class Settings(BaseModel):
    jira_url: str
    username: str
    api_key: str

app = FastAPI(title="TimeTracker API", version="1.0.0")

# Database setup
DATABASE_URL = "sqlite:///./timetracker.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DATABASE_URL.replace("sqlite:///", ""))
    cursor = conn.cursor()
    
    # Create projects table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            key TEXT UNIQUE NOT NULL
        )''')
    
    # Create time entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS time_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_key TEXT NOT NULL,
            task_name TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT
        )''')
    
    # Create settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jira_url TEXT NOT NULL,
            username TEXT NOT NULL,
            api_key TEXT NOT NULL
        )''')
    
    conn.commit()
    conn.close()

# Dependency to get database connection
async def get_db():
    conn = sqlite3.connect(DATABASE_URL.replace("sqlite:///", ""))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "TimeTracker dashboard is running"}

# Project endpoints
@app.post("/projects", response_model=Project)
async def create_project(project: Project, db=Depends(get_db)):
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO projects (name, key) VALUES (?, ?)",
            (project.name, project.key)
        )
        db.commit()
        project.id = cursor.lastrowid
        return project
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Project key already exists")

@app.get("/projects", response_model=List[Project])
async def get_projects(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM projects")
    rows = cursor.fetchall()
    return [Project(id=row['id'], name=row['name'], key=row['key']) for row in rows]

# Time entry endpoints
@app.post("/time_entries/start", response_model=TimeEntry)
async def start_timer(entry: TimeEntry, db=Depends(get_db)):
    cursor = db.cursor()
    entry.start_time = datetime.now()
    cursor.execute(
        "INSERT INTO time_entries (project_key, task_name, start_time) VALUES (?, ?, ?)",
        (entry.project_key, entry.task_name, entry.start_time.isoformat())
    )
    db.commit()
    entry.id = cursor.lastrowid
    return entry

@app.post("/time_entries/stop", response_model=TimeEntry)
async def stop_timer(entry: TimeEntry, db=Depends(get_db)):
    cursor = db.cursor()
    entry.end_time = datetime.now()
    cursor.execute(
        "UPDATE time_entries SET end_time = ? WHERE project_key = ? AND task_name = ? AND end_time IS NULL",
        (entry.end_time.isoformat(), entry.project_key, entry.task_name)
    )
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=400, detail="No active timer found for this task")
    return entry

@app.get("/time_entries", response_model=List[TimeEntry])
async def get_time_entries(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM time_entries")
    rows = cursor.fetchall()
    return [TimeEntry(
        id=row['id'],
        project_key=row['project_key'],
        task_name=row['task_name'],
        start_time=datetime.fromisoformat(row['start_time']),
        end_time=datetime.fromisoformat(row['end_time']) if row['end_time'] else None
    ) for row in rows]

# Settings endpoints
@app.post("/settings", response_model=Settings)
async def set_settings(settings: Settings, db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO settings (id, jira_url, username, api_key) VALUES (1, ?, ?, ?)",
        (settings.jira_url, settings.username, settings.api_key)
    )
    db.commit()
    return settings

@app.get("/settings", response_model=Settings)
async def get_settings(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM settings WHERE id = 1")
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Settings not found")
    return Settings(
        jira_url=row['jira_url'],
        username=row['username'],
        api_key=row['api_key']
    )

# Jira integration endpoints
@app.get("/jira/projects")
async def fetch_jira_projects(db=Depends(get_db)):
    # Get settings from database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM settings WHERE id = 1")
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=400, detail="Jira settings not configured")
    
    jira_url = row['jira_url']
    username = row['username']
    api_key = row['api_key']
    
    # Fetch projects from Jira API
    response = requests.get(
        f"{jira_url}/rest/api/2/project",
        auth=(username, api_key)
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch projects from Jira")
    
    return response.json()

# Test endpoint for development
@app.get("/test")
async def test_endpoint():
    return {"message": "API is working correctly"}