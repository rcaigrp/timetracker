import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.storage import Storage
from src.networking import JiraClient

class PythonBridge:
    def __init__(self):
        self.storage = Storage()
        self.jira_client = None

    def set_jira_config(self, base_url, username, api_key):
        self.jira_client = JiraClient(base_url, username, api_key)

    def get_entries(self):
        return self.storage.get_entries()

    def add_entry(self, entry):
        self.storage.add_entry(entry)

    def fetch_jira_projects(self):
        if self.jira_client:
            return self.jira_client.get_projects()
        return []
