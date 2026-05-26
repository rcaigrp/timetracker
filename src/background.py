import time
from src.timer_service import TimerService

class BackgroundManager:
    def __init__(self, timer_service: TimerService):
        self.timer_service = timer_service
        self.is_active = True

    def on_suspend(self):
        if self.timer_service.timer_entry and not self.timer_service.paused:
            self.timer_service.pause_timer()

    def on_resume(self):
        if self.timer_service.timer_entry and self.timer_service.paused:
            self.timer_service.resume_timer()
