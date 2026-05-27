// TimeTrackerApp.swift
import SwiftUI

@main
struct TimeTrackerApp: App {
    @StateObject private var timerService = TimerService()
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(timerService)
        }
    }
}