import SwiftUI

struct DashboardView: View {
    @State private var entries: [String] = []
    @State private var showTimer = false
    
    var body: some View {
        NavigationStack {
            List(entries) { entry in
                Text(entry)
            }
            .navigationTitle("Projects")
            .toolbar {
                Button("Start Timer") {
                    showTimer = true
                }
            }
        }
        .sheet(isPresented: $showTimer) {
            TimerView()
        }
    }
}