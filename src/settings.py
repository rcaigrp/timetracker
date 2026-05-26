class SettingsViewModel:
    def __init__(self):
        self.base_url = ""
        self.username = ""
        self.api_key = ""

    def set_credentials(self, base_url, username, api_key):
        self.base_url = base_url
        self.username = username
        self.api_key = api_key
