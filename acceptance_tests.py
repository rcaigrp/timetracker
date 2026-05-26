import pytest
import responses
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.viewmodel import ViewModel
from src.storage import Storage
from src.networking import JiraClient

class TestAC1_TimerDashboard:
    def test_timer_starts_and_shows_elapsed(self):
        vm = ViewModel()
        vm.start_timer()
        time.sleep(0.1)
        elapsed = vm.get_elapsed_time()
        assert elapsed > 0

class TestAC2_ManualEntry:
    def test_manual_entry_saves(self):
        vm = ViewModel()
        vm.start_timer()
        vm.stop_timer()
        entries = vm.storage.get_entries()
        assert len(entries) > 0

class TestAC3_Settings:
    def test_settings_stored(self):
        vm = ViewModel()
        vm.configure_jira('http://example.com', 'user', 'pass')
        settings = vm.storage.data.get('settings')
        assert settings['base_url'] == 'http://example.com'

class TestAC4_JiraFetch:
    @responses.activate
    def test_fetch_projects(self):
        vm = ViewModel()
        vm.configure_jira('http://example.com', 'user', 'pass')
        responses.add(responses.GET, 'http://example.com/rest/api/latest/project', json=[{'id': '1'}])
        projects = vm.get_jira_projects()
        assert len(projects) == 1

class TestAC5_Persistence:
    def test_persistence(self):
        vm1 = ViewModel()
        vm1.start_timer()
        vm1.stop_timer()
        vm2 = ViewModel()
        entries = vm2.storage.get_entries()
        assert len(entries) > 0

class TestAC6_Networking:
    @responses.activate
    def test_networking_handles_response(self):
        vm = ViewModel()
        vm.configure_jira('http://example.com', 'user', 'pass')
        responses.add(responses.GET, 'http://example.com/rest/api/latest/project', json=[{'id': '1'}])
        projects = vm.get_jira_projects()
        assert isinstance(projects, list)