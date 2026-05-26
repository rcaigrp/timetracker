import SwiftUI
import SwiftData

struct DashboardView: View {
    @State private var isTimerRunning = false
    @State private var elapsedTime: TimeInterval = 0
    @State private var timer: Timer?
    @Environment(\.managedContext) private var managedContext

    var body: some View {
        VStack {
            Text("TimeTracker")
            TimerView(elapsedTime: $elapsedTime, isRunning: $isTimerRunning)
            EntryList()
        }
    }

    func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            elapsedTime += 1
        }
        isTimerRunning = true
    }

    func stopTimer() {
        timer?.invalidate()
        timer = nil
        isTimerRunning = false
    }
}

struct TimerView: View {
    @Binding var elapsedTime: TimeInterval
    @Binding var isRunning: Bool

    var body: some View {
        VStack {
            Text("Elapsed: \(elapsedTime.formatted())")
            Button(isRunning ? "Stop" : "Start") { isRunning.toggle() }
        }
    }
}

struct EntryList: View {
    var body: some View {
        List {
            Text("No entries")
        }
    }
}