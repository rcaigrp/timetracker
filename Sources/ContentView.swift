import SwiftUI

class TimerService: ObservableObject {
    @Published var isRunning = false
    @Published var elapsedTime: TimeInterval = 0
    private var timer: Timer?
    private var startTime: Date?
    
    func start() {
        guard !isRunning else { return }
        isRunning = true
        startTime = Date()
        
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            if let startTime = self.startTime {
                self.elapsedTime = Date().timeIntervalSince(startTime)
            }
        }
    }
    
    func stop() {
        isRunning = false
        timer?.invalidate()
        timer = nil
    }
    
    func reset() {
        stop()
        elapsedTime = 0
    }
}

struct ContentView: View {
    @StateObject private var timerService = TimerService()
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Time Tracker")
                .font(.largeTitle)
                
            Text("Elapsed Time: \(String(format: "%02d:%02d:%02d", Int(timerService.elapsedTime) / 3600, (Int(timerService.elapsedTime) % 3600) / 60, Int(timerService.elapsedTime) % 60))")
                .font(.title2)
                
            HStack {
                Button(action: timerService.start) {
                    Text("Start")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                Button(action: timerService.stop) {
                    Text("Stop")
                        .padding()
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                Button(action: timerService.reset) {
                    Text("Reset")
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
            }
        }
        .padding()
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}