import json
import csv

class Exporter:
    def __init__(self):
        pass

    def to_json(self, entries):
        return json.dumps(entries, indent=2)

    def to_csv(self, entries):
        if not entries:
            return ""
        keys = entries[0].keys()
        return '\n'.join(','.join(str(v) for v in e.values()) for e in entries)
