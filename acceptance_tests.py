import pytest
import requests
import time
from unittest.mock import patch

class TestTimeTracker:
    def test_criterion_1_start_timer(self):
        response = requests.post('http://localhost:5000/start')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'started'

    def test_criterion_2_stop_timer(self):
        # Start the timer first
        requests.post('http://localhost:5000/start')
        
        # Stop the timer
        response = requests.post('http://localhost:5000/stop')
        assert response.status_code == 200
        data = response.json()
        assert data['status'] == 'stopped'

    def test_criterion_3_get_time(self):
        # Start and stop timer to ensure we have some time recorded
        requests.post('http://localhost:5000/start')
        time.sleep(0.1)  # Small delay to ensure some time passes
        requests.post('http://localhost:5000/stop')
        
        response = requests.get('http://localhost:5000/time')
        assert response.status_code == 200
        data = response.json()
        assert 'total_seconds' in data
        assert 'formatted_time' in data
        assert isinstance(data['total_seconds'], (int, float))
        assert len(data['formatted_time']) == 8  # HH:MM:SS format

    def test_criterion_4_timer_logic(self):
        # Test timer logic with multiple start/stop cycles
        response = requests.post('http://localhost:5000/start')
        assert response.status_code == 200
        
        time.sleep(0.1)
        
        response = requests.post('http://localhost:5000/stop')
        assert response.status_code == 200
        
        # Get time after stopping
        response = requests.get('http://localhost:5000/time')
        data = response.json()
        assert data['total_seconds'] > 0
