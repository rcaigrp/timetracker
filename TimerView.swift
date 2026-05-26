import SwiftUI
import SwiftData

struct TimerView: View {
    @State private var isRunning = false
    @Environment(\.modelContext) private var context
    
    var body: some View {
        Button(isRunning ? "Stop" : "Start") {
            if isRunning {
                stopTimer()
            } else {
                startTimer()
            }
        }
    }
    
    private func startTimer() {
        isRunning = true
        let entry = TimerEntry(id: UUID().uuidString, projectName: "Project", startTime: Date(), endTime: nil, duration: 0)
        context.append(entry)
    }
    
    private func stopTimer() {
        isRunning = false
    }
}
