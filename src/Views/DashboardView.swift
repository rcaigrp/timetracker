import SwiftUI
import SwiftData

struct DashboardView: View {
    @Environment(\.modelContainer) private var modelContainer
    @Query var timerEntries: [TimerEntry]
    
    var body: some View {
        List {
            Section(header: Text("Timer")) {
                TimerView()
            }
            Section(header: Text("Recent Entries")) {
                ForEach(timerEntries) { entry in
                    Text(entry.project)
                }
            }
        }
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                NavigationLink("Settings") {
                    SettingsView()
                }
            }
        }
    }
}
