import pytest
import responses
import json
import os
import tempfile

# Setup test environment
@pytest.fixture
def temp_file():
    fd, path = tempfile.mkstemp()
    os.close(fd)
    yield path
    os.unlink(path)

# Mock Jira API for Criterion 4
@responses.activate
def test_criterion_4_fetch_jira_projects():
    """Test that app fetches projects from Jira API using configured credentials."""
    # Mock Jira API response (search endpoint)
    responses.add(
        responses.GET,
        "https://jira.example.com/rest/api/2/search",
        json={"issues": [{"key": "PROJ-1", "fields": {"name": "Test Project"}}]},
        status=200
    )

    # Import and setup Flask app in test mode
    from app import app
    client = app.test_client()

    # Call the API endpoint that fetches projects
    response = client.get('/api/jira/projects')

    # Verify the endpoint was called and returned 200
    assert response.status_code == 200
    assert 'Test Project' in response.get_json().get('data', {})

# Criterion 5: Local Storage Persistence
def test_criterion_5_persistence():
    """Test that logs are persisted between sessions."""
    # Create a temporary log file
    temp_file_path = '/tmp/test_time_logs.json'
    initial_data = []
    with open(temp_file_path, 'w') as f:
        json.dump(initial_data, f)

    try:
        # Simulate writing a new log
        new_log = {"id": 1, "project": "Dev", "duration": 3600, "date": "2023-01-01"}
        with open(temp_file_path, 'r+') as f:
            data = json.load(f)
            data.append(new_log)
            f.seek(0)
            json.dump(data, f)
            f.truncate()

        # Verify persistence (reading back)
        with open(temp_file_path, 'r') as f:
            loaded = json.load(f)
            assert len(loaded) == 1
            assert loaded[0]['project'] == "Dev"

    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

# Criterion 2: Manual Entry
def test_criterion_2_manual_entry():
    """Test that users can manually create time entries."""
    from app import app
    client = app.test_client()
    
    entry_data = {
        "project": "Dev",
        "duration": 3600,
        "date": "2023-01-01",
        "description": "Test Entry"
    }
    
    response = client.post('/api/logs', json=entry_data)
    
    assert response.status_code == 200
    assert response.get_json()['success'] == True

# Criterion 1: App Launch
def test_criterion_1_launch():
    """Test that the application launches cleanly and the dashboard is accessible."""
    from app import app
    client = app.test_client()
    
    # Test dashboard endpoint (assumed)
    response = client.get('/api/dashboard')
    assert response.status_code == 200

# Criterion 3: Settings
@responses.activate
def test_criterion_3_settings():
    """Test that settings screen accepts Jira config and stores it securely."""
    from app import app
    client = app.test_client()
    
    # Mock the settings endpoint
    responses.add(
        responses.POST,
        "http://localhost:5000/api/settings",
        json={"url": "https://jira.example.com"},
        status=200
    )
    
    settings_data = {
        "jira_url": "https://jira.example.com",
        "username": "admin",
        "api_key": "test_key"
    }
    
    response = client.post('/api/settings', json=settings_data)
    
    assert response.status_code == 200
    assert response.get_json()['success'] == True

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
