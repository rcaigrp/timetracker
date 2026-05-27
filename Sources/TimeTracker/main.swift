import Foundation

enum TimeTrackerCommand: String, CaseIterable {
    case start
    case stop
    case reset
    case status
}

class TimerService {
    private var isRunning = false
    private var elapsedTime: TimeInterval = 0
    private var timer: Timer?
    private var startTime: Date?
    
    func start() {
        guard !isRunning else { return }
        isRunning = true
        startTime = Date()
        
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
            self.elapsedTime = Date().timeIntervalSince(self.startTime!)
        }
    }
    
    func stop() {
        isRunning = false
        timer?.invalidate()
        timer = nil
    }
    
    func reset() {
        stop()
        elapsedTime = 0
        startTime = nil
    }
    
    func getStatus() -> (isRunning: Bool, elapsedTime: TimeInterval) {
        return (isRunning, elapsedTime)
    }
}

func printUsage() {
    print("Usage: TimeTracker <command>")
    print("Commands:")
    for command in TimeTrackerCommand.allCases {
        print("  \(command.rawValue)")
    }
}

let service = TimerService()

if CommandLine.arguments.count < 2 {
    printUsage()
    exit(1)
}

let command = CommandLine.arguments[1]

switch command {
    case "start":
        service.start()
        print("Timer started")
    case "stop":
        service.stop()
        print("Timer stopped")
    case "reset":
        service.reset()
        print("Timer reset")
    case "status":
        let (isRunning, elapsedTime) = service.getStatus()
        print("Status: \(isRunning ? "Running" : "Stopped") | Elapsed: \(String(format: "%.1f", elapsedTime))s")
    default:
        print("Unknown command: \(command)")
        printUsage()
        exit(1)
}