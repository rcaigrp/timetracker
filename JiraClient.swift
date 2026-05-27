// JiraClient.swift
import Foundation

class JiraClient: ObservableObject {
    @Published var projects: [Project] = []
    private var baseUrl: String = ""
    private var username: String = ""
    private var apiKey: String = ""
    
    func configure(baseUrl: String, username: String, apiKey: String) {
        self.baseUrl = baseUrl
        self.username = username
        self.apiKey = apiKey
    }
    
    func fetchProjects(completion: @escaping (Result<[Project], Error>) -> Void) {
        guard !baseUrl.isEmpty, !username.isEmpty, !apiKey.isEmpty else {
            completion(.failure(NSError(domain: "ConfigurationError", code: 0, userInfo: [NSLocalizedDescriptionKey: "Jira credentials not configured"])))
            return
        }
        
        let url = URL(string: "\(baseUrl)/rest/api/2/project")!
        var request = URLRequest(url: url)
        request.httpMethod = "GET"
        request.setValue("Basic \(Data("\(username):\(apiKey)".utf8).base64EncodedString())", forHTTPHeaderField: "Authorization")
        
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data else {
                completion(.failure(NSError(domain: "DataError", code: 0, userInfo: [NSLocalizedDescriptionKey: "No data received"])))
                return
            }
            
            do {
                let projects = try JSONDecoder().decode([Project].self, from: data)
                completion(.success(projects))
            } catch {
                completion(.failure(error))
            }
        }
        task.resume()
    }
}