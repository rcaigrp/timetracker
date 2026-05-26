import SwiftData

@Model
final class ProjectModel {
    var id: UUID
    var name: String
    var createdAt: Date

    init(id: UUID = UUID(), name: String, createdAt: Date = Date.now) {
        self.id = id
        self.name = name
        self.createdAt = createdAt
    }
}
