// JiraClient.swift
import Foundation

class Project: Identifiable, Codable {
    let id = UUID()
    let key: String
    let name: String
    
    init(key: String, name: String) {
        self.key = key
        self.name = name
    }
}

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
        // Mock implementation for now - will be replaced with real API calls
        DispatchQueue.main.async {
            self.projects = [
                Project(key: "PROJ-1", name: "Project Alpha"),
                Project(key: "PROJ-2", name: "Project Beta")
            ]
            completion(.success(self.projects))
        }
    }
}