// Dashboard View
import SwiftUI

class TimeTrackerViewModel: ObservableObject {
    @Published var timerIsRunning = false
    @Published var elapsedTime = 0
    @Published var projects: [Project] = []
    
    func startTimer() {
        timerIsRunning = true
    }
    
    func stopTimer() {
        timerIsRunning = false
    }
}

struct DashboardView: View {
    @StateObject private var viewModel = TimeTrackerViewModel()
    
    var body: some View {
        VStack {
            Text("Time Tracker Dashboard")
                .font(.largeTitle)
            
            TimerView(viewModel: viewModel)
            
            Button(action: {
                if viewModel.timerIsRunning {
                    viewModel.stopTimer()
                } else {
                    viewModel.startTimer()
                }
            }) {
                Text(viewModel.timerIsRunning ? "Stop" : "Start")
            }
        }
        .padding()
    }
}

struct DashboardView_Previews: PreviewProvider {
    static var previews: some View {
        DashboardView()
    }
}