import Foundation
import PythonKit

class PythonBridge {
    static let shared = PythonBridge()
    
    func callPython(module: String, function: String, args: [Any] = []) -> Any {
        let moduleImport = "import " + module
        let funcCall = module + "." + function
        
        // Construct the Python script
        var script = moduleImport + "\n"
        if !args.isEmpty {
            let argStr = args.map { "\"\(\$0)\"" }.joined(separator: ", ")
            script += "result = " + funcCall + "(" + argStr + ")"
        } else {
            script += "result = " + funcCall + "()"
        }
        script += "\nresult"
        
        // Execute and return
        return Python.run(script)
    }
    
    // Storage Methods
    func saveEntry(project: String, date: String, duration: String, notes: String) {
        callPython(module: "storage", function: "save_entry", args: [project, date, duration, notes])
    }
    
    func getEntries() -> Any {
        return callPython(module: "storage", function: "get_entries")
    }
    
    func clearEntries() {
        callPython(module: "storage", function: "clear_entries")
    }
    
    // Timer Methods
    func startTimer(project: String) {
        callPython(module: "storage", function: "start_timer", args: [project])
    }
    
    func stopTimer() {
        callPython(module: "storage", function: "stop_timer")
    }
    
    func pauseTimer() {
        callPython(module: "storage", function: "pause_timer")
    }
    
    func resumeTimer() {
        callPython(module: "storage", function: "resume_timer")
    }
    
    func getElapsed() -> String {
        return callPython(module: "storage", function: "get_elapsed") as? String ?? "00:00"
    }
    
    // Jira Methods
    func fetchJiraProjects() -> Any {
        return callPython(module: "networking", function: "fetch_projects")
    }
    
    func setJiraConfig(url: String, username: String, apiKey: String) {
        callPython(module: "networking", function: "set_config", args: [url, username, apiKey])
    }
}