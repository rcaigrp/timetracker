import uuid
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Project:
    id: str
    name: str
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class TimeEntry:
    id: str
    project_id: str
    start_time: datetime
    end_time: datetime | None = None
    duration_seconds: int = 0
    notes: str = ""
    
    def __post_init__(self):
        if self.end_time:
            self.duration_seconds = int((self.end_time - self.start_time).total_seconds())
