import SwiftUI
import SwiftData

struct DashboardView: View {
    @StateObject var viewModel: TimerViewModel
    
    var body: some View {
        VStack {
            TimerDisplayView(viewModel: viewModel)
            EntryListView(viewModel: viewModel)
        }
    }
}

struct TimerDisplayView: View {
    @ObservedObject var viewModel: TimerViewModel
    
    var body: some View {
        Text(viewModel.isRunning ? "Timer Running" : "Timer Stopped")
    }
}

struct EntryListView: View {
    @ObservedObject var viewModel: TimerViewModel
    
    var body: some View {
        List(viewModel.entries) { entry in
            Text(entry.projectName)
        }
    }
}
