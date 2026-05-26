// TimerModel.swift
import Foundation

class TimerModel: ObservableObject {
    @Published var isRunning = false
    @Published var elapsedTime = 0
    
    private var timer: Timer?
    
    func start() {
        isRunning = true
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            self.elapsedTime += 1
        }
    }
    
    func pause() {
        isRunning = false
        timer?.invalidate()
        timer = nil
    }
    
    func stop() {
        isRunning = false
        timer?.invalidate()
        timer = nil
        elapsedTime = 0
    }
}
