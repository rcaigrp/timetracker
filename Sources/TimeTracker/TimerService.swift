import Foundation
import Combine

class TimerService: ObservableObject {
    @Published var elapsedTime: TimeInterval = 0
    @Published var isRunning = false
    @Published var projects: [Project] = []
    
    private var timer: Timer?
    private var lastStartTime: Date?
    
    func startTimer() {
        guard !isRunning else { return }
        
        isRunning = true
        lastStartTime = Date()
        
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.elapsedTime += 1
        }
    }
    
    func stopTimer() {
        guard isRunning else { return }
        
        isRunning = false
        timer?.invalidate()
        timer = nil
        
        // Save to projects
        let project = Project(name: "Untitled Task", elapsedTime: elapsedTime)
        projects.append(project)
        
        // Reset timer
        elapsedTime = 0
    }
    
    func resetTimer() {
        isRunning = false
        timer?.invalidate()
        timer = nil
        elapsedTime = 0
    }
    
    var elapsedTimeFormatted: String {
        let hours = Int(elapsedTime) / 3600
        let minutes = (Int(elapsedTime) % 3600) / 60
        let seconds = Int(elapsedTime) % 60
        return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
    }
}