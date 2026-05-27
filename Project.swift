// Project.swift
import Foundation

struct Project: Codable, Identifiable {
    let id = UUID()
    let key: String
    let name: String
    
    enum CodingKeys: String, CodingKey {
        case key
        case name
    }
}

// Simple local storage for time logs
struct TimeLog: Codable {
    let id = UUID()
    let projectId: String
    let projectName: String
    let startTime: Date
    let endTime: Date?
    
    var duration: TimeInterval {
        guard let endTime = endTime else { return 0 }
        return endTime.timeIntervalSince(startTime)
    }
}