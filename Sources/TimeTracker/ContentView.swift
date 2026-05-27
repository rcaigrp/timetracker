// ContentView.swift
import SwiftUI

struct ContentView: View {
    @StateObject private var timerService = TimerService()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Timer display
                Text("\(timerService.elapsedTimeString)")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .padding()
                
                // Timer controls
                HStack(spacing: 20) {
                    Button(action: timerService.startTimer) {
                        Text("Start")
                            .frame(minWidth: 80)
                    }
                    .disabled(timerService.isRunning)
                    
                    Button(action: timerService.stopTimer) {
                        Text("Stop")
                            .frame(minWidth: 80)
                    }
                    .disabled(!timerService.isRunning)
                    
                    Button(action: timerService.resetTimer) {
                        Text("Reset")
                            .frame(minWidth: 80)
                    }
                }
                
                // Project list
                List(timerService.projects, id: \Project.id) { project in
                    HStack {
                        VStack(alignment: .leading) {
                            Text(project.name)
                                .font(.headline)
                            Text("\(project.elapsedTimeString)")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                    }
                }
            }
            .navigationTitle("Time Tracker")
            .navigationBarTitleDisplayMode(.large)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
