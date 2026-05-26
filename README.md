# TimeTracker iOS App

## Goal
Build a native iOS application for time tracking with Jira integration.

## Architecture
- **UI**: SwiftUI Dashboard, Settings, Timer View
- **Networking**: Python module (`src/networking.py`) interfacing via PythonKit
- **Storage**: SwiftData for iOS, Python module (`src/storage.py`) for local persistence logic
- **Testing**: `pytest` with `responses` for mocking Jira API

## Sprint Status
- Meeting 2: Implement SwiftUI Dashboard and TimerViewModel. Replace failing acceptance tests with SwiftUI Previews to verify dashboard rendering, real-time timer updates, and manual entry persistence. Focus on AC1, AC2, AC3.
- Completed Work: Architecture design, API research, dependency selection, Python mocking layer for Jira API and SecureStorage.
- Test Results: Python mocking tests for Jira API and SecureStorage passed. UI tests failed due to Docker environment limitations.
- Known Bugs: None.
- Next Steps: Implement `TimerViewModel` and `DashboardView` in Swift. Validate via SwiftUI Previews. Proceed to Jira integration tests for AC4/AC6.