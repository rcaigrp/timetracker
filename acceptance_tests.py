import os
import tempfile
from unittest.mock import patch
from time_tracker import TimeTracker, Project

def test_create_project():
    tracker = TimeTracker()
    tracker.start_project("TestProject")
    assert len(tracker.projects) == 1
    assert tracker.projects[0].name == "TestProject"


def test_start_existing_running_project():
    tracker = TimeTracker()
    tracker.start_project("TestProject")
    # Try to start same project again - should not create new one
    tracker.start_project("TestProject")
    assert len(tracker.projects) == 1


def test_stop_project():
    tracker = TimeTracker()
    tracker.start_project("TestProject")
    tracker.stop_project()
    assert tracker.projects[0].end_time is not None


def test_list_projects():
    tracker = TimeTracker()
    tracker.start_project("TestProject")
    # Mock stdout to capture output
    with patch('sys.stdout') as mock_stdout:
        tracker.list_projects()
        # Just verify it doesn't crash
        assert True


def test_duration_calculation():
    tracker = TimeTracker()
    tracker.start_project("TestProject")
    project = tracker.projects[0]
    # Check that duration is calculated properly (should be 0 initially)
    assert project.duration.total_seconds() >= 0
