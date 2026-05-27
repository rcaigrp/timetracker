import pytest
from app import app
from unittest.mock import patch
import requests

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

class TestDashboard:
    def test_criterion_1_launch_dashboard(self, client):
        """Test that the application launches cleanly with a dashboard."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Status' in response.data

class TestManualEntry:
    def test_criterion_2_manual_entry(self, client):
        """Test users can create time entries."""
        payload = {"project": "DS", "duration": "1h", "date": "2023-01-01"}
        response = client.post('/api/times', json=payload)
        assert response.status_code == 200
        assert b'success' in response.data

class TestPersistence:
    def test_criterion_5_persist(self, client):
        """Test local storage persists logs between sessions."""
        # Add entry
        payload = {"project": "API", "duration": "2h", "date": "2023-01-02"}
        client.post('/api/times', json=payload)
        # Fetch entry
        response = client.get('/api/times')
        assert response.status_code == 200
        assert len(response.json) > 0

class TestJiraIntegration:
    def test_criterion_4_fetch_jira_projects(self, client):
        """Test that app fetches projects from Jira API automatically."""
        # Mock the requests.get call inside the app logic
        mock_response = [
            {"id": "PROJ-1", "name": "Design System", "key": "DS"},
            {"id": "PROJ-2", "name": "Backend API", "key": "API"}
        ]
        
        with patch('requests.get') as mock_get:
            # Configure the mock to return our mock response
            mock_get.return_value.json = lambda: mock_response
            mock_get.return_value.status_code = 200
            
            # Call the endpoint
            response = client.get('/api/projects')
            
            # Verify the result
            assert response.status_code == 200
            assert len(response.json) == 2
            
            # Verify the app made the API call
            mock_get.assert_called_once()

class TestSettings:
    def test_criterion_3_settings(self, client):
        """Test that settings screen accepts credentials."""
        payload = {"url": "https://jira.example.com", "api_key": "test123"}
        response = client.post('/api/settings', json=payload)
        assert response.status_code == 200
        assert b'saved' in response.data
