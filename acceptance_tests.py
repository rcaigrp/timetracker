import pytest
import responses
import os
from app import app

# Mock the environment or path setup for testing
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup():
    yield
    if os.path.exists("settings.json"):
        os.remove("settings.json")

# Criterion 1: App runs on iOS (simulated by API availability)
def test_criterion_1_api_responds(client):
    # Mock Jira response
    responses.add(
        responses.GET,
        "https://jira.example.com/rest/api/3/search",
        json={"issues": [{"id": "1"}, {"id": "2"}]},
        status=200
    )
    
    response = client.get('/api/projects')
    assert response.status_code == 200
    assert 'issues' in response.json

# Criterion 2: Jira API integration handles auth
@responses.activate
def test_criterion_2_auth_required():
    # Setup settings
    settings = {"jira_url": "https://jira.example.com", "api_key": "test_token"}
    with open("settings.json", "w") as f:
        json.dump(settings, f)

    # Mock Jira response
    responses.add(
        responses.GET,
        "https://jira.example.com/rest/api/3/search",
        json={"issues": []},
        status=200
    )

    # Call API
    client = app.test_client()
    response = client.get('/api/projects')

    # Verify request contains Authorization header
    req_headers = responses.calls[0].request.headers
    assert "Authorization" in req_headers
    assert req_headers["Authorization"] == f"Basic {settings['api_key']}"

# Criterion 3: Local storage persists data
def test_criterion_3_settings_save(client):
    # Mock Jira response to force a network call (invalid for this test, but checks persistence)
    # Actually, let's just test the file write directly
    payload = {
        "jira_url": "https://jira.example.com",
        "username": "testuser",
        "api_key": "secret123"
    }
    
    response = client.post('/api/settings', json=payload)
    assert response.status_code == 200
    
    with open("settings.json", "r") as f:
        loaded = json.load(f)
        assert loaded['api_key'] == 'secret123'
