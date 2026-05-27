import Foundation

class StorageManager {
    static let shared = StorageManager()
    
    private init() {}
    
    func save(entries: [TimeEntry]) {
        // Implementation for saving to UserDefaults or Core Data
    }
    
    func loadEntries() -> [TimeEntry] {
        // Implementation for loading from UserDefaults or Core Data
        return []
    }
}

struct TimeEntry: Codable {
    let id: String
    let projectKey: String
    let startTime: Date
    let endTime: Date?
    let notes: String?
}
