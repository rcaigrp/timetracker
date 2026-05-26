import requests
from typing import List, Dict

class JiraClient:
    def __init__(self, base_url: str, username: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_key = api_key

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Basic {self.username}:{self.api_key}",
            "Content-Type": "application/json"
        }

    def fetch_projects(self) -> List[Dict]:
        url = f"{self.base_url}/rest/api/2/project"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, project_key: str) -> List[Dict]:
        url = f"{self.base_url}/rest/api/2/search?jql=project={project_key}"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json().get("issues", [])
