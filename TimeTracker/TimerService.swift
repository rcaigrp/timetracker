import Foundation
import PythonKit

class TimerService: ObservableObject {
    @Published var elapsed: Int = 0
    @Published var isRunning: Bool = false

    private var timer: Timer?

    func start() {
        if isRunning { return }
        isRunning = true
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            self.elapsed += 1
        }
    }

    func pause() {
        if !isRunning { return }
        isRunning = false
        timer?.invalidate()
        timer = nil
    }

    func stop() {
        pause()
        elapsed = 0
    }
}
