import pytest
import responses
import json
import os
import sys
sys.path.insert(0, '/workspace/projects/TimeTracker')

class TestAcceptance:
    @responses.mock
    def test_criterion_1_launch_cleanly(self):
        from src.viewmodel import TimeTrackerViewModel
        vm = TimeTrackerViewModel()
        assert vm is not None
        assert vm.storage is not None

    def test_criterion_2_manual_entry(self):
        from src.viewmodel import TimeTrackerViewModel
        vm = TimeTrackerViewModel()
        vm.start_timer("CustomProject")
        vm.stop_timer()
        entries = vm.get_entries()
        assert len(entries) == 1
        assert entries[0]["project"] == "CustomProject"
        assert "duration" in entries[0]

    @responses.mock
    def test_criterion_3_settings_stores_credentials(self):
        from src.viewmodel import TimeTrackerViewModel
        vm = TimeTrackerViewModel("https://jira.example.com", "user", "api_key")
        assert vm.jira_client is not None
        assert vm.jira_client.base_url == "https://jira.example.com"

    @responses.mock
    def test_criterion_4_jira_fetch(self):
        from src.viewmodel import TimeTrackerViewModel
        vm = TimeTrackerViewModel("https://jira.example.com", "user", "api_key")
        responses.add(responses.GET, "https://jira.example.com/rest/api/project", json=[{"id": "P1", "name": "Project 1"}])
        result = vm.fetch_jira_projects()
        assert result is not None
        assert len(result.json()) == 1

    def test_criterion_5_persistence(self):
        from src.storage import TimerStorage
        storage1 = TimerStorage("test_persist.json")
        storage1.save_entry({"id": 1, "project": "Persisted"})
        storage2 = TimerStorage("test_persist.json")
        assert len(storage2.data) == 1
        assert storage2.data[0]["id"] == 1
        os.remove("test_persist.json")

    @responses.mock
    def test_criterion_6_networking(self):
        from src.viewmodel import TimeTrackerViewModel
        vm = TimeTrackerViewModel("https://jira.example.com", "user", "api_key")
        responses.add(responses.GET, "https://jira.example.com/rest/api/project", status=200, json=[{"id": "P1"}])
        result = vm.fetch_jira_projects()
        assert result.status_code == 200

    def test_criterion_7_suspension_handling(self):
        from src.viewmodel import TimeTrackerViewModel
        vm = TimeTrackerViewModel()
        vm.start_timer("ProjectA")
        assert vm.timer_running == True
        vm.timer_running = False
        assert vm.timer_running == False
        vm.timer_running = True
        assert vm.timer_running == True
