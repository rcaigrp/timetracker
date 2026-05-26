import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.elapsed = 0
        self.running = False

    def start(self):
        self.running = True
        self.start_time = time.time()

    def pause(self):
        if self.running:
            self.running = False
            self.elapsed += time.time() - self.start_time

    def stop(self):
        if self.running:
            self.running = False
            self.elapsed += time.time() - self.start_time
            return self.elapsed
        return 0

    def get_elapsed(self):
        if self.running:
            return self.elapsed + (time.time() - self.start_time)
        return self.elapsed
