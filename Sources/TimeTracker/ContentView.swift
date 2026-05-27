import SwiftUI

struct ContentView: View {
    @StateObject private var timerService = TimerService.shared
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Time Tracker")
                .font(.largeTitle)
                .padding()
            
            Text(formatTime(timerService.elapsedTime))
                .font(.system(size: 48, weight: .bold))
                .padding()
            
            Button(action: {
                if timerService.isRunning {
                    timerService.stop()
                } else {
                    timerService.start()
                }
            }) {
                Text(timerService.isRunning ? "Stop Timer" : "Start Timer")
                    .font(.title2)
                    .padding()
                    .background(timerService.isRunning ? Color.red : Color.green)
                    .foregroundColor(.white)
                    .cornerRadius(10)
            }
            
            List {
                ForEach(timerService.projects, id: \Project.id) { project in
                    HStack {
                        Text(project.name)
                        Spacer()
                        Text(formatTime(project.totalTime))
                    }
                }
            }
        }
        .padding()
    }
    
    private func formatTime(_ timeInterval: TimeInterval) -> String {
        let hours = Int(timeInterval) / 3600
        let minutes = Int(timeInterval) / 60 % 60
        let seconds = Int(timeInterval) % 60
        return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}