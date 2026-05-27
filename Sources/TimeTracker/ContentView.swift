import SwiftUI

struct ContentView: View {
    @StateObject private var timerService = TimerService()
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Time Tracker")
                .font(.largeTitle)
                
            Text("Elapsed Time: \(String(format: "%.1f", timerService.elapsedTime)) seconds")
                .font(.headline)
                
            HStack(spacing: 20) {
                Button(action: timerService.startTimer) {
                    Text("Start")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                Button(action: timerService.stopTimer) {
                    Text("Stop")
                        .padding()
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                Button(action: timerService.resetTimer) {
                    Text("Reset")
                        .padding()
                        .background(Color.gray)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
            }
        }
        .padding()
    }
}

#Preview {
    ContentView()
}