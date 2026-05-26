import SwiftUI

struct SettingsView: View {
    @Environment(\.dismiss) var dismiss
    @State private var jiraUrl = ""
    @State private var username = ""
    @State private var apiKey = ""
    
    var body: some View {
        Form {
            Section(header: Text("Jira Configuration")) {
                TextField("Base URL", text: $jiraUrl)
                TextField("Username", text: $username)
                SecureField("API Key", text: $apiKey)
            }
            Button("Save") {
                dismiss()
            }
        }
        .padding()
    }
}