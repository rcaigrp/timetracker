// TimeTracker - Simple CLI time tracking tool
import Foundation

// MARK: - Data Models
struct Project: Codable {
    let id: String
    let name: String
    let startTime: Date?
    let endTime: Date?
    var duration: TimeInterval {        if let start = startTime, let end = endTime {
            return end.timeIntervalSince(start)
        }
        return 0
    }
    
    init(name: String) {
        self.id = UUID().uuidString
        self.name = name
        self.startTime = nil
        self.endTime = nil
    }
}

// MARK: - Storage Manager
struct StorageManager {
    static let fileName = "time_entries.json"
    
    static func saveProjects(_ projects: [Project]) throws {
        let data = try JSONEncoder().encode(projects)
        try data.write(to: FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!.appendingPathComponent(fileName))
    }
    
    static func loadProjects() -> [Project] {
        guard let url = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first?.appendingPathComponent(fileName) else { return [] }
        
        do {
            let data = try Data(contentsOf: url)
            return try JSONDecoder().decode([Project].self, from: data)
        } catch {
            // Return empty array if file doesn't exist or is corrupted
            return []
        }
    }
}

// MARK: - Timer Service
final class TimerService {
    private var timer: Timer?
    private var startTime: Date?
    private var elapsedTime: TimeInterval = 0
    
    func startTimer() {
        guard startTime == nil else { return }
        startTime = Date()
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
            self.elapsedTime = Date().timeIntervalSince(self.startTime!)
            print("Elapsed time: \(self.formatTime(self.elapsedTime))")
        }
    }
    
    func stopTimer() {
        timer?.invalidate()
        timer = nil
        startTime = nil
    }
    
    func resetTimer() {
        timer?.invalidate()
        timer = nil
        startTime = nil
        elapsedTime = 0
        print("Timer reset")")
    }
    
    private func formatTime(_ timeInterval: TimeInterval) -> String {
        let hours = Int(timeInterval) / 3600
        let minutes = Int(timeInterval) / 60 % 60
        let seconds = Int(timeInterval) % 60
        return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
    }
}

// MARK: - Main Program
func main() {
    print("TimeTracker CLI Tool")
    print("Commands: start, stop, reset, list, quit")
    
    let timerService = TimerService()
    var projects: [Project] = StorageManager.loadProjects()
    
    while true {
        print("> ", terminator: "")
        guard let input = readLine()?.lowercased() else { continue }
        
        switch input {
        case "start":
            timerService.startTimer()
        case "stop":
            timerService.stopTimer()
        case "reset":
            timerService.resetTimer()
        case "list":
            for project in projects {
                print("- \(project.name): \(project.duration) seconds")
            }
        case "quit":
            // Save projects before quitting
            try? StorageManager.saveProjects(projects)
            print("Goodbye!")
            exit(0)
        default:
            print("Unknown command. Try: start, stop, reset, list, quit")
        }
    }
}

main()