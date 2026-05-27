import SwiftUI

struct ContentView: View {
    @StateObject private var timerService = TimerService()
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Time Tracker")
                .font(.largeTitle)
                .padding()
            
            Text("Timer: \(timerService.elapsedTimeFormatted)")
                .font(.title2)
                
            HStack {
                Button(action: timerService.startTimer) {
                    Text("Start")
                }
                
                Button(action: timerService.stopTimer) {
                    Text("Stop")
                }
                
                Button(action: timerService.resetTimer) {
                    Text("Reset")
                }
            }
            
            List(timerService.projects, id: \Project.id) { project in
                HStack {
                    Text(project.name)
                        .foregroundColor(.primary)
                    Spacer()
                    Text(project.elapsedTimeFormatted)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding()
    }
}