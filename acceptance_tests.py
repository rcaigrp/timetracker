import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app import app, get_db, Project, TimeEntry

class MockDB:
    def __init__(self):
        self.projects = []
        self.time_entries = []

    def add_project(self, project):
        self.projects.append(project)
        return project

    def get_projects(self):
        return self.projects

    def add_time_entry(self, entry):
        self.time_entries.append(entry)
        return entry

    def get_time_entries(self):
        return self.time_entries

    def close(self):
        pass

def mock_get_db():
    return MockDB()

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = mock_get_db
    client = TestClient(app)
    return client


test_project_data = {
    "name": "Test Project",
    "key": "TP"
}

test_time_entry_data = {
    "project_key": "TP",
    "task_name": "Test Task",
    "start_time": "2023-01-01T10:00:00Z",
    "end_time": "2023-01-01T11:00:00Z"
}

def test_criterion_1_dashboard_launches(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "dashboard" in response.json().get("message", "")

def test_criterion_2_timer_operations(client):
    # Test starting timer
    response = client.post("/time_entries/start", json={"project_key": "TP", "task_name": "Test Task"})
    assert response.status_code == 200
    
    # Test stopping timer
    response = client.post("/time_entries/stop", json={"project_key": "TP", "task_name": "Test Task"})
    assert response.status_code == 200
    
    # Test listing time entries
    response = client.get("/time_entries")
    assert response.status_code == 200
    

def test_criterion_3_settings_storage(client):
    # Test setting credentials
    response = client.post("/settings", json={
        "jira_url": "https://example.atlassian.net",
        "username": "test@example.com",
        "api_key": "secret-key"
    })
    assert response.status_code == 200
    

def test_criterion_4_jira_projects_fetch(client):
    # Test fetching projects from Jira API
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            "values": [
                {"key": "TP", "name": "Test Project"}
            ]
        }
        response = client.get("/jira/projects")
        assert response.status_code == 200
        

def test_criterion_5_local_storage_persistence(client):
    # Test creating project entry
    response = client.post("/projects", json=test_project_data)
    assert response.status_code == 200
    
    # Test retrieving projects
    response = client.get("/projects")
    assert response.status_code == 200
    assert len(response.json()) >= 1