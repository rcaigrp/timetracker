import requests
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin

class JiraClient:
    def __init__(self, base_url: str, username: str, api_token: str):
        self.base_url = base_url.rstrip('/')
        self.username = username
        self.api_token = api_token
        self.session = requests.Session()
        self.session.auth = (username, api_token)
        self.session.headers.update({'Content-Type': 'application/json'})

    def fetch_projects(self) -> List[Dict]:
        url = urljoin(self.base_url, '/rest/api/3/project')
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, project_key: str) -> List[Dict]:
        url = urljoin(self.base_url, '/rest/api/3/search')
        payload = {
            "jql": f"project = '{project_key}'",
            "fields": ["summary", "status", "timeSpent"]
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("issues", [])
