import json
import os

class Storage:
    def __init__(self):
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists('timer_data.json'):
            with open('timer_data.json', 'r') as f:
                self.data = json.load(f)

    def save(self):
        with open('timer_data.json', 'w') as f:
            json.dump(self.data, f)

    def get_timer_state(self):
        return self.data.get('timer_state')

    def set_timer_state(self, state):
        self.data['timer_state'] = state
        self.save()

    def get_entries(self):
        return self.data.get('entries', [])

    def set_entries(self, entries):
        self.data['entries'] = entries
        self.save()

    def save_entry(self, entry):
        entries = self.get_entries()
        entries.append(entry)
        self.set_entries(entries)

    def save_settings(self, settings):
        self.data['settings'] = settings
        self.save()