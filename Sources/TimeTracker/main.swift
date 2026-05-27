// Time Tracker Application
import Foundation

struct TimeEntry {
    let id = UUID()
    let startTime: Date
    let endTime: Date?
    let description: String
}

class TimeTracker {
    private var entries: [TimeEntry] = []
    
    func startTracking(description: String) -> TimeEntry {
        let entry = TimeEntry(startTime: Date(), endTime: nil, description: description)
        entries.append(entry)
        print("Started tracking: \(description)")
        return entry
    }
    
    func stopTracking(id: UUID) {
        guard let index = entries.firstIndex(where: { $0.id == id }) else { return }
        entries[index].endTime = Date()
        print("Stopped tracking: \(entries[index].description)")
    }
    
    func listEntries() {
        for entry in entries {
            let duration = entry.endTime != nil ? 
                entry.endTime!.timeIntervalSince(entry.startTime) : 
                Date().timeIntervalSince(entry.startTime)
            print("\(entry.description): \(String(format: "%.2f", duration)) seconds")
        }
    }
}

let tracker = TimeTracker()

// Example usage
let entry1 = tracker.startTracking(description: "Programming")
tracker.listEntries()

// Simulate stopping tracking
tracker.stopTracking(id: entry1.id)
tracker.listEntries()