// TimeTrackerApp.swift
import SwiftUI

@main
struct TimeTrackerApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @StateObject private var timerService = TimerService()
    
    var body: some View {
        VStack {
            Text("Time Tracker")
                .font(.largeTitle)
            
            Text("Elapsed Time: \(timerService.elapsedTime, specifier: "%.1f") seconds")
                .font(.headline)
            
            HStack {
                Button(action: timerService.startTimer) {
                    Text("Start")
                }
                .disabled(timerService.isRunning)
                
                Button(action: timerService.stopTimer) {
                    Text("Stop")
                }
                .disabled(!timerService.isRunning)
                
                Button(action: timerService.resetTimer) {
                    Text("Reset")
                }
            }
        }
        .padding()
    }
}

struct SettingsView: View {
    @State private var jiraBaseUrl = ""
    @State private var username = ""
    @State private var apiKey = ""
    
    var body: some View {
        Form {
            Section(header: Text("Jira Configuration")) {
                TextField("Jira Base URL", text: $jiraBaseUrl)
                TextField("Username", text: $username)
                SecureField("API Key", text: $apiKey)
            }
        }
        .navigationTitle("Settings")
    }
}