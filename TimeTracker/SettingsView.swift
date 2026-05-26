import SwiftUI
import PythonKit

struct SettingsView: View {
    @State private var base_url = ""
    @State private var username = ""
    @State private var api_key = ""

    let storage: Storage = PythonBridge.storage

    var body: some View {
        Form {
            TextField("Base URL", text: $base_url)
            TextField("Username", text: $username)
            SecureField("API Key", text: $api_key)
            
            Button("Save Settings") {
                storage.update_settings(base_url, username, api_key)
            }
        }
        .onAppear {
            let settings = storage.get_settings()
            base_url = settings["base_url"] as! String
            username = settings["username"] as! String
            api_key = settings["api_key"] as! String
        }
    }
}
