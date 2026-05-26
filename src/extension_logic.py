import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import csv
import io
from datetime import datetime
from src.storage import LocalStorage

class ExtensionLogic:
    def __init__(self):
        self.storage = LocalStorage()
        self.timer = None

    def start_timer(self, project_name):
        self.timer = {
            'start': datetime.now(),
            'paused': False,
            'project': project_name,
            'elapsed': 0
        }

    def pause_timer(self):
        if self.timer and not self.timer['paused']:
            self.timer['paused'] = True

    def resume_timer(self):
        if self.timer and self.timer['paused']:
            self.timer['paused'] = False

    def stop_timer(self):
        if self.timer and not self.timer['paused']:
            self.timer['paused'] = True
            self.timer['end'] = datetime.now()
            self.timer['duration'] = self.timer['end'] - self.timer['start']
            entry = {
                'id': 'entry_' + str(len(self.storage.get('entries') or []) + 1),
                'project': self.timer['project'],
                'date': self.timer['end'].strftime('%Y-%m-%d'),
                'startTime': self.timer['start'].strftime('%H:%M'),
                'endTime': self.timer['end'].strftime('%H:%M'),
                'duration': self.timer['duration'].total_seconds(),
                'notes': ''
            }
            entries = self.storage.get('entries') or []
            entries.append(entry)
            self.storage.set('entries', entries)
            self.timer = None
            return entry
        return None

    def manual_entry(self, project, date, duration_hours, duration_minutes, notes):
        entry = {
            'id': 'manual_' + str(len(self.storage.get('entries') or []) + 1),
            'project': project,
            'date': date,
            'startTime': '00:00',
            'endTime': '00:00',
            'duration': duration_hours * 3600 + duration_minutes * 60,
            'notes': notes
        }
        entries = self.storage.get('entries') or []
        entries.append(entry)
        self.storage.set('entries', entries)
        return entry

    def export_json(self):
        entries = self.storage.get('entries') or []
        return json.dumps(entries, indent=2)

    def export_csv(self):
        entries = self.storage.get('entries') or []
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['id', 'project', 'date', 'startTime', 'endTime', 'duration', 'notes'])
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)
        return output.getvalue()

    def clear_storage(self):
        self.storage.clear()
