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
        if not self.base_url:
            return []
        url = f"{self.base_url}/rest/api/project"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(url, headers=headers)
        return response.json()
