import pytest
from fastapi.testclient import TestClient
from main import app
import sqlite3
import os

client = TestClient(app)

def test_criterion_1_api_starts_cleanly():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TimeTracker API is running"}

def test_criterion_2_project_crud_operations():
    # Create a project
    project_data = {"name": "Test Project", "jira_id": "TEST-1"}
    response = client.post("/projects", json=project_data)
    assert response.status_code == 200
    created_project = response.json()
    assert created_project["name"] == "Test Project"
    
    # Read projects
    response = client.get("/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) >= 1
    
    # Delete the project
    response = client.delete(f"/projects/{created_project['id']}")
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get("/projects")
    projects_after = response.json()
    assert len(projects_after) == len(projects) - 1

def test_criterion_3_time_entry_operations():
    # Create a project first
    project_data = {"name": "Test Project", "jira_id": "TEST-1"}
    response = client.post("/projects", json=project_data)
    project = response.json()
    
    # Create time entry
    entry_data = {
        "project_id": project["id"],
        "start_time": "2023-01-01T10:00:00Z",
        "end_time": "2023-01-01T11:00:00Z",
        "duration": 3600
    }
    response = client.post("/time_entries", json=entry_data)
    assert response.status_code == 200
    created_entry = response.json()
    
    # Read time entries
    response = client.get("/time_entries")
    assert response.status_code == 200
    entries = response.json()
    assert len(entries) >= 1
    
    # Update entry
    updated_data = {
        "project_id": project["id"],
        "start_time": "2023-01-01T10:00:00Z",
        "end_time": "2023-01-01T12:00:00Z",
        "duration": 7200
    }
    response = client.put(f"/time_entries/{created_entry['id']}", json=updated_data)
    assert response.status_code == 200
    
    # Delete entry
    response = client.delete(f"/time_entries/{created_entry['id']}")
    assert response.status_code == 200
    
    # Verify deletion
    response = client.get("/time_entries")
    entries_after = response.json()
    assert len(entries_after) == len(entries) - 1
    
    # Clean up project
    client.delete(f"/projects/{project['id']}")

def test_criterion_4_jira_integration_requires_credentials():
    # Test that Jira API requires credentials
    response = client.get("/jira/projects")
    assert response.status_code == 400
    
    # Set required environment variables
    os.environ["JIRA_BASE_URL"] = "https://example.atlassian.net"
    os.environ["JIRA_USERNAME"] = "test@example.com"
    os.environ["JIRA_API_TOKEN"] = "test-token"
    
    # Now it should work (mocked)
    response = client.get("/jira/projects")
    assert response.status_code == 200
    
    # Clean up environment variables
    del os.environ["JIRA_BASE_URL"]
    del os.environ["JIRA_USERNAME"]
    del os.environ["JIRA_API_TOKEN"]

def test_criterion_5_local_storage_persists_logs():
    # Test database persistence
    conn = sqlite3.connect("timetracker.db")
    cursor = conn.cursor()
    
    # Create a project
    cursor.execute("INSERT INTO projects (name, jira_id) VALUES (?, ?)", ("Persistence Test", "PERSIST-1"))
    conn.commit()
    project_id = cursor.lastrowid
    
    # Create a time entry
    cursor.execute("INSERT INTO time_entries (project_id, start_time, end_time, duration) VALUES (?, ?, ?, ?)", 
                   (project_id, "2023-01-01T10:00:00Z", "2023-01-01T11:00:00Z", 3600))
    conn.commit()
    entry_id = cursor.lastrowid
    
    # Verify data exists
    cursor.execute("SELECT * FROM projects WHERE id=?", (project_id,))
    project_row = cursor.fetchone()
    assert project_row is not None
    
    cursor.execute("SELECT * FROM time_entries WHERE id=?", (entry_id,))
    entry_row = cursor.fetchone()
    assert entry_row is not None
    
    # Clean up
    cursor.execute("DELETE FROM time_entries WHERE id=?", (entry_id,))
    cursor.execute("DELETE FROM projects WHERE id=?", (project_id,))
    conn.commit()
    conn.close()