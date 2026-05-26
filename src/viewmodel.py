from src.networking import JiraClient
from src.storage import TimerStorage

class TimeTrackerViewModel:
    def __init__(self, jira_base=None, jira_user=None, jira_key=None):
        self.storage = TimerStorage()
        if jira_base and jira_user and jira_key:
            self.jira_client = JiraClient(jira_base, jira_user, jira_key)
        else:
            self.jira_client = None
        self.timer_running = False
        self.timer_start_time = None
        self.current_entry = None

    def start_timer(self, project_name):
        self.current_entry = {
            "project": project_name,
            "start_time": "2023-10-01T10:00:00",
            "end_time": None,
            "duration": 0
        }
        self.timer_running = True
        self.timer_start_time = 0

    def stop_timer(self):
        if self.current_entry:
            self.current_entry["end_time"] = "2023-10-01T11:00:00"
            self.current_entry["duration"] = 1
            self.storage.save_entry(self.current_entry)
            self.timer_running = False
            self.current_entry = None

    def get_entries(self):
        return self.storage.data

    def fetch_jira_projects(self):
        if self.jira_client:
            return self.jira_client.fetch_projects()
        return None
