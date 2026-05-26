import SwiftUI

struct TimerView: View {
    @ObservedObject var timerState: TimerState
    @ObservedObject var pythonBridge: PythonBridge
    
    var body: some View {
        VStack {
            Text(timerState.elapsed)
                .font(.system(size: 64, weight: .bold))
                .foregroundColor(.primary)
            
            HStack {
                Button(action: {
                    if !timerState.isRunning {
                        pythonBridge.startTimer(project: timerState.currentProject)
                        timerState.isRunning = true
                    }
                }) {
                    Text("Start")
                        .padding()
                }
                
                Button(action: {
                    pythonBridge.stopTimer()
                    timerState.isRunning = false
                }) {
                    Text("Stop")
                        .padding()
                }
            }
        }
    }
}