import SwiftUI

struct SettingsView: View {
    var body: some View {
        Form {
            Section(header: Text("Jira Integration"))
            TextField("Base URL", text: $jiraUrl)
            TextField("Username", text: $username)
            SecureField("API Key", text: $apiKey)
        }
    }
}
