// main.swift
import Foundation
import TimeTrackerLib

print("TimeTracker App Started")

let tracker = TimeTrackerService()
let entry = tracker.startTimer(for: "Test Project")
print("Timer started for \(entry.projectName)")

let stoppedEntry = tracker.stopTimer(entry)
print("Timer stopped for \(stoppedEntry.projectName)")