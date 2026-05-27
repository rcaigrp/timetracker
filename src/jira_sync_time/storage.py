#!/usr/bin/env python3
"""
Local storage for time logs using SQLite.
"""

import sqlite3
import os
from datetime import datetime
from pathlib import Path


class TimeStorage:
    def __init__(self, db_path='time_tracker.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create time_logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS time_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_key TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT,
                source TEXT NOT NULL  -- 'manual' or 'process'
            )''')
        
        conn.commit()
        conn.close()

    def add_log(self, issue_key, start_time, end_time, source):
        """Add a new time log entry."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert datetime to string for storage
        start_time_str = start_time.isoformat() if isinstance(start_time, datetime) else str(start_time)
        end_time_str = end_time.isoformat() if isinstance(end_time, datetime) else str(end_time) if end_time else None
        
        cursor.execute('''
            INSERT INTO time_logs (issue_key, start_time, end_time, source)
            VALUES (?, ?, ?, ?)''', (issue_key, start_time_str, end_time_str, source))
        
        log_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return log_id

    def update_log(self, log_id, end_time):
        """Update an existing time log with end time."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Convert datetime to string for storage
        end_time_str = end_time.isoformat() if isinstance(end_time, datetime) else str(end_time)
        
        cursor.execute('''
            UPDATE time_logs
            SET end_time = ?
            WHERE id = ?''', (end_time_str, log_id))
        
        conn.commit()
        conn.close()

    def get_logs(self):
        """Get all time logs."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, issue_key, start_time, end_time, source
            FROM time_logs
            ORDER BY start_time DESC''')
        
        logs = cursor.fetchall()
        conn.close()
        
        return logs

    def get_active_log(self):
        """Get the currently active log entry (where end_time is NULL)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, issue_key, start_time, end_time, source
            FROM time_logs
            WHERE end_time IS NULL''')
        
        log = cursor.fetchone()
        conn.close()
        
        return log
