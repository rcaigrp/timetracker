import Foundation

protocol JiraClientProtocol {
    func fetchProjects(completion: @escaping (Result<[String], Error>) -> Void)
    func fetchIssues(completion: @escaping (Result<[String], Error>) -> Void)
}

class JiraClient: JiraClientProtocol {
    var baseURL: String
    var username: String
    var apiKey: String
    
    init(baseURL: String, username: String, apiKey: String) {
        self.baseURL = baseURL
        self.username = username
        self.apiKey = apiKey
    }
    
    func fetchProjects(completion: @escaping (Result<[String], Error>) -> Void) {
        let url = URL(string: "\(baseURL)/rest/api/2/project")!
        // In real Swift, use URLSession
        // For architecture, we define the contract
        // Mocked here for Swift preview simulation
        completion(.success([]))
    }
    
    func fetchIssues(completion: @escaping (Result<[String], Error>) -> Void) {
        completion(.success([]))
    }
}
