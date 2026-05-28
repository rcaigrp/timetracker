# TimeTracker

A simple time tracking application that records start and stop times for tasks.

## Installation

```bash
pip install flask requests flask-cors
```

## Usage

```bash
python app.py
```

## Configuration

Create a `settings.json` file in the project root:
```json
{
  "jira_url": "https://your-jira-instance.atlassian.net",
  "api_key": "your-api-key",
  "username": "your-username"
}
```

Data is stored in `settings.json` for configuration.