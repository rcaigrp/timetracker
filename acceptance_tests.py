import pytest
import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

sys.path.append('/workspace/projects/TimeTracker/src')

import storage
import networking

class TestStorage:
    def setup_method(self):
        self.storage = storage.StorageManager(db_path="test_storage.json")
    
    def teardown_method(self):
        if os.path.exists("test_storage.json"):
            os.remove("test_storage.json")

    def test_save_and_load(self):
        entry = {"id": 1, "project": "Test"}
        self.storage.add_entry(entry)
        assert entry in self.storage.get_entries()

    def test_clear_entries(self):
        self.storage.add_entry({"id": 1})
        self.storage.clear_entries()
        assert self.storage.get_entries() == []

    def test_settings(self):
        self.storage.set_setting("key", "value")
        assert self.storage.get_setting("key") == "value"

class TestNetworking:
    @patch('networking.requests.Session')
    def test_get_projects(self, mock_session_class):
        mock_instance = MagicMock()
        mock_session_class.return_value = mock_instance
        mock_instance.get.return_value.json.return_value = [{"id": "1"}]
        
        client = networking.JiraClient("http://test.com", "user", "key")
        projects = client.get_projects()
        assert projects == [{"id": "1"}]

    @patch('networking.requests.Session')
    def test_get_issues(self, mock_session_class):
        mock_instance = MagicMock()
        mock_session_class.return_value = mock_instance
        mock_instance.get.return_value.json.return_value = {"issues": []}
        
        client = networking.JiraClient("http://test.com", "user", "key")
        issues = client.get_issues("PROJ")
        assert issues == {"issues": []}
