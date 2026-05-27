// TimerService.swift
import Foundation

class TimerService: ObservableObject {
    @Published var isRunning = false
    @Published var elapsedTime: TimeInterval = 0
    private var timer: Timer?
    private var startTime: Date?

    func startTimer() {
        guard !isRunning else { return }
        isRunning = true
        startTime = Date()
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
            if let startTime = self.startTime {
                self.elapsedTime = Date().timeIntervalSince(startTime)
            }
        }
    }

    func stopTimer() {
        isRunning = false
        timer?.invalidate()
        timer = nil
    }

    func resetTimer() {
        stopTimer()
        elapsedTime = 0
    }
}