import Foundation
import PythonBridge

class TimerService: ObservableObject {
    @Published var startTime: Date?
    @Published var elapsed: TimeInterval = 0
    @Published var isRunning = false
    
    var elapsedTimeFormatted: String {
        let minutes = Int(elapsed) / 60
        let seconds = Int(elapsed) % 60
        return String(format: "%02d:%02d", minutes, seconds)
    }
    
    func start() {
        startTime = Date()
        isRunning = true
    }
    
    func pause() {
        if isRunning {
            isRunning = false
        }
    }
    
    func stop() {
        if let start = startTime {
            let duration = Date().timeIntervalSince(start)
            PythonBridge.saveEntry(duration: duration)
        }
        startTime = nil
        elapsed = 0
        isRunning = false
    }
}
