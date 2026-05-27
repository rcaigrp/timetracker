# Time Tracker

A simple command-line time tracking tool that records task durations using SQLite.

## Installation

No installation required. Just run the Python script directly.

```bash
python main.py
```

## Usage

Start a task:
```bash
python main.py start "task name"
```

Stop a task:
```bash
python main.py stop "task name"
```

List active tasks:
```bash
python main.py list
```

Show report of all tracked tasks:
```bash
python main.py report
```

## Configuration

The tool uses a SQLite database file called `timetracker.db` in the current directory to store task data.