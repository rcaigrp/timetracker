# TimeTracker iOS App

A native iOS application for tracking time spent on development projects with Jira integration.

## Features
- Timer functionality for manual time tracking
- Jira API integration for project fetching and time logging
- Local storage of time logs
- Settings screen for Jira credentials
- Export and clear functionality

## Architecture
- SwiftUI for UI components
- SwiftData for local data persistence
- URLSession for API calls with rate limit handling

## Files
- `StorageManager.swift`: Manages local data persistence
- `JiraAPIService.swift`: Handles Jira API interactions
- `TimerModel.swift`: Core time tracking logic

## Getting Started
1. Open in Xcode
2. Build and run on simulator
3. Configure Jira credentials in Settings
4. Start tracking time on projects