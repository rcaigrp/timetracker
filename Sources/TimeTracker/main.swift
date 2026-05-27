// Entry point for the TimeTracker application
// This is a cross-platform stub that can be compiled in container environment
import Foundation
import TimeTrackerLib

print("TimeTracker application initialized")

// In a real iOS environment, this would launch the SwiftUI app
// For container testing, we'll just verify the build works
let tracker = TimeTrackerLib()
print("TimeTracker library loaded successfully: \(tracker)")
