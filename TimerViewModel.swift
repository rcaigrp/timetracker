import Foundation
import SwiftUI

@MainActor
class TimerViewModel: ObservableObject {
    @Published var isRunning = false
    @Published var elapsedTime: TimeInterval = 0
    @Published var currentEntry: TimeEntryModel?
    
    private var startTimestamp: Date?
    
    func startTimer(projectId: UUID) {
        let entry = TimeEntryModel(projectId: projectId, startTime: Date.now)
        currentEntry = entry
        startTimestamp = Date.now
        isRunning = true
    }
    
    func stopTimer() {
        if let start = startTimestamp, let entry = currentEntry {
            let end = Date.now
            currentEntry?.endTime = end
            currentEntry?.duration = end.timeIntervalSince(start)
            isRunning = false
            currentEntry = nil
            startTimestamp = nil
        }
    }
    
    func updateElapsed() {
        if isRunning, let start = startTimestamp {
            elapsedTime = Date.now.timeIntervalSince(start)
        }
    }
}
