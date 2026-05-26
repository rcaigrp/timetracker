import Foundation
import PythonKit

@MainActor
struct PythonBridge {
    static func saveEntry(duration: TimeInterval) {
        let py = Python("python")
        let storage = py.import("src.storage")
        let store = storage.Storage()
        store.addEntry(project: "DevProject", duration: duration, notes: "")
    }
    
    static func saveSettings(base_url: String, username: String, api_key: String) {
        let py = Python("python")
        let storage = py.import("src.storage")
        let store = storage.Storage()
        store.updateSettings(base_url: base_url, username: username, api_key: api_key)
    }
    
    static func loadProjects(completion: @escaping ([String]) -> Void) {
        let py = Python("python")
        let storage = py.import("src.storage")
        let store = storage.Storage()
        let entries = store.getEntries()
        let names: [String] = entries.map { $["project"] as! String }
        completion(names)
    }
}
