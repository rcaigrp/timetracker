# LocalTrack Browser Extension

## Goal
Build a privacy-first, local-only Browser Extension called 'LocalTrack' for tracking project time. The extension must operate entirely offline with zero cloud dependency, accounts, or telemetry.

## Architecture
- **UI**: Vanilla JS, HTML, CSS, Manifest V3.
- **Storage**: chrome.storage.local for timer state and entries.
- **Export**: Blob and URL.createObjectURL for JSON/CSV.
- **Testing**: pytest with static file validation and logic checks.

## Sprint Status
- Meeting 1: Architecture design, API research, dependency selection.
- Meeting 2: Implemented core extension files, persistence logic, and acceptance tests.
- Next: Verify tests pass, refine UI, and finalize export functionality.
