// TimeTracker main entry point
import Foundation
import TimeTrackerLib

func run() {
    let taskManager = TaskManager()
    
    // Simple CLI interface for time tracking
    print("TimeTracker CLI")
    
    // For demo purposes, we'll create a simple command parser
    // In a real app this would be more robust
    let args = CommandLine.arguments
    
    if args.count < 2 {
        print("Usage: start \"task name\", stop \"task name\", list")
        return
    }
    
    let command = args[1]
    
    switch command {
    case "start":
        if args.count < 3 {
            print("Usage: start \"task name\"")
            return
        }
        let taskName = args[2...].joined(separator: " ")
        if taskManager.startTask(taskName) {
            print("Started task: \(taskName)")
        } else {
            print("Failed to start task: \(taskName). Task may already be running.")
        }
    case "stop":
        if args.count < 3 {
            print("Usage: stop \"task name\"")
            return
        }
        let taskName = args[2...].joined(separator: " ")
        if taskManager.stopTask(taskName) {
            print("Stopped task: \(taskName)")
        } else {
            print("Failed to stop task: \(taskName). Task not found or not running.")
        }
    case "list":
        let tasks = taskManager.listTasks()
        if tasks.isEmpty {
            print("No tasks recorded.")
        } else {
            print("Tasks:")
            for task in tasks {
                let duration: String
                if let endTime = task.endTime {
                    let interval = endTime.timeIntervalSince(task.startTime)
                    duration = "\(Int(interval)) seconds"
                } else {
                    duration = "Running..."
                }
                print("- \(task.name): \(duration)")
            }
        }
    default:
        print("Unknown command: \(command)")
        print("Usage: start \"task name\", stop \"task name\", list")
    }
}

run()
