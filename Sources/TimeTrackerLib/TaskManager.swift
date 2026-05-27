import Foundation

class Task {
    let name: String
    let startTime: Date
    var endTime: Date?
    
    init(name: String, startTime: Date = Date()) {
        self.name = name
        self.startTime = startTime
    }
}

class TaskManager {
    private var tasks: [Task] = []
    
    func startTask(_ name: String) -> Bool {
        // Check if task with same name is already running
        let isRunning = tasks.contains { $0.endTime == nil && $0.name == name }
        
        if !isRunning {
            let newTask = Task(name: name)
            tasks.append(newTask)
            return true
        }
        return false
    }
    
    func stopTask(_ name: String) -> Bool {
        guard let index = tasks.firstIndex(where: { $0.name == name && $0.endTime == nil }) else {
            return false
        }
        
        tasks[index].endTime = Date()
        return true
    }
    
    func listTasks() -> [Task] {
        return tasks
    }
    
    func getRunningTask() -> Task? {
        return tasks.first { $0.endTime == nil }
    }
}
