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
- Meeting 2 (Current): Establish acceptance criteria, baseline tests, and core module stubs.
- Next: Implement secure storage, networking abstraction, and local data models.

## Completed Work
- Project initialized with `project.json` and `README.md`.
- Acceptance tests defined covering all 7 criteria.
- Previous agents provided `TimeTrackerViewModel`, `JiraClient`, and UI delegation patterns.

## Known Bugs
- None reported yet.

## Next Steps
- Refine ViewModel logic for background suspension handling.
- Integrate JiraClient with mocked responses for API validation.
- Prepare for Meeting 3 implementation sprint.