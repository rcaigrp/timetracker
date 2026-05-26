import SwiftUI

struct SettingsView: View {
    @State private var baseURL = ""
    @State private var username = ""
    @State private var apiKey = ""
    
    var body: some View {
        Form {
            TextField("Base URL", text: $baseURL)
            TextField("Username", text: $username)
            SecureField("API Key", text: $apiKey)
        }
    }
}