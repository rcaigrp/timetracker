# TimeTracker

A web-based time tracking application with Jira integration.

## Installation

```bash
pip install flask requests pytest responses
```

## Usage

```bash
python app.py
```

## Configuration

**Required Environment Variables / Settings:**
1. `JIRA_URL`: The base URL of your Jira instance (e.g., `https://your-company.atlassian.net`)
2. `JIRA_API_KEY`: The API token for Jira authentication.
3. `JIRA_USERNAME`: The username for the Jira account.

Data is persisted locally in `settings.json` and `time_entries.json`.
