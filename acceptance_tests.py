import json
from unittest.mock import patch, MagicMock
import responses
import pytest
from app import app

class TestTimeTracker:
    def setup_method(self):
        self.app = app.test_client()
        # Clear any existing data file
        with open('timer_data.json', 'w') as f:
            json.dump({'projects': [], 'active_project': None}, f)

    @responses.activate
    def test_criterion_1_create_project(self):
        responses.add(responses.POST, 'http://localhost/api/projects',
                      json={'id': 0, 'name': 'Test Project', 'start_time': None, 'end_time': None, 'duration': 0, 'is_active': False},
                      status=200)
        
        response = self.app.post('/api/projects',
                                data=json.dumps({'name': 'Test Project'}),
                                content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Test Project'

    @responses.activate
    def test_criterion_2_start_project(self):
        # First create a project
        self.app.post('/api/projects',
                     data=json.dumps({'name': 'Test Project'}),
                     content_type='application/json')
        
        # Then start it
        responses.add(responses.POST, 'http://localhost/api/projects/0/start',
                      json={'id': 0, 'name': 'Test Project', 'start_time': '2023-01-01T00:00:00', 'end_time': None, 'duration': 0, 'is_active': True},
                      status=200)
        
        response = self.app.post('/api/projects/0/start')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['is_active'] is True

    @responses.activate
    def test_criterion_3_stop_project(self):
        # Create and start a project first
        self.app.post('/api/projects',
                     data=json.dumps({'name': 'Test Project'}),
                     content_type='application/json')
        self.app.post('/api/projects/0/start')
        
        # Then stop it
        responses.add(responses.POST, 'http://localhost/api/projects/0/stop',
                      json={'id': 0, 'name': 'Test Project', 'start_time': '2023-01-01T00:00:00', 'end_time': '2023-01-01T00:01:00', 'duration': 60, 'is_active': False},
                      status=200)
        
        response = self.app.post('/api/projects/0/stop')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['is_active'] is False