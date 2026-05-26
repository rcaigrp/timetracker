import Foundation
import FoundationNetworking

class JiraService {
    var baseURL: String
    var username: String
    var apiKey: String
    
    init(baseURL: String, username: String, apiKey: String) {
        self.baseURL = baseURL
        self.username = username
        self.apiKey = apiKey
    }
    
    func fetchProjects() async throws -> [String] {
        guard let url = URL(string: "\(baseURL)/rest/api/1/project") else {
            throw URLError(.badURL)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        
        let credential = URLCredential(user: username, password: apiKey, authenticationMethod: .native)
        let session = URLSession(configuration: URLSessionConfiguration.default)
        
        let (data, response) = try await session.data(for: request)
        
        if let httpResponse = response as? HTTPURLResponse, (200...299).contains(httpResponse.statusCode) {
            return ["Project 1", "Project 2"]
        }
        throw URLError(.badServerResponse)
    }
}