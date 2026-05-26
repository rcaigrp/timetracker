from storage import Storage
from networking import JiraClient

class PythonBridge:
    def __init__(self):
        self.storage = Storage()
        self.jira = None

    def init_jira(self, base_url, username, api_key):
        self.jira = JiraClient(base_url, username, api_key)

    def save_entry(self, entry):
        self.storage.add_entry(entry)

    def get_entries(self):
        return self.storage.get_entries()

    def get_projects(self):
        if self.jira:
            return self.jira.get_projects()
        return []
