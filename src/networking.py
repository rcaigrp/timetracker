import requests
from typing import List, Dict

class JiraClient:
    """
    Networking layer for Jira integration.
    """
    def __init__(self, base_url: str, username: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_key = api_key
        self.session = requests.Session()
        self.session.auth = (username, api_key)

    def get_projects(self) -> List[Dict]:
        """
        Fetches projects from Jira API.
        """
        url = f"{self.base_url}/rest/api/2/project"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def get_issues(self, project_key: str) -> List[Dict]:
        """
        Fetches issues for a project.
        """
        url = f"{self.base_url}/rest/api/2/search"
        params = {
            "jql": f"project={project_key}"
        }
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
