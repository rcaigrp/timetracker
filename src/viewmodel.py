import time
import uuid
from src.storage import Storage
from src.networking import JiraClient

class ViewModel:
    def __init__(self):
        self.storage = Storage()
        self.jira_client = JiraClient()
        self.timer_state = self.storage.get_timer_state() or {
            'status': 'stopped',
            'start_time': None,
            'elapsed': 0
        }
        self.entries = self.storage.get_entries() or []

    def start_timer(self):
        self.timer_state['status'] = 'running'
        self.timer_state['start_time'] = time.time()
        self.timer_state['elapsed'] = 0
        self.storage.set_timer_state(self.timer_state)

    def pause_timer(self):
        if self.timer_state['status'] == 'running':
            self.timer_state['elapsed'] += time.time() - self.timer_state['start_time']
            self.timer_state['status'] = 'paused'
            self.timer_state['start_time'] = None
            self.storage.set_timer_state(self.timer_state)

    def stop_timer(self):
        if self.timer_state['status'] == 'running':
            self.timer_state['elapsed'] += time.time() - self.timer_state['start_time']
            self.timer_state['status'] = 'stopped'
            self.timer_state['start_time'] = None
            self.storage.set_timer_state(self.timer_state)
            self._save_entry()

    def _save_entry(self):
        entry = {
            'id': str(uuid.uuid4()),
            'project': 'Custom Project',
            'date': time.strftime('%Y-%m-%d'),
            'startTime': self.timer_state['start_time'],
            'endTime': time.time(),
            'duration': self.timer_state['elapsed'],
            'notes': ''
        }
        self.storage.save_entry(entry)
        self.entries = self.storage.get_entries()

    def get_elapsed_time(self):
        if self.timer_state['status'] == 'running':
            return self.timer_state['elapsed'] + (time.time() - self.timer_state['start_time'])
        return self.timer_state['elapsed']

    def configure_jira(self, base_url, username, api_key):
        self.jira_client.set_credentials(base_url, username, api_key)
        self.storage.save_settings({'base_url': base_url, 'username': username, 'api_key': api_key})

    def get_jira_projects(self):
        return self.jira_client.fetch_projects()