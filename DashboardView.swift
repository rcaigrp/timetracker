import SwiftUI
import SwiftData

struct DashboardView: View {
    @Environment(\.dismiss) var dismiss
    @State private var showSettings = false
    @Query(sort: \\.date) var entries: [Entry]
    
    var body: some View {
        NavigationStack {
            VStack {
                TimerView()
                Divider()
                Text("Recent Entries")
                List(entries) { entry in
                    Text(entry.project)
                }
                Spacer()
                Button("Settings") {
                    showSettings = true
                }
            }
            .navigationTitle("TimeTracker")
            .sheet(isPresented: $showSettings) {
                SettingsView()
            }
        }
    }
}