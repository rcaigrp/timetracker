import SwiftUI

struct DashboardView: View {
    @StateObject var viewModel: TimeTrackerViewModel
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack {
                    // Timer Display
                    TimerDisplay(seconds: viewModel.elapsedSeconds, isRunning: viewModel.isRunning)
                    
                    // Controls
                    HStack {
                        Button("Start") { viewModel.startTimer() }
                        Button("Pause") { viewModel.pauseTimer() }
                        Button("Stop") { viewModel.stopTimer() }
                    }
                    
                    // Recent Entries
                    EntryList(entries: viewModel.entries)
                    
                    // Settings Link
                    NavigationLink("Settings") {
                        SettingsView()
                    }
                }
                .padding()
            }
            .navigationTitle("TimeTracker")
        }
    }
}

struct TimerDisplay: View {
    let seconds: Int
    let isRunning: Bool
    
    var body: some View {
        Text("\(seconds / 60):\(String(format: "%02d", seconds % 60))")
            .font(.largeTitle)
            .foregroundColor(isRunning ? .green : .gray)
    }
}

struct EntryList: View {
    let entries: [TimeEntry]
    
    var body: some View {
        List(entries) { entry in
            Text(entry.project)
        }
    }
}
