# TimeTracker

A Python web application that enables users to track time spent on development projects through manual entries with local storage persistence.

## Features
- Web interface for time tracking
- Manual project entry with start/stop timer
- Local storage of logs between sessions
- Summary view of tracked time

## Installation
```bash
pip install flask
```

## Usage
Run the application:
```bash
python app.py
```
Then visit `http://localhost:5000` in your browser.

## Configuration
No configuration needed. All data is stored locally in `timer_data.json`.