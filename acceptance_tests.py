import os
import sqlite3
import tempfile
from unittest.mock import patch

def test_criterion_1_track_time():
    # Test that we can start and stop tasks
    from main import TaskManager
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'timetracker.db')
        tm = TaskManager(db_path)
        
        # Start a task
        tm.start_task('test_task')
        
        # Stop the task
        tm.stop_task('test_task')
        
        # Check that task was recorded in database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        result = cursor.fetchall()
        assert len(result) == 1
        conn.close()
        

def test_criterion_2_list_active_tasks():
    # Test listing of active tasks
    from main import TaskManager
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'timetracker.db')
        tm = TaskManager(db_path)
        
        # Start a task
        tm.start_task('test_task')
        
        # List active tasks
        active_tasks = tm.list_active_tasks()
        assert 'test_task' in active_tasks
        

def test_criterion_3_persist_data():
    # Test that data persists between sessions
    from main import TaskManager
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'timetracker.db')
        tm1 = TaskManager(db_path)
        
        # Start and stop a task
        tm1.start_task('persistent_task')
        tm1.stop_task('persistent_task')
        
        # Create new instance to verify persistence
        tm2 = TaskManager(db_path)
        
        # Check that task was recorded in database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        result = cursor.fetchall()
        assert len(result) == 1
        conn.close()