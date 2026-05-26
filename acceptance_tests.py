import pytest
import json
import os
import time
import responses
import sys

sys.path.insert(0, '/workspace/projects/TimeTracker/src')

from app import TimerManager, SettingsManager
from networking import JiraClient


@pytest.fixture
def timer_manager(tmp_path):
    path = str(tmp_path / "timer.json")
    return TimerManager(storage_path=path)

@pytest.fixture
def settings_manager(tmp_path):
    path = str(tmp_path / "settings.json")
    return SettingsManager(settings_path=path)

@pytest.fixture
def jira_client():
    return JiraClient("https://test.atlassian.net", "user", "key")


def test_criterion_1_timer_launches_and_tracks(timer_manager):
    # Timer launches cleanly and tracks time
    assert not timer_manager.is_running
    timer_manager.start("DevProject")
    assert timer_manager.is_running
    assert timer_manager.get_elapsed() > 0


def test_criterion_2_manual_entry_creation(timer_manager):
    # Manual entry with name, start/stop, and elapsed time
    timer_manager.start("TestProject")
    time.sleep(0.1)
    timer_manager.stop()
    entries = timer_manager.get_entries()
    assert len(entries) == 1
    assert entries[0]["project"] == "TestProject"
    assert entries[0]["duration"] > 0


def test_criterion_3_settings_stores_credentials_securely(settings_manager):
    # Settings accepts and stores credentials securely
    settings_manager.save_settings("https://jira.local", "admin", "secret123")
    settings = settings_manager.get_settings()
    assert "api_key_hash" in settings
    assert settings["base_url"] == "https://jira.local"
    assert settings["username"] == "admin"


def test_criterion_4_jira_fetches_projects_without_crashing(jira_client):
    # Fetches projects/issues without crashing
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://test.atlassian.net/rest/api/latest/project",
            json=[{"id": "1", "name": "TestProject"}],
            status=200
        )
        projects = jira_client.get_projects()
        assert len(projects) == 1
        assert projects[0]["name"] == "TestProject"


def test_criterion_5_data_persists_across_relaunchs(timer_manager):
    # Data persists across app relaunches (simulated by reloading JSON)
    timer_manager.start("PersistTest")
    time.sleep(0.1)
    timer_manager.stop()
    entries_before = timer_manager.get_entries()
    # Simulate reload
    new_manager = TimerManager(storage_path=timer_manager.storage_path)
    assert len(new_manager.get_entries()) == len(entries_before)


def test_criterion_6_networking_handles_requests(jira_client):
    # Handles HTTP requests and returns structured data
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://test.atlassian.net/rest/api/latest/search",
            json={"issues": [{"id": "123"}]},
            status=200
        )
        issues = jira_client.get_issues("TEST")
        assert len(issues) == 1
        assert issues[0]["id"] == "123"


def test_criterion_7_background_suspension_handling(timer_manager):
    # Gracefully handles suspension by pausing and resuming
    timer_manager.start("SuspensionTest")
    time.sleep(0.1)
    timer_manager.pause()
    assert not timer_manager.is_running
    timer_manager.resume()
    assert timer_manager.is_running
    assert timer_manager.get_elapsed() > 0
