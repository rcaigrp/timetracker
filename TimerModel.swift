// TimerModel.swift
import Foundation

class TimerModel {
    var id = UUID()
    var startTime: Date
    var endTime: Date?
    var duration: TimeInterval = 0
    var projectName: String
    
    init(projectName: String) {
        self.projectName = projectName
        self.startTime = Date()
    }
    
    func stopTimer() {
        endTime = Date()
        duration = endTime!.timeIntervalSince(startTime)
    }
    
    func formatDuration() -> String {
        let hours = Int(duration) / 3600
        let minutes = (Int(duration) % 3600) / 60
        let seconds = Int(duration) % 60
        return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
    }
}