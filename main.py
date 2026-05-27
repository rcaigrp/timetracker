from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from datetime import datetime

class TimeTracker:
    def __init__(self, db_path="timetracker.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                jira_id TEXT
            )''')
        
        # Create time_entries table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                start_time TEXT NOT NULL,
                end_time TEXT,
                duration INTEGER,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            )''')
        
        conn.commit()
        conn.close()

    def get_projects(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, jira_id FROM projects")
        rows = cursor.fetchall()
        projects = [{'id': row[0], 'name': row[1], 'jira_id': row[2]} for row in rows]
        conn.close()
        return projects

    def create_project(self, name, jira_id=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO projects (name, jira_id) VALUES (?, ?)", (name, jira_id))
        conn.commit()
        project_id = cursor.lastrowid
        conn.close()
        return {'id': project_id, 'name': name, 'jira_id': jira_id}

    def get_time_entries(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, project_id, start_time, end_time, duration FROM time_entries")
        rows = cursor.fetchall()
        entries = [{'id': row[0], 'project_id': row[1], 'start_time': row[2], 'end_time': row[3], 'duration': row[4]} for row in rows]
        conn.close()
        return entries

    def create_time_entry(self, project_id, start_time, end_time=None, duration=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO time_entries (project_id, start_time, end_time, duration) VALUES (?, ?, ?, ?)", 
                      (project_id, start_time, end_time, duration))
        conn.commit()
        entry_id = cursor.lastrowid
        conn.close()
        return {'id': entry_id, 'project_id': project_id, 'start_time': start_time, 'end_time': end_time, 'duration': duration}

app = Flask(__name__)
time_tracker = TimeTracker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/projects', methods=['GET'])
def get_projects():
    projects = time_tracker.get_projects()
    return jsonify(projects)

@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.json
    project = time_tracker.create_project(data['name'], data.get('jira_id'))
    return jsonify(project)

@app.route('/api/time_entries', methods=['GET'])
def get_time_entries():
    entries = time_tracker.get_time_entries()
    return jsonify(entries)

@app.route('/api/time_entries', methods=['POST'])
def create_time_entry():
    data = request.json
    entry = time_tracker.create_time_entry(
        data['project_id'], 
        data['start_time'], 
        data.get('end_time'), 
        data.get('duration')
    )
    return jsonify(entry)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)