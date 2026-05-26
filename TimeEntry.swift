import SwiftData
import Foundation

@Model
final class TimeEntry {
    var id: String
    var projectName: String
    var startDate: Date
    var endDate: Date?
    var duration: TimeInterval
    var notes: String
    
    init(projectName: String, startDate: Date, endDate: Date? = nil, duration: TimeInterval = 0, notes: String = "") {
        self.id = UUID().uuidString
        self.projectName = projectName
        self.startDate = startDate
        self.endDate = endDate
        self.duration = duration
        self.notes = notes
    }
}
