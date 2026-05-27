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
    
    public func fetchProjects() async throws -> [String] {
        // Mock implementation - in real app this would make HTTP calls
        return ["PROJ1", "PROJ2", "PROJ3"]
    }
}