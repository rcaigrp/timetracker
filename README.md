# TimeTracker

A simple Python Flask application for tracking time with Jira integration.

## Installation & Setup

1. Ensure Python 3.6+ is installed.
2. Install dependencies:
   ```bash
   pip install flask requests pytest responses
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```
2. The app will run on `http://127.0.0.1:5000`

## Running Tests

Run the acceptance tests:
```bash
pytest acceptance_tests.py -v
```

## Configuration

The app looks for a `data` directory in the root. Settings are stored in `data/settings.json`. Logs are stored in `data/logs.json`.