# TimeTracker

A simple time tracking application that allows users to create projects, track time spent on each project, and manage Jira integration settings.

## Installation

```bash
pip install flask
```

## Usage

Run the application:

```bash
python app.py
```

The application will be available at http://localhost:5000

## API Endpoints

- `GET /` - Dashboard
- `POST /projects` - Create a new project
- `GET /projects` - List all projects
- `POST /projects/{id}/start` - Start timer for a project
- `POST /projects/{id}/stop` - Stop timer for a project
- `GET /projects/{id}/timer` - Get timer data for a project
- `POST /settings` - Set Jira settings
- `GET /settings` - Get current Jira settings

## Configuration

The application stores its data in JSON files:
- `projects.json` - Stores project information
- `timers.json` - Stores timer data
- `settings.json` - Stores Jira integration settings