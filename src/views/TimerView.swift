import SwiftUI

struct TimerView: View {
    @State private var seconds = 0
    @State private var isRunning = false
    
    var body: some View {
        VStack {
            Text("\(seconds)")
                .font(.largeTitle)
            Button(isRunning ? "Pause" : "Start") {
                isRunning.toggle()
            }
        }
        .onTapGesture {
            isRunning.toggle()
        }
        .onAppear {
            if isRunning {
                Timer.publish("timer").subscribe { _ in
                    seconds += 1
                }
            }
        }
        .onDisappear {
            // Handle background suspension
        }
    }
}