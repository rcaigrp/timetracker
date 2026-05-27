import SwiftUI

class SettingsViewModel: ObservableObject {
    @Published var jiraBaseURL = ""
    @Published var jiraUsername = ""
    @Published var jiraAPIKey = ""
    
    func saveCredentials() {
        // Mock implementation - will be replaced with secure storage
    }
}

struct SettingsView: View {
    @StateObject private var settingsVM = SettingsViewModel()
    
    var body: some View {
        Form {
            Section(header: Text("Jira Configuration")) {
                TextField("Base URL", text: $settingsVM.jiraBaseURL)
                    .autocapitalization(.none)
                
                TextField("Username", text: $settingsVM.jiraUsername)
                    .autocapitalization(.none)
                
                SecureField("API Key", text: $settingsVM.jiraAPIKey)
            }
            
            Section {
                Button(action: settingsVM.saveCredentials) {
                    Text("Save Settings")
                }
            }
        }
        .navigationTitle("Settings")
    }
}

struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
    }
}