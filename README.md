# TimeTracker

A simple time tracking application with Jira integration.

## Installation

```bash
pip install flask requests
```

## Usage

```bash
python app.py
```

## Configuration

The application requires Jira API credentials to fetch projects. Update the `app.py` file with the following:

- **JIRA_BASE_URL**: URL of your Jira instance (e.g., `https://your-company.atlassian.net`)
- **JIRA_USERNAME**: Your Jira username or email
- **JIRA_API_KEY**: Your API token generated from Jira settings
