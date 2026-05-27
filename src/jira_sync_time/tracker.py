#!/usr/bin/env python3
"""
Time tracker that monitors active git repos and IDEs to map time to Jira issues.
"""

import psutil
import os
import time
from datetime import datetime
from .storage import TimeStorage


class TimeTracker:
    def __init__(self):
        self.storage = TimeStorage()
        self.current_tracking = None

    def start_tracking(self, issue_key):
        """Start tracking time for a specific Jira issue."""
        # Check if already tracking
        if self.current_tracking:
            raise Exception("Already tracking time. Stop current tracking first.")
        
        # Store start time
        start_time = datetime.now()
        
        # Create new log entry
        log_id = self.storage.add_log(issue_key, start_time, None, 'process')
        self.current_tracking = {
            'id': log_id,
            'issue_key': issue_key,
            'start_time': start_time
        }
        
        return log_id

    def stop_tracking(self):
        """Stop current time tracking."""
        if not self.current_tracking:
            raise Exception("No active tracking to stop.")
        
        end_time = datetime.now()
        
        # Update the log entry with end time
        self.storage.update_log(self.current_tracking['id'], end_time)
        
        # Clear current tracking state
        self.current_tracking = None
        
        return True

    def get_active_processes(self):
        """Get list of active processes that might be related to development."""
        dev_processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Check if process is a common IDE or git
                process_name = proc.info['name'].lower()
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                
                if any(ide in process_name for ide in ['idea', 'pycharm', 'vscode', 'sublime', 'atom']) or \
                   'git' in process_name or 'git' in cmdline:
                    dev_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process might have terminated or we don't have access
                pass
        
        return dev_processes

    def get_active_git_repos(self):
        """Check for active git repositories in current directory and parent directories."""
        active_repos = []
        current_path = os.getcwd()
        
        # Walk up the directory tree looking for .git directories
        while True:
            git_dir = os.path.join(current_path, '.git')
            if os.path.exists(git_dir):
                active_repos.append(current_path)
                break
            
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:  # Reached root directory
                break
            current_path = parent_path
        
        return active_repos
