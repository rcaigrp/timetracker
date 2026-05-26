import SwiftUI

struct TimerView: View {
    @State private var isRunning = false
    @State private var startTime: Date?
    @State private var elapsed: TimeInterval = 0
    
    var body: some View {
        VStack {
            Text(isRunning ? "Running..." : "Stopped")
            Button(isRunning ? "Stop" : "Start") {
                if isRunning {
                    // Stop logic
                    isRunning = false
                } else {
                    // Start logic
                    isRunning = true
                    startTime = Date()
                }
            }
        }
    }
}
