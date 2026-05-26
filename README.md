# TimeTracker iOS App

## Goal
Build a native iOS application for time tracking with Jira integration.

## Architecture
- **UI**: SwiftUI Dashboard, Settings, Timer View
- **Networking**: Pure Swift `URLSession` for Jira API
- **Storage**: SwiftData for local persistence
- **Testing**: `pytest` for static analysis of Swift code

## Sprint Status
- Meeting 2: Refactored to pure Swift. Removed PythonKit and Chrome artifacts.
- Next: Implement background suspension handling and complete UI polish.
