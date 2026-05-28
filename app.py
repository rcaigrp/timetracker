import json
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_file = 'time_tracker.json'

CONFIG = {
    'JIRA_BASE_URL': '',
    'JIRA_API_KEY': '',
    'JIRA_USERNAME': ''
}

# Load config
if os.path.exists(data_file):
    try:
        with open(data_file, 'r') as f:
            data = json.load(f)
            CONFIG.update(data.get('config', {}))
    except (json.JSONDecodeError, FileNotFoundError):
        pass

def save_config():
    with open(data_file, 'w') as f:
        json.dump({'config': CONFIG}, f)

class Timer(BaseModel):
    running: bool = False
    log: Optional[dict] = None

@app.get("/api/settings")
def get_settings():
    return CONFIG

@app.post("/api/settings")
def post_settings(data: dict):
    CONFIG['JIRA_BASE_URL'] = data.get('JIRA_BASE_URL')
    CONFIG['JIRA_API_KEY'] = data.get('JIRA_API_KEY')
    CONFIG['JIRA_USERNAME'] = data.get('JIRA_USERNAME')
    save_config()
    return {'status': 'success', 'config': CONFIG}

# Mock Project response
class ProjectItem(BaseModel):
    id: str
    name: str
    key: str

@app.get("/api/projects")
def get_projects():
    if not CONFIG.get('JIRA_BASE_URL'):
        raise HTTPException(status_code=400, detail="Jira settings not configured")
    return [
        ProjectItem(id="PROJ1", name="Development", key="DEV"),
        ProjectItem(id="PROJ2", name="Design", key="DES")
    ]

class TimerManager:
    def __init__(self):
        self.running = False
        self.start_time = None
        self.logs = []

    def start(self):
        self.running = True
        self.start_time = datetime.now()
        log_entry = {
            "start": self.start_time.isoformat(),
            "end": None,
            "duration": 0.0,
            "project": "DEV"
        }
        self.logs.append(log_entry)
        return {"running": True, "log": log_entry}

    def stop(self):
        if self.running:
            self.running = False
            now = datetime.now()
            log = self.logs[-1]
            duration = (now - self.start_time).total_seconds()
            log["end"] = now.isoformat()
            log["duration"] = duration
            return {"running": False, "log": log}
        raise HTTPException(status_code=400, detail="Timer not running")

timer = TimerManager()

@app.get("/api/timer")
def get_timer():
    return {"running": timer.running, "log": timer.logs[-1] if timer.logs else None}

@app.post("/api/timer/start")
def start_timer():
    return timer.start()

@app.post("/api/timer/stop")
def stop_timer():
    return timer.stop()
