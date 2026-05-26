from src.timer import Timer
from src.storage import Storage
from src.exporter import Exporter

class DashboardViewModel:
    def __init__(self):
        self.timer = Timer()
        self.storage = Storage()
        self.exporter = Exporter()
        self.entries = []

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        duration = self.timer.stop()
        if duration > 0:
            entry = {
                'project': 'Current Project',
                'duration': duration,
                'date': 'Today'
            }
            self.storage.add_entry(entry)
            return entry
        return None
