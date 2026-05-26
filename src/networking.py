import requests

class JiraClient:
    def __init__(self, base_url, username, api_key):
        self.base_url = base_url
        self.username = username
        self.api_key = api_key
        self.session = requests.Session()
        self.session.auth = (self.username, self.api_key)

    def get_projects(self):
        url = f"{self.base_url}/rest/api/project"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
