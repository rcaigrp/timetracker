import pytest
import os
import json
import responses
import time
import sys
import tempfile

sys.path.insert(0, '/workspace/projects/TimeTracker')

from src.storage import StorageManager
from src.timer import TimerManager
from src.networking import JiraClient

class TestAppLaunch:
    def test_app_launch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = StorageManager(data_dir=tmpdir)
            assert sm.entries == []
            assert sm.settings == {}

class TestManualEntry:
    def test_manual_entry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = StorageManager(data_dir=tmpdir)
            entry = {"id": "1", "project": "Test", "date": "2023-01-01", "duration": "0:30"}
            sm.add_entry(entry)
            assert len(sm.entries) == 1
            assert sm.entries[0] == entry

class TestSettings:
    def test_settings_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm = StorageManager(data_dir=tmpdir)
            sm.save_settings("http://jira.com", "user", "pass")
            assert sm.settings == {"base_url": "http://jira.com", "username": "user", "api_key": "pass"}

class TestJiraIntegration:
    @responses.activate
    def test_jira_fetch(self):
        base_url = "http://jira.com"
        username = "user"
        api_key = "pass"
        
        responses.add(
            responses.GET,
            f"{base_url}/rest/api/project",
            json=[{"id": "1", "name": "TestProject"}],
            status=200
        )
        
        client = JiraClient(base_url, username, api_key)
        projects = client.get_projects()
        
        assert len(projects) == 1
        assert projects[0]["name"] == "TestProject"

class TestPersistence:
    def test_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sm1 = StorageManager(data_dir=tmpdir)
            sm1.add_entry({"id": "1"})
            sm1.save_entries()
            
            sm2 = StorageManager(data_dir=tmpdir)
            assert len(sm2.entries) == 1

class TestBackgroundSuspension:
    def test_background_suspension(self):
        tm = TimerManager()
        tm.start()
        time.sleep(1)
        tm.pause()
        elapsed_before = tm.get_elapsed()
        
        time.sleep(1)
        tm.resume()
        time.sleep(1)
        tm.pause()
        elapsed_after = tm.get_elapsed()
        
        assert elapsed_after >= elapsed_before + 0.9
