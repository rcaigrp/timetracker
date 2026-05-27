# TimeTracker

A web-based time tracking application that enables users to track time spent on development projects with Jira integration.

## Features
- Main dashboard with working timer and project list
- Manual time entry screen
- Settings screen for Jira API credentials (base URL, API token)
- Automatic project fetching from Jira API
- Local storage of logs
- Summary/export functionality

## Installation

```bash
pip install flask requests responses
```

## Usage

Start the application:

```bash
python app.py
```

Then visit `http://localhost:5000` in your browser.

## Configuration

The application uses environment variables for configuration. Set these before running:

- JIRA_BASE_URL: Your Jira instance URL
- JIRA_USERNAME: Your Jira username/email
- JIRA_API_KEY: Your Jira API key

## Testing

Run the acceptance tests with:

```bash
pytest acceptance_tests.py -v
```
