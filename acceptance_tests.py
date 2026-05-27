import pytest
from fastapi.testclient import TestClient
from main import app

class TestSettings:
    jira_base_url = "https://example.atlassian.net"
    jira_username = "test@example.com"
    jira_api_token = "test-token-12345"

test_client = TestClient(app)

def test_criterion_1_api_running():
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TimeTracker API is running"}

def test_criterion_2_create_and_get_projects():
    # Create a project
    project_data = {"name": "Test Project"}
    response = test_client.post("/projects", json=project_data)
    assert response.status_code == 200
    created_project = response.json()
    assert created_project["name"] == "Test Project"
    
    # Get all projects
    response = test_client.get("/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 1
    assert projects[0]["name"] == "Test Project"

def test_criterion_3_create_and_get_time_entries():
    # Create a time entry
    entry_data = {"project_id": 1, "start_time": "2023-01-01T10:00:00Z", "end_time": "2023-01-01T11:00:00Z"}
    response = test_client.post("/time_entries", json=entry_data)
    assert response.status_code == 200
    created_entry = response.json()
    assert created_entry["project_id"] == 1
    
    # Get all time entries
    response = test_client.get("/time_entries")
    assert response.status_code == 200
    entries = response.json()
    assert len(entries) == 1
    assert entries[0]["project_id"] == 1

def test_criterion_4_settings_storage_and_retrieval():
    # Set settings
    settings_data = {
        "jira_base_url": TestSettings.jira_base_url,
        "jira_username": TestSettings.jira_username,
        "jira_api_token": TestSettings.jira_api_token
    }
    response = test_client.post("/settings", json=settings_data)
    assert response.status_code == 200
    
    # Get settings
    response = test_client.get("/settings")
    assert response.status_code == 200
    returned_settings = response.json()
    assert returned_settings["jira_base_url"] == TestSettings.jira_base_url

def test_criterion_5_jira_integration():
    # First set up settings
    settings_data = {
        "jira_base_url": TestSettings.jira_base_url,
        "jira_username": TestSettings.jira_username,
        "jira_api_token": TestSettings.jira_api_token
    }
    test_client.post("/settings", json=settings_data)
    
    # Fetch Jira projects (should return mocked data)
    response = test_client.get("/jira/projects")
    assert response.status_code == 200
    projects = response.json()
    assert "projects" in projects
    assert len(projects["projects"]) >= 1