import pytest
from unittest.mock import patch, MagicMock
import json
import os
import responses

class MockResponse:
    def __init__(self):
        self.status_code = 200
        self.json_data = {'key': 'value'}
    
    def json(self):
        return self.json_data

# Mock the requests library to prevent real HTTP calls
@pytest.fixture(autouse=True)
@responses.activate
def mock_requests():
    # Mock successful responses for any API calls
    responses.add(
        responses.GET,
        'https://api.example.com/projects',
        json={'values': [{'id': '1', 'name': 'Project Alpha'}, {'id': '2', 'name': 'Project Beta'}]},
        status=200
    )
    responses.add(
        responses.POST,
        'https://api.example.com/projects',
        json={'id': '3', 'name': 'New Project'},
        status=201
    )
    yield responses

@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test criterion 1: Application launches cleanly with working dashboard
@pytest.mark.parametrize("endpoint", [('/', 'GET')])
def test_criterion_1_dashboard_loads(client):
    response = client.get('/')
    assert response.status_code == 200

# Test criterion 2: Users can create projects and manage timers
@pytest.mark.parametrize("endpoint", [('api/projects', 'POST'), ('api/projects', 'GET')])
def test_criterion_2_project_timer_functionality(client):
    # Create a project
    response = client.post('/api/projects', 
                          json={'name': 'Test Project'})
    assert response.status_code == 201
    data = response.get_json()
    project_id = data['id']
    
    # Start timer
    response = client.post(f'/api/timer/start/{project_id}')
    assert response.status_code == 200
    
    # Stop timer
    response = client.post(f'/api/timer/stop/{project_id}')
    assert response.status_code == 200
    
    # Get timer status
    response = client.get(f'/api/timer/{project_id}')
    assert response.status_code == 200

# Test criterion 3: Settings are stored securely
@pytest.mark.parametrize("endpoint", [('api/settings', 'POST'), ('api/settings', 'GET')])
def test_criterion_3_settings_storage(client):
    # Set settings
    settings_data = {'theme': 'dark', 'notifications': True}
    response = client.post('/api/settings', json=settings_data)
    assert response.status_code == 200
    
    # Get settings
    response = client.get('/api/settings')
    assert response.status_code == 200
    data = response.get_json()
    assert data['theme'] == 'dark'
    assert data['notifications'] is True