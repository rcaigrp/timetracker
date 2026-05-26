import os
import pytest

PROJECT_DIR = "/workspace/projects/TimeTracker"

def test_criterion_1_dashboard_timer():
    assert os.path.exists(os.path.join(PROJECT_DIR, "DashboardView.swift"))
    assert os.path.exists(os.path.join(PROJECT_DIR, "TimerView.swift"))
    with open(os.path.join(PROJECT_DIR, "DashboardView.swift")) as f:
        assert "TimerView" in f.read()
        assert "List" in f.read()

def test_criterion_2_manual_entry_timer():
    assert os.path.exists(os.path.join(PROJECT_DIR, "TimerViewModel.swift"))
    with open(os.path.join(PROJECT_DIR, "TimerViewModel.swift")) as f:
        assert "startTimer" in f.read()
        assert "stopTimer" in f.read()
        assert "@Published" in f.read()

def test_criterion_3_settings_jira():
    assert os.path.exists(os.path.join(PROJECT_DIR, "SettingsView.swift"))
    with open(os.path.join(PROJECT_DIR, "SettingsView.swift")) as f:
        assert "jiraUrl" in f.read()
        assert "jiraApiKey" in f.read()

def test_criterion_4_jira_fetch():
    assert os.path.exists(os.path.join(PROJECT_DIR, "NetworkingManager.swift"))
    with open(os.path.join(PROJECT_DIR, "NetworkingManager.swift")) as f:
        assert "fetchProjects" in f.read()

def test_criterion_5_persistence():
    assert os.path.exists(os.path.join(PROJECT_DIR, "ProjectModel.swift"))
    assert os.path.exists(os.path.join(PROJECT_DIR, "TimeEntryModel.swift"))
    assert "@Model" in open(os.path.join(PROJECT_DIR, "ProjectModel.swift")).read()
    assert "@Model" in open(os.path.join(PROJECT_DIR, "TimeEntryModel.swift")).read()

def test_criterion_6_networking():
    with open(os.path.join(PROJECT_DIR, "NetworkingManager.swift")) as f:
        assert "URLSession" in f.read() or "async" in f.read()

def test_criterion_7_background():
    assert os.path.exists(os.path.join(PROJECT_DIR, "BackgroundManager.swift"))
    with open(os.path.join(PROJECT_DIR, "BackgroundManager.swift")) as f:
        assert "handleBackgroundSuspension" in f.read()
