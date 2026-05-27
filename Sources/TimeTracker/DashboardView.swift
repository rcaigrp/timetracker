import SwiftUI

class TimerViewModel: ObservableObject {
    @Published var isRunning = false
    @Published var elapsedTime = 0
    
    private var timer: Timer?
    
    func startTimer() {
        isRunning = true
        timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { _ in
            elapsedTime += 1
        }
    }
    
    func stopTimer() {
        isRunning = false
        timer?.invalidate()
        timer = nil
    }
    
    func resetTimer() {
        stopTimer()
        elapsedTime = 0
    }
}

struct DashboardView: View {
    @StateObject private var viewModel = TimerViewModel()
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Time Tracker")
                .font(.largeTitle)
                
            Text("Elapsed Time: \(viewModel.elapsedTime)s")
                .font(.title2)
                
            HStack(spacing: 20) {
                Button(action: viewModel.startTimer) {
                    Text("Start")
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                Button(action: viewModel.stopTimer) {
                    Text("Stop")
                        .padding()
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                Button(action: viewModel.resetTimer) {
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
    DashboardView()
}