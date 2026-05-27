# TimeTracker

A native iOS application that enables users to track time spent on development projects through both manual entries and seamless Jira integration via configured API endpoints.

## Features
- Main dashboard with working timer and project list
- Manual time entry screen
- Settings screen for Jira API credentials (base URL, API token)
- Automatic project fetching from Jira API
- Local storage of logs
- Summary/export functionality

## Tech Stack
- SwiftUI for UI
- UIKit for iOS target
- URLSession for API calls with rate limit handling

## Development Plan
1. Set up basic iOS project structure
2. Implement Settings screen with credential storage
3. Build Jira API integration layer
4. Create manual time entry interface
5. Add local data persistence
6. Implement summary/export functionality