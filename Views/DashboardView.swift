import SwiftUI

struct DashboardView: View {
    @StateObject var viewModel = DashboardViewModel()
    
    var body: some View {
        NavigationView {
            VStack {
                TimerDisplayView(viewModel: viewModel)
                ProjectListView(viewModel: viewModel)
            }
            .navigationTitle("TimeTracker")
        }
    }
}

struct TimerDisplayView: View {
    @ObservedObject var viewModel: DashboardViewModel
    
    var body: some View {
        Text(viewModel.currentTimer?.duration.formatted() ?? "00:00:00")
        Button(viewModel.isRunning ? "Pause" : "Start") {
            viewModel.toggleTimer()
        }
    }
}

struct ProjectListView: View {
    @ObservedObject var viewModel: DashboardViewModel
    
    var body: some View {
        List(viewModel.entries) { entry in
            Text(entry.startTime.formatted())
        }
    }
}