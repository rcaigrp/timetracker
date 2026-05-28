# TimeTracker

A web-based time tracking application that records start and stop times for tasks and integrates with Jira.

## Installation

```bash
pip install flask flask-cors requests pytest responses
```

## Usage

1. Start the Flask backend:
```bash
python app.py
```

2. Run the tests:
```bash
pytest acceptance_tests.py -v
```

## Configuration

The application requires Jira configuration via environment variables:

- `JIRA_URL`: The base URL of your Jira instance (e.g., `https://your-company.atlassian.net`)
- `JIRA_USER`: Your Jira username
- `JIRA_API`: Your Jira API token or password

These settings can be updated via the `/api/settings` endpoint or the `.env` file.