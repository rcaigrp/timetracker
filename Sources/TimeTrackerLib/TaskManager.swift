import Foundation

class TaskManager {
    private var tasks: [Task] = []
    
    func addTask(_ task: Task) {
        tasks.append(task)
    }
    
    func getTasks() -> [Task] {
        return tasks
    }
    
    func startTask(_ taskId: UUID) -> Bool {
        guard let index = tasks.firstIndex(where: { $0.id == taskId }) else {
            return false
        }
        tasks[index].startTime = Date()
        tasks[index].isRunning = true
        return true
    }
    
    func stopTask(_ taskId: UUID) -> Bool {
        guard let index = tasks.firstIndex(where: { $0.id == taskId }) else {
            return false
        }
        tasks[index].stopTime = Date()
        tasks[index].isRunning = false
        return true
    }
}

class Task: Codable {
    public let id: UUID
    public var name: String
    public var description: String?
    public var startTime: Date?
    public var stopTime: Date?
    public var isRunning: Bool = false
    
    init(id: UUID = UUID(), name: String, description: String? = nil) {
        self.id = id
        self.name = name
        self.description = description
    }
}