import time
from typing import Optional


class TimeTrackerViewModel:
    def __init__(self):
        self.timer_start: Optional[float] = None
        self.timer_elapsed: float = 0.0
        self.is_timer_running: bool = False
        self.was_running_before_suspension: bool = False
        self.is_suspended: bool = False

    def start_timer(self):
        self.timer_start = time.time()
        self.is_timer_running = True

    def pause_timer(self):
        if self.is_timer_running:
            self.timer_elapsed += time.time() - self.timer_start
            self.timer_start = None
            self.is_timer_running = False

    def stop_timer(self):
        if self.is_timer_running:
            self.timer_elapsed += time.time() - self.timer_start
            self.timer_start = None
            self.is_timer_running = False

    def get_elapsed(self) -> float:
        if self.is_timer_running:
            return self.timer_elapsed + (time.time() - self.timer_start)
        return self.timer_elapsed

    def will_suspension_handler(self):
        self.was_running_before_suspension = self.is_timer_running
        self.is_suspended = True
        if self.is_timer_running:
            self.pause_timer()

    def did_activation_handler(self):
        if self.is_suspended:
            self.is_suspended = False
            if self.was_running_before_suspension and not self.is_timer_running:
                self.timer_start = time.time()
                self.is_timer_running = True
