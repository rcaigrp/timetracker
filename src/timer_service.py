import uuid
import time
from src.models import TimeEntry, Project
from src.storage import LocalStorage

class TimerService:
    def __init__(self, storage: LocalStorage):
        self.storage = storage
        self.timer_entry: TimeEntry | None = None
        self.start_time: float = 0
        self.paused: bool = False
        self.paused_duration: float = 0

    def start_timer(self, project: Project) -> TimeEntry:
        self.timer_entry = TimeEntry(
            id=str(uuid.uuid4()),
            project_id=project.id,
            start_time=datetime.fromtimestamp(time.time()),
            notes=""
        )
        self.start_time = time.time()
        self.paused = False
        self.paused_duration = 0
        self.storage.save_entry(self.timer_entry)
        return self.timer_entry

    def pause_timer(self):
        if self.timer_entry and not self.paused:
            self.paused = True
            self.paused_duration = time.time() - self.start_time

    def resume_timer(self):
        if self.timer_entry and self.paused:
            self.paused = False
            self.start_time = time.time() - self.paused_duration
            self.paused_duration = 0

    def stop_timer(self) -> TimeEntry:
        if self.timer_entry:
            self.timer_entry.end_time = datetime.fromtimestamp(time.time())
            self.timer_entry.duration_seconds = int(self.timer_entry.end_time.timestamp() - self.timer_entry.start_time.timestamp())
            self.storage.update_entry(self.timer_entry)
            entry = self.timer_entry
            self.timer_entry = None
            self.start_time = 0
            self.paused = False
            self.paused_duration = 0
            return entry
        return None

    def get_elapsed(self) -> float:
        if self.timer_entry and not self.paused:
            return time.time() - self.start_time
        return 0
