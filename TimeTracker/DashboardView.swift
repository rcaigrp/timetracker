import SwiftUI
import PythonKit

struct DashboardView: View {
    @State private var timerRunning = false
    @State private var elapsed: Int = 0
    @State private var entries: [String] = []

    let storage: Storage = PythonBridge.storage
    let networking: JiraClient = PythonBridge.networking

    var body: some View {
        VStack {
            Text("TimeTracker")
                .font(.largeTitle)
            
            TimerDisplay(elapsed: elapsed, running: timerRunning)
            
            Button(action: toggleTimer) {
                Text(timerRunning ? "Stop" : "Start")
                    .buttonStyle(.bordered)
            }
            
            List(entries, id: \.self) { entry in
                Text(entry)
            }
            
            NavigationLink(destination: SettingsView()) {
                Text("Settings")
            }
        }
        .onAppear {
            loadEntries()
        }
    }

    func toggleTimer() {
        if timerRunning {
            elapsed = 0
            timerRunning = false
        } else {
            timerRunning = true
        }
    }

    func loadEntries() {
        entries = storage.get_entries().map { $0["project"] as! String }
    }
}
