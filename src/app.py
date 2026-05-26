from src.dashboard import DashboardViewModel
from src.settings import SettingsViewModel
from src.timer import TimerViewModel
from src.storage import StorageManager
from src.networking import JiraClient

class App:
    def __init__(self):
        self.dashboard = DashboardViewModel()
        self.settings = SettingsViewModel()
        self.timer = TimerViewModel()
        self.storage = StorageManager()
        self.jira = JiraClient()

    def launch(self):
        self.dashboard.entries = self.storage.get_entries()

    def save_entry(self, entry):
        self.storage.add_entry(entry)
