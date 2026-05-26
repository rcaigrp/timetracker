import Foundation
import Combine

struct TimeEntry: Identifiable {
    let id = UUID()
    let project: String
    let startTime: Date
    let endTime: Date
    let duration: TimeInterval
}

class TimeTrackerViewModel: ObservableObject {
    @Published var isRunning: Bool = false
    @Published var elapsedSeconds: Int = 0
    @Published var entries: [TimeEntry] = []
    
    private var timerTimer: Timer?
    private var startTime: Date?
    
    let jiraClient: JiraClientProtocol
    
    init(jiraClient: JiraClientProtocol) {
        self.jiraClient = jiraClient
        self.loadEntries()
    }
    
    func startTimer() {
        guard !isRunning else { return }
        isRunning = true
        startTime = Date()
        timerTimer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            if let start = self.startTime {
                self.elapsedSeconds = Int(Date().timeIntervalSince(start))
            }
        }
    }
    
    func pauseTimer() {
        guard isRunning else { return }
        isRunning = false
        timerTimer?.invalidate()
        timerTimer = nil
    }
    
    func stopTimer() {
        guard isRunning || elapsedSeconds > 0 else { return }
        pauseTimer()
        if let start = startTime {
            let entry = TimeEntry(project: "Default", startTime: start, endTime: Date(), duration: TimeInterval(seconds: elapsedSeconds))
            entries.append(entry)
            self.saveEntries()
        }
        isRunning = false
        elapsedSeconds = 0
        startTime = nil
    }
    
    private func loadEntries() {
        // Simulate loading from persistent storage
        self.entries = []
    }
    
    private func saveEntries() {
        // Simulate saving to persistent storage
        print("Saved entries")
    }
}
