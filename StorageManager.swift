import SwiftData
import Foundation

@Model
final class TimeEntry: Identifiable {
    @Attribute(.nonMigrationable) var id: UUID
    var project: String
    var startTime: Date
    var endTime: Date?
    var duration: TimeInterval
    var notes: String?
    
    init(project: String, startTime: Date, duration: TimeInterval, notes: String? = nil) {
        self.id = UUID()
        self.project = project
        self.startTime = startTime
        self.duration = duration
        self.notes = notes
    }
}

class StorageManager {
    static let shared = StorageManager()
    private let container: NSPersistentContainer

    init() {
        self.container = NSPersistentContainer(name: "TimeTracker")
        self.container.loadPersistentStores { _, error in
            if let error = error {
                print("Failed to load persistent stores: \(error)")
            }
        }
    }

    func save(entry: TimeEntry) {
        // Implementation in SwiftData context
    }

    func fetchEntries() -> [TimeEntry] {
        return []
    }
}