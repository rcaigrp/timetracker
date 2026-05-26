import time

class TimerManager:
    def __init__(self):
        self.is_running = False
        self.start_time = None
        self.accumulated_time = 0

    def start(self):
        self.is_running = True
        self.start_time = time.time()
        self.accumulated_time = 0

    def pause(self):
        if self.is_running:
            self.accumulated_time += time.time() - self.start_time
            self.is_running = False
            self.start_time = None

    def stop(self):
        if self.is_running:
            self.accumulated_time += time.time() - self.start_time
            self.is_running = False
            self.start_time = None

    def resume(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def get_elapsed(self):
        if self.is_running:
            return self.accumulated_time + (time.time() - self.start_time)
        return self.accumulated_time
