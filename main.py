import sqlite3
import click
from datetime import datetime

class TimeTracker:
    def __init__(self, db_name='timetracker.db'):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                start_time TEXT,
                end_time TEXT
            )''')
        conn.commit()
        conn.close()

    def start_tracking(self, project_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO time_entries (project_name, start_time) VALUES (?, ?)",
            (project_name, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        print(f"Started tracking {project_name}")

    def stop_tracking(self, project_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE time_entries SET end_time = ? WHERE project_name = ? AND end_time IS NULL",
            (datetime.now().isoformat(), project_name)
        )
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        if rows_affected > 0:
            print(f"Stopped tracking {project_name}")
        else:
            print(f"No active tracking found for {project_name}")

    def list_projects(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT project_name, start_time, end_time FROM time_entries ORDER BY start_time DESC"
        )
        entries = cursor.fetchall()
        conn.close()

        if not entries:
            print("No projects tracked yet.")
            return

        print("Time Tracking Entries:")
        for entry in entries:
            project_name, start_time, end_time = entry
            if end_time:
                print(f"{project_name}: Started at {start_time}, Ended at {end_time}")
            else:
                print(f"{project_name}: Started at {start_time} (currently running)")

@click.group()
def cli():
    pass

@cli.command()
@click.argument('project_name')
def start(project_name):
    tracker = TimeTracker()
    tracker.start_tracking(project_name)

@cli.command()
@click.argument('project_name')
def stop(project_name):
    tracker = TimeTracker()
    tracker.stop_tracking(project_name)

@cli.command()
def list():
    tracker = TimeTracker()
    tracker.list_projects()

if __name__ == '__main__':
    cli()