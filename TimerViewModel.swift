import Foundation
import SwiftData
import Combine

@MainActor
class TimerViewModel: ObservableObject {
    @Published var entries: [TimeEntry] = []
    @Published var currentEntry: TimeEntry?
    @Published var isRunning: Bool = false
    
    var timer: Timer?
    var startTime: Date?
    
    init() {
        loadEntries()
    }
    
    func startTimer(projectName: String) {
        let newEntry = TimeEntry(projectName: projectName, startDate: Date())
        currentEntry = newEntry
        isRunning = true
        startTime = Date()
        saveEntry(newEntry)
    }
    
    func stopTimer() {
        guard let entry = currentEntry, let start = startTime else { return }
        let stopTime = Date()
        let duration = stopTime.timeIntervalSince(start)
        
        let updatedEntry = TimeEntry(
            projectName: entry.projectName,
            startDate: entry.startDate,
            endDate: stopTime,
            duration: duration,
            notes: entry.notes
        )
        
        updateEntry(updatedEntry)
        currentEntry = nil
        isRunning = false
        startTime = nil
    }
    
    func pauseTimer() {
        if let entry = currentEntry, let start = startTime {
            stopTimer()
        }
    }
    
    private func loadEntries() {
        entries = []
    }
    
    private func saveEntry(_ entry: TimeEntry) {
        entries.append(entry)
    }
    
    private func updateEntry(_ entry: TimeEntry) {
        if let index = entries.firstIndex(where: { $0.id == entry.id }) {
            entries[index] = entry
        }
    }
}
