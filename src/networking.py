import requests

class JiraClient:
    def __init__(self, base_url, username, api_key):
        self.base_url = base_url
        self.username = username
        self.api_key = api_key

    def fetch_projects(self):
        """Fetches projects from Jira API using configured credentials."""
        url = f"{self.base_url}/rest/api/2/project"
        response = requests.get(url, auth=(self.username, self.api_key))
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, project_key):
        """Fetches issues for a specific project."""
        url = f"{self.base_url}/rest/api/2/search"
        params = {"jql": f"project = '{project_key}'"}
        response = requests.get(url, auth=(self.username, self.api_key), params=params)
        response.raise_for_status()
        return response.json()
