#!/usr/bin/env python3
"""
Jira sync functionality to send time logs to Jira API.
"""

import requests
import os
from datetime import datetime
import time


class JiraSync:
    def __init__(self):
        self.base_url = os.getenv('JIRA_BASE_URL')
        self.username = os.getenv('JIRA_USERNAME')
        self.api_token = os.getenv('JIRA_API_TOKEN')
        
        if not all([self.base_url, self.username, self.api_token]):
            raise Exception("Jira credentials not configured. Set JIRA_BASE_URL, JIRA_USERNAME, and JIRA_API_TOKEN environment variables.")

    def sync_log(self, issue_key, start_time, end_time):
        """Sync a single time log to Jira."""
        # Calculate duration in hours
        start_dt = datetime.fromisoformat(start_time)
        end_dt = datetime.fromisoformat(end_time)
        duration = (end_dt - start_dt).total_seconds() / 3600  # Convert seconds to hours
        
        # Jira API endpoint for time tracking
        url = f"{self.base_url}/rest/api/2/issue/{issue_key}/worklog"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self._get_auth_token()}'
        }
        
        data = {
            'started': start_dt.strftime('%Y-%m-%dT%H:%M:%S.000+0000'),
            'timeSpent': f'{int(duration * 60)}m'  # Convert hours to minutes string
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 1))
                time.sleep(retry_after)
                return self.sync_log(issue_key, start_time, end_time)  # Retry once
            
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            # Handle specific HTTP errors
            if response.status_code == 401:
                raise Exception("Authentication failed. Check Jira credentials.")
            elif response.status_code == 403:
                raise Exception("Access denied. Check permissions for Jira API access.")
            else:
                raise Exception(f"Failed to sync log: {e}")

    def _get_auth_token(self):
        """Generate base64 encoded authentication token."""
        import base64
        credentials = f'{self.username}:{self.api_token}'
        return base64.b64encode(credentials.encode()).decode()
