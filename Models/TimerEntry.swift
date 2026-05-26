import SwiftData

@Model
final class TimerEntry {
    var id: UUID
    var projectId: UUID
    var startTime: Date
    var endTime: Date?
    var duration: TimeInterval
    
    init(id: UUID = UUID(), projectId: UUID, startTime: Date, endTime: Date? = nil, duration: TimeInterval = 0) {
        self.id = id
        self.projectId = projectId
        self.startTime = startTime
        self.endTime = endTime
        self.duration = duration
    }
}