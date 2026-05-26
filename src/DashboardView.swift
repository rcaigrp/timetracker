import SwiftUI
import TimerService
import PythonBridge

struct DashboardView: View {
    @State private var timerService = TimerService()
    @State private var projects: [String] = []
    
    var body: some View {
        VStack {
            TimerView(service: timerService)
            List(projects, id: \.self) { project in
                Text(project)
            }
            .onAppear {
                PythonBridge.loadProjects { data in
                    projects = data
                }
            }
        }
    }
}

struct TimerView: View {
    @ObservedObject var service: TimerService
    var body: some View {
        VStack {
            Text(service.elapsedTimeFormatted)
            HStack {
                Button(action: service.start) { Text("Start") }
                Button(action: service.pause) { Text("Pause") }
                Button(action: service.stop) { Text("Stop") }
            }
        }
    }
}
