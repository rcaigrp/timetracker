class SecureStorage:
    _credentials = None

    @staticmethod
    def save_credentials(base_url, username, api_key):
        """Saves Jira credentials securely (simulated in-memory for PythonKit integration)."""
        SecureStorage._credentials = {
            "base_url": base_url,
            "username": username,
            "api_key": api_key
        }

    @staticmethod
    def get_credentials():
        """Retrieves stored credentials."""
        return SecureStorage._credentials

    @staticmethod
    def has_credentials():
        """Returns True if credentials are configured."""
        return SecureStorage._credentials is not None
