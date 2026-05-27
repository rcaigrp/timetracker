// Jira Client
import Foundation

class JiraClient {
    private let baseURL: String
    private let username: String
    private let apiToken: String
    
    init(baseURL: String, username: String, apiToken: String) {
        self.baseURL = baseURL
        self.username = username
        self.apiToken = apiToken
    }
    
    func fetchProjects(completion: @escaping (Result<[Project], Error>) -> Void) {
        // Mock implementation for now
        let mockProjects = [
            Project(name: "Project A"),
            Project(name: "Project B")
        ]
        completion(.success(mockProjects))
    }
}