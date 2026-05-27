// SettingsView.swift
import SwiftUI

class SettingsManager: ObservableObject {
    @Published var jiraBaseUrl: String = ""
    @Published var jiraUsername: String = ""
    @Published var jiraApiKey: String = ""
    
    func saveSettings() {
        // In a real app, this would securely store credentials
        print("Saving settings: \(jiraBaseUrl), \(jiraUsername)")
    }
}

struct SettingsView: View {
    @StateObject private var settings = SettingsManager()
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Jira Configuration")) {
                    TextField("Base URL", text: $settings.jiraBaseUrl)
                    TextField("Username", text: $settings.jiraUsername)
                    SecureField("API Key", text: $settings.jiraApiKey)
                }
                
                Button("Save Settings") {
                    settings.saveSettings()
                }
            }
            .navigationTitle("Settings")
        }
    }
}