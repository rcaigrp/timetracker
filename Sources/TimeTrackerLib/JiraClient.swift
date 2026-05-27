//
// JiraClient.swift
// TimeTracker
//

import Foundation

public class JiraClient {
    private let baseURL: String
    private let username: String
    private let apiKey: String
    
    public init(baseURL: String, username: String, apiKey: String) {
        self.baseURL = baseURL
        self.username = username
        self.apiKey = apiKey
    }
    
    public func fetchProjects() async throws -> [Project] {
        // Mock implementation
        return []
    }
}
