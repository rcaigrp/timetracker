import Foundation

struct Project: Identifiable, Codable {
    let id = UUID()
    let name: String
    
    init(name: String) {
        self.name = name
    }
}