// TimeTrackerApp.swift
// This file defines the main SwiftUI application structure

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
