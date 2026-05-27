# TimeTracker

A simple command-line time tracking application that records start and stop times for projects.

## Installation

```bash
pip install click
```

## Usage

Start tracking a project:
```bash
python main.py start "Project Alpha"
```

Stop tracking a project:
```bash
python main.py stop "Project Alpha"
```

View all tracked projects:
```bash
python main.py list
```

## Configuration

The application stores data in a SQLite database file called `timetracker.db` in the current directory.
