# TimeTracker - iOS Time Tracking Application

## Project Overview

A native iOS application built with SwiftUI and SwiftData for tracking time spent on development projects. Features include:

- Main dashboard with working timer and project list
- Manual time entry screen with project selection
- Settings screen for Jira API credentials (base URL, API token)
- Automatic project fetching from Jira API
- Local storage of time logs with persistence
- Summary/export functionality

## Core Features

1. **Timer Functionality**
   - Start/Pause/Stop buttons for tracking elapsed time
   - Persistent timer state across app sessions

2. **Manual Entry**
   - Form fields for Project Name, Date, Duration (hours/minutes), and Optional Notes
   - Input validation for all fields

3. **Jira Integration**
   - Secure storage of Jira API credentials
   - Automatic fetching of projects from Jira API
   - Seamless integration with time tracking workflow

4. **Local Storage**
   - Persisted storage using SwiftData
   - All entries saved as structured data

5. **Export Functionality**
   - Generate JSON and CSV files from stored data
   - Download functionality via system prompts

## Technical Stack

- SwiftUI for UI framework
- SwiftData for local persistence
- URLSession for API calls with rate limit handling
- Xcode for development environment

## Acceptance Criteria

- Application launches cleanly on simulator
- Timer persists across app sessions
- Manual entries save and retrieve correctly
- Jira integration works as expected
- Export generates valid files with correct data
- All logic is client-side with no network dependencies
