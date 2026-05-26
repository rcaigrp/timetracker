import SwiftData

@Model
final class Project {
    var id: UUID
    var name: String
    var jiraKey: String?
    
    init(id: UUID = UUID(), name: String, jiraKey: String? = nil) {
        self.id = id
        self.name = name
        self.jiraKey = jiraKey
    }
}