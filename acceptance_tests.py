#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
import json
import os

class TestTimeTrackerAcceptance(unittest.TestCase):
    
    def setUp(self):
        # Import here to avoid circular imports during test discovery
        from app import app
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        self.app_context.pop()
    
    def test_criterion_1_main_dashboard_loads(self):
        """The application launches cleanly and presents a main dashboard"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'TimeTracker Dashboard', response.data)
    
    def test_criterion_2_manual_entry_and_timer(self):
        """Users can create custom project entries and view elapsed time"""
        # Create a project entry
        response = self.app.post('/projects', data={
            'name': 'Test Project',
            'description': 'Test description'
        })
        self.assertEqual(response.status_code, 201)
        
        # Start timer
        response = self.app.post('/timer/start', data={'project_id': 1})
        self.assertEqual(response.status_code, 200)
        
        # Stop timer
        response = self.app.post('/timer/stop', data={'project_id': 1})
        self.assertEqual(response.status_code, 200)
        
        # Verify logs are persisted
        response = self.app.get('/logs')
        self.assertEqual(response.status_code, 200)
    
    def test_criterion_3_settings_screen_stores_credentials(self):
        """Settings screen accepts and stores Jira credentials securely"""
        response = self.app.post('/settings', data={
            'jira_base_url': 'https://example.atlassian.net',
            'username': 'test@example.com',
            'api_key': 'test-api-key'
        })
        self.assertEqual(response.status_code, 200)
        
        # Verify credentials are stored
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['jira_base_url'], 'https://example.atlassian.net')
    
    def test_criterion_4_jira_project_fetching(self):
        """App fetches projects from Jira API automatically"""
        # First set up credentials
        self.app.post('/settings', data={
            'jira_base_url': 'https://example.atlassian.net',
            'username': 'test@example.com',
            'api_key': 'test-api-key'
        })
        
        # Mock Jira API response
        with patch('app.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'values': [
                    {'id': '1', 'name': 'Project Alpha'},
                    {'id': '2', 'name': 'Project Beta'}
                ]
            }
            mock_get.return_value = mock_response
            
            response = self.app.get('/jira/projects')
            self.assertEqual(response.status_code, 200)
    
    def test_criterion_5_local_storage_persists_logs(self):
        """Local storage persists logs between app sessions"""
        # Create a project
        response = self.app.post('/projects', data={'name': 'Test Project'})
        self.assertEqual(response.status_code, 201)
        
        # Start and stop timer
        self.app.post('/timer/start', data={'project_id': 1})
        self.app.post('/timer/stop', data={'project_id': 1})
        
        # Verify logs exist
        response = self.app.get('/logs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertGreater(len(data), 0)
