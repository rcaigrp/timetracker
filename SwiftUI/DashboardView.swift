import SwiftUI

struct DashboardView: View {
    @State private var entries: [Entry] = []
    @State private var showingTimer = false

    var body: some View {
        NavigationView {
            List(entries) { entry in
                Text(entry.project)
            }
            .navigationTitle("Projects")
            .toolbar {
                Button("Start Timer") {
                    showingTimer = true
                }
            }
        }
        .sheet(isPresented: $showingTimer) {
            TimerView()
        }
    }
}
