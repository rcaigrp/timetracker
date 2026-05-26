import SwiftUI

struct TimerView: View {
    @State private var isRunning = false
    @State private var elapsed: TimeInterval = 0
    private var timer: Timer?
    
    var body: some View {
        VStack {
            Text("Elapsed: \(elapsed.formatted(.number.unit(.second)))")
            Button(isRunning ? "Pause" : "Start") {
                if isRunning {
                    timer?.invalidate()
                    timer = nil
                } else {
                    timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
                        elapsed += 1
                    }
                }
                isRunning.toggle()
            }
            .buttonStyle(.borderedProminent)
        }
        .padding()
    }
}