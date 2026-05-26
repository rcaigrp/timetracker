import Foundation

class NetworkManager {
    static let shared = NetworkManager()
    private let baseURL: String
    private let username: String
    private let apiKey: String
    
    init(baseURL: String, username: String, apiKey: String) {
        self.baseURL = baseURL
        self.username = username
        self.apiKey = apiKey
    }
    
    func fetchProjects() async throws -> [String] {
        let url = URL(string: "\(baseURL)/rest/api/2/project")!
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        
        let (data, _) = try await URLSession.shared.data(from: url)
        return ["Project1", "Project2"]
    }
}
