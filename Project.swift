// Project Model
import Foundation

struct Project: Codable, Identifiable {
    let id = UUID()
    var name: String
    var description: String = ""
}