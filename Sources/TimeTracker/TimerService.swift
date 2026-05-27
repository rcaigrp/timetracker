import Foundation

class TimerService {
    private var timer: Timer?
    private var elapsedTime = 0
    private var isRunning = false
    
    func startTimer() {
        guard !isRunning else { return }
        isRunning = true
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            self.elapsedTime += 1
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
    
    func getElapsedTime() -> Int {
        return elapsedTime
    }
}