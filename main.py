import sqlite3
import time
import os
from datetime import datetime

class TaskManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
        
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_time REAL,
                end_time REAL,
                duration REAL
            )''')
        conn.commit()
        conn.close()
        
    def start_task(self, task_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (name, start_time) VALUES (?, ?)",
            (task_name, time.time())
        )
        conn.commit()
        conn.close()
        print(f"Started task: {task_name}")
        
    def stop_task(self, task_name):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, start_time FROM tasks WHERE name=? AND end_time IS NULL",
            (task_name,)
        )
        result = cursor.fetchone()
        
        if result:
            task_id, start_time = result
            end_time = time.time()
            duration = end_time - start_time
            
            cursor.execute(
                "UPDATE tasks SET end_time=?, duration=? WHERE id=?",
                (end_time, duration, task_id)
            )
            conn.commit()
            print(f"Stopped task: {task_name}, Duration: {duration:.2f} seconds")
        else:
            print(f"Task not found or already stopped: {task_name}")
        
        conn.close()
        
    def list_active_tasks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM tasks WHERE end_time IS NULL"
        )
        active_tasks = [row[0] for row in cursor.fetchall()]
        conn.close()
        return active_tasks
        
    def list_all_tasks(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, start_time, end_time, duration FROM tasks ORDER BY start_time DESC"
        )
        tasks = cursor.fetchall()
        conn.close()
        return tasks
        
    def show_report(self):
        tasks = self.list_all_tasks()
        if not tasks:
            print("No tasks recorded.")
            return
        
        print("\nTime Tracking Report:")
        print("-" * 50)
        for task in tasks:
            name, start_time, end_time, duration = task
            if duration is not None:
                print(f"{name}: {duration:.2f} seconds")
            else:
                print(f"{name}: Active (started at {datetime.fromtimestamp(start_time)})")
        
    def show_active_tasks(self):
        active_tasks = self.list_active_tasks()
        if not active_tasks:
            print("No active tasks.")
        else:
            print("Active tasks:")
            for task in active_tasks:
                print(f"  - {task}")

if __name__ == "__main__":
    import sys
    
    db_path = os.path.join(os.getcwd(), 'timetracker.db')
    tm = TaskManager(db_path)
    
    if len(sys.argv) < 2:
        print("Usage: python main.py [start|stop|list|report]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "start" and len(sys.argv) > 2:
        tm.start_task(sys.argv[2])
    elif command == "stop" and len(sys.argv) > 2:
        tm.stop_task(sys.argv[2])
    elif command == "list":
        tm.show_active_tasks()
    elif command == "report":
        tm.show_report()
    else:
        print("Unknown command or missing arguments")
        sys.exit(1)