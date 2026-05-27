# TimeTracker

A simple web-based time tracking application that allows users to start, stop, and check elapsed time.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Start the server:

```bash
python main.py
```

Then interact with the API:

- Start timer: `curl -X POST http://localhost:5000/start`
- Stop timer: `curl -X POST http://localhost:5000/stop`
- Check time: `curl http://localhost:5000/time`

## Configuration

The application runs on port 5000 by default.
