import requests

class JiraClient:
    def __init__(self, base_url, username, api_key):
        self.base_url = base_url
        self.username = username
        self.api_key = api_key
        self.session = requests.Session()
        self.session.auth = (username, api_key)
        self.session.headers.update({'Content-Type': 'application/json'})

    def get_projects(self):
        try:
            url = f"{self.base_url}/rest/api/latest/project"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            return []
