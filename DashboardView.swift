import SwiftUI
import SwiftData

struct DashboardView: View {
    @StateObject var viewModel = TimerViewModel()
    @Environment(\.modelContext) private var context
    
    var body: some View {
        List {
            Section(header: Text("Active Timer")) {
                TimerView(viewModel: viewModel)
            }
            Section(header: Text("Recent Entries")) {
                ForEach(viewModel.recentEntries) { entry in
                    Text(entry.startTime.description)
                }
            }
        }
    }
}
