import SwiftUI

struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @AppStorage("jiraBaseUrl") private var jiraBaseUrl = ""
    @AppStorage("jiraUsername") private var jiraUsername = ""
    @AppStorage("jiraApiKey") private var jiraApiKey = ""
    
    var body: some View {
        Form {
            Section("Jira Configuration") {
                TextField("Base URL", text: $jiraBaseUrl)
                TextField("Username", text: $jiraUsername)
                SecureField("API Key", text: $jiraApiKey)
            }
        }
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                Button("Done") {
                    dismiss()
                }
            }
        }
    }
}
