// TimerService.swift
import Foundation

class TimerService: ObservableObject {
    @Published var isRunning = false
    @Published var elapsedTime: TimeInterval = 0
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
        lastStartTime = nil
    }
    
    func pauseTimer() {
        guard isRunning else { return }
        isRunning = false
        timer?.invalidate()
        timer = nil
    }
    
    func resetTimer() {
        stopTimer()
        elapsedTime = 0
    }
}