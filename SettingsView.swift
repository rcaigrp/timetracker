import SwiftUI

struct SettingsView: View {
    @AppStorage("api_key") private var apiKey: String = ""
    
    var body: some View {
        Form {
            SecureField("API Key", text: $apiKey)
        }
    }
}
