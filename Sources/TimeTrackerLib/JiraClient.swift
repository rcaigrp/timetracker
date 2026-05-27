import Foundation

class JiraClient {
    private let baseUrl: String
    private let username: String
    private let apiToken: String
    
    init(baseUrl: String, username: String, apiToken: String) {
        self.baseUrl = baseUrl
        self.username = username
        self.apiToken = apiToken
    }
    
    func fetchIssues(for projectKey: String) async throws -> [Issue] {
        // Mock implementation
        return []
    }
    
    struct Issue: Codable {
        let id: String
        let key: String
        let summary: String
        let status: String
    }
}