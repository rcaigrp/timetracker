import Foundation

public struct Project: Codable, Identifiable {
    public let id = UUID()
    public var name: String
    public var elapsedTime: TimeInterval
    
    public init(name: String, elapsedTime: TimeInterval) {
        self.name = name
        self.elapsedTime = elapsedTime
    }
    
    public var elapsedTimeFormatted: String {
        let hours = Int(elapsedTime) / 3600
        let minutes = (Int(elapsedTime) % 3600) / 60
        let seconds = Int(elapsedTime) % 60
        return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
    }
}