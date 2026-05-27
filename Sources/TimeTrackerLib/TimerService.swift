//
// TimerService.swift
// TimeTracker
//

import Foundation

public class TimerService {
    private var timer: Timer?
    private var startTime: Date?
    private var elapsedTime: TimeInterval = 0
    
    public init() {}
    
    public func startTimer() {
        startTime = Date()
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            // Update UI or log time
        }
    }
    
    public func stopTimer() {
        timer?.invalidate()
        timer = nil
        startTime = nil
    }
    
    public func getElapsedTime() -> TimeInterval {
        if let startTime = startTime {
            return Date().timeIntervalSince(startTime) + elapsedTime
        }
        return elapsedTime
    }
    
    public func resetTimer() {
        timer?.invalidate()
        timer = nil
        startTime = nil
        elapsedTime = 0
    }
}
