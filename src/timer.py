import time
from datetime import datetime

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0
        self.is_running = False

    def start(self):
        self.start_time = datetime.now()
        self.is_running = True

    def stop(self):
        if self.is_running:
            self.elapsed += int((datetime.now() - self.start_time).total_seconds())
            self.start_time = None
            self.is_running = False

    def pause(self):
        if self.is_running:
            self.elapsed += int((datetime.now() - self.start_time).total_seconds())
            self.start_time = None
            self.is_running = False

    def resume(self):
        if not self.is_running:
            self.start_time = datetime.now()
            self.is_running = True

    def get_elapsed(self) -> int:
        if self.is_running:
            return self.elapsed + int((datetime.now() - self.start_time).total_seconds())
        return self.elapsed
