import json
import os

DATA_FILE = "time_entries.json"

def save_entries(entries):
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f)

def load_entries():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)
