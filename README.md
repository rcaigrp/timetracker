# TimeTracker

A web-based time tracking application with Jira integration.

## Installation

```bash
pip install flask flask-cors requests pytest responses
```

## Usage

```bash
python app.py
```

## Configuration

1. **Jira API Credentials:**
   - Set `JIRA_BASE_URL` (e.g., `https://your-company.atlassian.net`)
   - Set `JIRA_API_KEY` (Personal API Token)
   - Set `JIRA_USERNAME` (Email address)

2. **Data Persistence:**
   - Data is stored in `time_tracker.json` by default.

## API Endpoints

- `GET /api/settings` - Retrieve Jira configuration
- `POST /api/settings` - Update Jira configuration
- `GET /api/projects` - Fetch projects from Jira
- `POST /api/timer` - Start/Stop timer
- `GET /api/timer` - Retrieve current timer status
- `GET /api/logs` - Retrieve time logs

---

*Note: This is a backend API. A React frontend is required to consume these endpoints.*