import Foundation

class Entry: ObservableObject {
    @Published var project: String = ""
    @Published var date: String = ""
    @Published var duration: String = "00:00"
    @Published var notes: String = ""
}

class TimerState: ObservableObject {
    @Published var isRunning: Bool = false
    @Published var elapsed: String = "00:00"
    @Published var currentProject: String = ""
}