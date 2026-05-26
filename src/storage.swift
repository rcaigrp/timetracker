import Foundation

class Storage {
    static let shared = Storage()
    private let fileManager = FileManager.default
    private let fileName = "time_entries.json"
    
    private var filePath: String {
        let paths = fileManager.urls(for: .documentDirectory, in: .userDomainMask)
        return paths[0].path + "/" + fileName
    }
    
    func saveEntries(_ entries: [String]) {
        if let data = try? JSONSerialization.data(withJSONObject: entries, options: .prettyPrinted) {
            try? data.write(to: URL(fileURLWithPath: filePath), options: .atomic)
        }
    }
    
    func loadEntries() -> [String] {
        if let data = try? Data(contentsOf: URL(fileURLWithPath: filePath)) {
            do {
                if let entries = try JSONSerialization.jsonObject(with: data, options: []) as? [String] {
                    return entries
                }
            } catch {
                print("Error loading entries: \(error)")
            }
        }
        return []
    }
}