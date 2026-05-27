import Foundation

class TimerModel: ObservableObject {
    @Published var isRunning = false
    @Published var elapsedTime: TimeInterval = 0
    
    private var timer: Timer?
    private var startTime: Date?
    
    func start() {
        guard !isRunning else { return }
        
        isRunning = true
        startTime = Date()
        
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.elapsedTime = Date().timeIntervalSince(self.startTime!)
        }
    }
    
    func pause() {
        guard isRunning else { return }
        
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
