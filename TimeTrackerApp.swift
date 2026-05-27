// TimeTrackerApp.swift
import SwiftUI

@main
struct TimeTrackerApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var delegate
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(TimerService())
        }
    }
}