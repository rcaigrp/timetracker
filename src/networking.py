import requests

class JiraClient:
    def __init__(self):
        self.base_url = None
        self.username = None
        self.api_key = None

    def set_credentials(self, base_url, username, api_key):
        self.base_url = base_url
        self.username = username
        self.api_key = api_key

    def fetch_projects(self):
        if not self.base_url or not self.username or not self.api_key:
            raise ValueError("Credentials not configured")
        url = f"{self.base_url}/rest/api/latest/project"
        response = requests.get(url, auth=(self.username, self.api_key))
        response.raise_for_status()
        return response.json()