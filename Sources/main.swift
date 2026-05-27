// Time Tracker App
import Foundation

struct TimeEntry {
    let id: String
    let description: String
    let startTime: Date
    let endTime: Date?
}

class TimeTracker {
    func startTracking(description: String) -> TimeEntry {
        return TimeEntry(id: UUID().uuidString, description: description, startTime: Date(), endTime: nil)
    }
    
    func stopTracking(_ entry: inout TimeEntry) {
        entry.endTime = Date()
    }
}

// Example usage
let tracker = TimeTracker()
var entry = tracker.startTracking(description: "Working on project")
print("Started tracking: \(entry.description)")

// Simulate stopping the timer
tracker.stopTracking(&entry)
print("Stopped tracking: \(entry.description)")
