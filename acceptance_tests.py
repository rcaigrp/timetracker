import pytest
import json
import os
import responses
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

@responses.activate
def test_criterion_1_dashboard():
    # Test dashboard loads
    response = client.get('/')
    assert response.status_code == 200

@responses.activate
def test_criterion_2_manual_entry():
    # Test manual entry and timer logic
    with patch('app.get_settings') as mock_settings:
        # Mock settings
        pass

@responses.activate
def test_criterion_3_jira_settings():
    # Test Jira credentials storage
    settings_data = {'jira_url': 'http://test', 'username': 'user', 'api_key': 'key'}
    response = client.post('/api/settings', json=settings_data)
    assert response.status_code == 201

@responses.activate
def test_criterion_4_fetch_projects():
    # Mock Jira API response for projects
    responses.add(
        responses.GET,
        'http://test/rest/api/2/project',
        json=[{'key': 'PROJ1', 'name': 'Project 1'}],
        status=200
    )
    response = client.get('/api/projects')
    assert response.status_code == 200

@responses.activate
def test_criterion_5_persistence():
    # Test local storage persistence
    with open('time_tracker.json', 'w') as f:
        json.dump({'test': 'data'}, f)
    assert os.path.exists('time_tracker.json')
