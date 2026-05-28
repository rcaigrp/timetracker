# TimeTracker

A simple time tracking application that records start and stop times for tasks.

## Installation

```bash
cd /workspace/projects/TimeTracker
cp -r app.py .
# Ensure dependencies are installed
pip install flask flask-cors requests
```

## Usage

```bash
python app.py
```

## Configuration

**Required Environment:**
- `JIRA_BASE_URL`: The URL of your Jira instance (e.g., https://your-company.atlassian.net).
- `JIRA_API_KEY`: Your Jira API token or password.

Users must input these credentials via the Settings screen to access Jira API features (AC #3).