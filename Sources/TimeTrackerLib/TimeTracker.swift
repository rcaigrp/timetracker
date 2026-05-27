import Foundation

class TimeTracker {
    private var startTime: Date?
    private var elapsedTime: TimeInterval = 0
    
    func start() {
        startTime = Date()
    }
    
    func stop() {
        if let start = startTime {
            elapsedTime += Date().timeIntervalSince(start)
            startTime = nil
        }
    }
    
    func reset() {
        startTime = nil
        elapsedTime = 0
    }
    
    func getElapsedTime() -> TimeInterval {
        if let start = startTime {
            return elapsedTime + Date().timeIntervalSince(start)
        }
        return elapsedTime
    }
}