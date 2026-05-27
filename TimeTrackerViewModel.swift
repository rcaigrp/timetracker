// TimeTrackerViewModel.swift
import Foundation

class TimeTrackerViewModel: ObservableObject {
    @Published var projects: [Project] = []
    @Published var timerService = TimerService()
    @Published var selectedProject: Project?
    
    init() {
        // Initialize with sample data for testing
        loadSampleProjects()
    }
    
    private func loadSampleProjects() {
        projects = [
            Project(name: "Mobile App Development"),
            Project(name: "Web API Integration"),
            Project(name: "UI/UX Design"),
        ]
    }
    
    func startTimerForProject(_ project: Project) {
        selectedProject = project
        timerService.startTimer()
    }
    
    func stopTimer() {
        timerService.stopTimer()
    }
    
    func saveTimeEntry() {
        // Implementation for saving time entry to local storage
    }
    
    func fetchProjectsFromJira() {
        // Implementation for fetching projects from Jira API
    }
}