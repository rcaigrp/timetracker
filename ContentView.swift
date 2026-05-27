// ContentView.swift
// Main dashboard view with timer and project list

import SwiftUI

struct ContentView: View {
    @EnvironmentObject private var timerService: TimerService
    
    var body: some View {
        NavigationView {
            VStack {
                // Timer display
                HStack {
                    Text("Timer")
                        .font(.headline)
                    Spacer()
                    Text(timerService.elapsedTimeString)
                        .font(.title2)
                        .bold()
                }
                .padding()
                
                // Start/Stop button
                Button(action: {
                    if timerService.isRunning {
                        timerService.stopTimer()
                    } else {
                        timerService.startTimer()
                    }
                }) {
                    Text(timerService.isRunning ? "Stop" : "Start")
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(timerService.isRunning ? Color.red : Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                .padding(.horizontal)
                
                // Project list
                List {
                    ForEach(timerService.projects) { project in
                        HStack {
                            Text(project.name)
                            Spacer()
                            Text(project.elapsedTimeString)
                        }
                    }
                }
                .listStyle(PlainListStyle())
            }
            .navigationTitle("Time Tracker")
        }
    }
}
