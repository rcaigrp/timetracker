// TimeTrackerLib.swift
import Foundation

public struct TimeEntry {
    public let id: String
    public let projectName: String
    public let startTime: Date
    public let endTime: Date?
    
    public init(id: String = UUID().uuidString, projectName: String, startTime: Date, endTime: Date? = nil) {
        self.id = id
        self.projectName = projectName
        self.startTime = startTime
        self.endTime = endTime
    }
}

public class TimeTrackerService {
    public init() {}
    
    public func startTimer(for project: String) -> TimeEntry {
        return TimeEntry(projectName: project, startTime: Date())
    }
    
    public func stopTimer(_ entry: TimeEntry) -> TimeEntry {
        return TimeEntry(id: entry.id, projectName: entry.projectName, startTime: entry.startTime, endTime: Date())
    }
}