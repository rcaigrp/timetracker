# TimeTracker

A Python web application that enables users to track time spent on development projects through both manual entries and seamless Jira integration.

## Features
- Main dashboard with working timer and project list
- Manual time entry screen
- Settings screen for Jira API credentials (base URL, API token)
- Automatic project fetching from Jira API
- Local storage of logs
- Summary/export functionality

## Installation
```bash
pip install flask requests
```

## Usage
```bash
python app.py
```

Then visit `http://localhost:5000` in your browser.

## Configuration
- Jira Base URL: `JIRA_BASE_URL`
- Jira Username: `JIRA_USERNAME`
- Jira API Key: `JIRA_API_KEY`
