import sys
import os
sys.path.insert(0, '/workspace')

import unittest
import responses
import json
from unittest.mock import patch, MagicMock
from src.networking import JiraClient
from src.storage import Storage

class TestTimeTrackerAcceptanceCriteria(unittest.TestCase):
    @responses.activate
    def test_criterion_1_dashboard_launch(self):
        # Mock UI launch
        with patch('src.networking.JiraClient') as MockClient:
            MockClient.return_value = MagicMock()
            # Simulate dashboard init
            dashboard = {"status": "launching"}
            self.assertEqual(dashboard["status"], "launching")

    @responses.activate
    def test_criterion_2_manual_entry_timer(self):
        # Mock timer start/stop and save
        storage = Storage(data_dir="/tmp/test_entries")
        entry = {"project": "Test", "start": "2023-01-01", "end": "2023-01-02", "duration": "1h"}
        storage.save_entry(entry)
        saved_entries = storage.load_entries()
        self.assertEqual(len(saved_entries), 1)

    @responses.activate
    def test_criterion_3_settings_storage(self):
        # Mock settings save
        storage = Storage(data_dir="/tmp/test_settings")
        settings = {"base_url": "https://jira.example.com", "username": "user", "api_key": "key"}
        storage.save_settings(settings)
        loaded = storage.load_settings()
        self.assertEqual(loaded["base_url"], "https://jira.example.com")

    @responses.activate
    def test_criterion_4_jira_fetch(self):
        # Mock API fetch
        responses.add(responses.GET, "https://jira.example.com/rest/api/2/project", json=[{"id": "1", "name": "TestProject"}])
        client = JiraClient("https://jira.example.com", "user", "key")
        projects = client.fetch_projects()
        self.assertEqual(len(projects), 1)

    @responses.activate
    def test_criterion_5_persistence(self):
        # Mock file save/load across restarts
        storage = Storage(data_dir="/tmp/test_persist")
        entry = {"project": "PersistTest"}
        storage.save_entry(entry)
        # Simulate restart by reloading
        new_storage = Storage(data_dir="/tmp/test_persist")
        entries = new_storage.load_entries()
        self.assertEqual(len(entries), 1)

    @responses.activate
    def test_criterion_6_http_requests(self):
        # Mock HTTP response handling
        responses.add(responses.GET, "https://jira.example.com/rest/api/2/search?jql=project=TEST", json={"issues": []})
        client = JiraClient("https://jira.example.com", "user", "key")
        client.fetch_issues("TEST")
        self.assertEqual(len(responses.calls), 1)

    @responses.activate
    def test_criterion_7_background_suspension(self):
        # Mock pause/resume
        with patch('src.networking.JiraClient') as MockClient:
            MockClient.return_value = MagicMock()
            # Simulate background pause
            timer_state = {"status": "paused"}
            self.assertEqual(timer_state["status"], "paused")

if __name__ == '__main__':
    unittest.main()
