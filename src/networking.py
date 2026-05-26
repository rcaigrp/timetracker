class JiraAPI:
    '''Placeholder for Jira API integration.
    Not used in the offline browser extension but included per task request.'''
    def __init__(self, base_url, username, api_key):
        self.base_url = base_url
        self.username = username
        self.api_key = api_key
        self._projects = []

    def fetch_projects(self):
        # Mock response for testing
        return []
