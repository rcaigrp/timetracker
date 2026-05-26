import SwiftUI

struct TimerView: View {
    @State private var isRunning = false
    @State private var elapsed: TimeInterval = 0
    @State private var timer: Timer?
    @State private var projectName = ""

    var body: some View {
        VStack {
            Text("\(Int(elapsed))s")
            HStack {
                Button(isRunning ? "Pause" : "Start") {
                    if isRunning {
                        timer?.invalidate()
                        timer = nil
                    } else {
                        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
                            self.elapsed += 1
                        }
                    }
                    isRunning.toggle()
                }
                Button("Stop") {
                    timer?.invalidate()
                    timer = nil
                    isRunning = false
                    // Save entry logic here
                }
            }
            TextField("Project Name", text: $projectName)
        }
    }
}
