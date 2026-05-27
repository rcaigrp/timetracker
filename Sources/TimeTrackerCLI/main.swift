import Foundation
import TimeTrackerLib

print("Time Tracker CLI initialized")

// Create a sample task manager
let taskManager = TaskManager()
let project = Project(name: "Sample Project")
let task = Task(name: "Sample Task", description: "A sample task")

taskManager.addTask(task)
print("Added task: \(task.name)")

// Print all tasks
let tasks = taskManager.getTasks()
for task in tasks {
    print("Task: \(task.name) - Running: \(task.isRunning)")
}