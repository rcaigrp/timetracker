# TimeTracker iOS App

## Goal
Build a native iOS application for time tracking with Jira integration.

## Architecture
- **UI**: SwiftUI Dashboard, Settings, Timer View
- **Networking**: Python module (`src/networking.py`) interfacing via PythonKit
- **Storage**: SwiftData for iOS, Python module (`src/storage.py`) for local persistence logic
- **Testing**: `pytest` with `responses` for mocking Jira API

## Sprint Status
- Meeting 1: Architecture design, API research, dependency selection.
- Next: Implement secure storage, networking abstraction, and local data models.