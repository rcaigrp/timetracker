import sqlite3
import os
import tempfile
from unittest.mock import patch
from datetime import datetime
import pytest

class TestTimeTracker:
    def setup_method(self):
        self.db_name = 'test_timetracker.db'
        # Import here to avoid circular imports
        from main import TimeTracker
        self.tracker = TimeTracker(self.db_name)

    def teardown_method(self):
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_criterion_1_start_tracking(self):
        # Test that we can start tracking a project
        self.tracker.start_tracking('Test Project')
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM time_entries WHERE project_name = ?", ('Test Project',))
        entry = cursor.fetchone()
        conn.close()
        
        assert entry is not None
        assert entry[1] == 'Test Project'
        assert entry[3] is None  # end_time should be None

    def test_criterion_2_stop_tracking(self):
        # Test that we can stop tracking a project
        self.tracker.start_tracking('Test Project')
        self.tracker.stop_tracking('Test Project')
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM time_entries WHERE project_name = ?", ('Test Project',))
        entry = cursor.fetchone()
        conn.close()
        
        assert entry is not None
        assert entry[3] is not None  # end_time should be set

    def test_criterion_3_list_projects(self):
        # Test that we can list projects
        self.tracker.start_tracking('Project Alpha')
        self.tracker.start_tracking('Project Beta')
        
        # Capture stdout
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            self.tracker.list_projects()
        output = f.getvalue()
        
        assert 'Project Alpha' in output
        assert 'Project Beta' in output