import time
import threading
from datetime import datetime, timedelta

class TimerService:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.lock = threading.Lock()

    def start(self):
        with self.lock:
            if not self.is_running:
                self.start_time = datetime.now()
                self.is_running = True

    def stop(self):
        with self.lock:
            if self.is_running:
                elapsed = datetime.now() - self.start_time
                self.elapsed_time += elapsed.total_seconds()
                self.is_running = False

    def reset(self):
        with self.lock:
            self.start_time = None
            self.elapsed_time = 0
            self.is_running = False

    def get_elapsed_time(self):
        with self.lock:
            if self.is_running:
                current_elapsed = (datetime.now() - self.start_time).total_seconds()
                return self.elapsed_time + current_elapsed
            return self.elapsed_time

    def is_timer_running(self):
        return self.is_running

def main():
    timer_service = TimerService()
    
    while True:
        command = input("Enter command (start/stop/reset/status/quit): ").strip().lower()
        
        if command == 'start':
            timer_service.start()
            print("Timer started.")
        elif command == 'stop':
            timer_service.stop()
            print("Timer stopped.")
        elif command == 'reset':
            timer_service.reset()
            print("Timer reset.")
        elif command == 'status':
            elapsed = timer_service.get_elapsed_time()
            running = timer_service.is_timer_running()
            print(f"Elapsed time: {elapsed:.2f} seconds, Running: {running}")
        elif command == 'quit':
            break
        else:
            print("Unknown command. Try again.")

if __name__ == "__main__":
    main()