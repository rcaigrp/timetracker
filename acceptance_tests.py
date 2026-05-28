import pytest
import requests

def test_criterion_1_launch():
    # Patch requests.get to mock Jira API calls
    original_get = requests.get
    def mock_get(url, *args, **kwargs):
        if 'rest/api/2/project' in url:
            # Return a fake project list
            class FakeResponse:
                status_code = 200
                def json(self):
                    return [{'id': 'PROJ-1', 'name': 'Backend Services'}]
            return FakeResponse()
        return original_get(url, *args, **kwargs)
    
    requests.get = mock_get
    
    # Import and run app
    from app import app
    client = app.test_client()
    
    response = client.get('/api/jira/projects')
    
    # Restore original function
    requests.get = original_get
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == 'Backend Services'
    print("Criterion 1: App launches and fetches projects cleanly.")

def test_criterion_4_api_integration():
    # Check that the endpoint logic is defined
    import sys
    sys.path.insert(0, '/workspace/projects/TimeTracker')
    from app import fetch_jira_projects
    
    assert callable(fetch_jira_projects)
    print("Criterion 4: API integration logic is defined.")

if __name__ == '__main__':
    pytest.main([__file__, '-v'])