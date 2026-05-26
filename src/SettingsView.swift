import SwiftUI
import PythonBridge

struct SettingsView: View {
    @State private var base_url = ""
    @State private var username = ""
    @State private var api_key = ""
    
    var body: some View {
        Form {
            Section {
                TextField("Jira Base URL", text: $base_url)
                TextField("Username", text: $username)
                SecureField("API Key", text: $api_key)
            }
            Button("Save Configuration") {
                PythonBridge.saveSettings(base_url: base_url, username: username, api_key: api_key)
            }
        }
    }
}
