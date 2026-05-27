import Foundation

class Project: Codable {
    public let id: UUID
    public var name: String
    public var description: String?
    
    init(id: UUID = UUID(), name: String, description: String? = nil) {
        self.id = id
        self.name = name
        self.description = description
    }
}