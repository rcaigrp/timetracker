import Foundation
import Combine

class TimerService: ObservableObject {
    static let shared = TimerService()
    
    @Published var elapsedTime: TimeInterval = 0
    @Published var isRunning: Bool = false
    @Published var projects: [Project] = []
    
    private var timer: Timer?
    private var startTime: Date?
    private let persistenceKey = "TimeTrackerData"
    
    private init() {
        loadFromPersistence()
    }
    
    func start() {
        guard !isRunning else { return }
        
        isRunning = true
        startTime = Date()
        
        timer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { _ in
            self.updateElapsedTime()
        }
    }
    
    func stop() {
        guard isRunning else { return }
        
        isRunning = false
        timer?.invalidate()
        timer = nil
        
        saveToPersistence()
    }
    
    private func updateElapsedTime() {
        guard let startTime = startTime else { return }
        elapsedTime = Date().timeIntervalSince(startTime)
    }
    
    private func saveToPersistence() {
        let data = TimeTrackerData(elapsedTime: elapsedTime, isRunning: isRunning, projects: projects)
        if let encoded = try? JSONEncoder().encode(data) {
            UserDefaults.standard.set(encoded, forKey: persistenceKey)
        }
    }
    
    private func loadFromPersistence() {
        guard let data = UserDefaults.standard.data(forKey: persistenceKey),
              let decoded = try? JSONDecoder().decode(TimeTrackerData.self, from: data) else { return }
        
        elapsedTime = decoded.elapsedTime
        isRunning = decoded.isRunning
        projects = decoded.projects
        
        if isRunning {
            start()
        }
    }
}

struct TimeTrackerData: Codable {
    let elapsedTime: TimeInterval
    let isRunning: Bool
    let projects: [Project]
}