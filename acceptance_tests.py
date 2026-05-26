import unittest
import responses
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from settings import SecureStorage
from networking import JiraClient

class TestSecureStorage(unittest.TestCase):
    def setUp(self):
        SecureStorage._credentials = None

    def test_save_credentials(self):
        SecureStorage.save_credentials("https://jira.test.com", "user", "pass")
        creds = SecureStorage.get_credentials()
        self.assertEqual(creds["base_url"], "https://jira.test.com")
        self.assertEqual(creds["username"], "user")
        self.assertEqual(creds["api_key"], "pass")

    def test_has_credentials(self):
        self.assertFalse(SecureStorage.has_credentials())
        SecureStorage.save_credentials("https://jira.test.com", "user", "pass")
        self.assertTrue(SecureStorage.has_credentials())

class TestJiraClient(unittest.TestCase):
    @responses.activate
    def test_fetch_projects(self):
        base_url = "https://jira.test.com"
        client = JiraClient(base_url, "user", "pass")
        mock_projects = [{"id": "1", "key": "PROJ", "name": "Project"}]
        responses.add(
            responses.GET,
            f"{base_url}/rest/api/2/project",
            json=mock_projects,
            status=200
        )
        result = client.fetch_projects()
        self.assertEqual(result, mock_projects)

    @responses.activate
    def test_fetch_issues(self):
        base_url = "https://jira.test.com"
        client = JiraClient(base_url, "user", "pass")
        mock_issues = {"issues": [{"id": "1", "key": "ISSUE-1"}]}
        responses.add(
            responses.GET,
            f"{base_url}/rest/api/2/search",
            json=mock_issues,
            status=200
        )
        result = client.fetch_issues("PROJ")
        self.assertEqual(result, mock_issues)

if __name__ == '__main__':
    unittest.main()
