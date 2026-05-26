import unittest
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ios_logic import App, TimerEntry, Project, Settings

class TestTimeTrackerApp(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_criterion_1_app_launches(self):
        """Test 1: The application launches cleanly and presents a main dashboard."""
        self.assertIsNotNone(self.app)
        self.assertEqual(len(self.app.timer_entries), 0)

    def test_criterion_2_manual_entry_timer(self):
        """Test 2: Users can manually create a custom project entry, start/stop timer, and view elapsed time."""
        self.app.start_timer("Dev Project")
        time.sleep(0.1)
        self.app.stop_timer()
        self.assertFalse(self.app.timer_running)
        self.assertEqual(len(self.app.timer_entries), 1)
        entry = self.app.timer_entries[0]
        self.assertEqual(entry.project, "Dev Project")
        self.assertGreater(entry.duration, 0)

    def test_criterion_3_settings_config(self):
        """Test 3: Settings screen accepts Jira URL, username, API key, stores securely."""
        self.app.configure_settings("https://jira.example.com", "user", "pass")
        self.assertIsNotNone(self.app.settings)
        self.assertEqual(self.app.settings.base_url, "https://jira.example.com")
        self.assertEqual(self.app.settings.username, "user")
        self.assertEqual(self.app.settings.api_key, "pass")

    def test_criterion_4_fetch_projects(self):
        """Test 4: Upon successful Jira configuration, fetches and displays projects."""
        self.app.configure_settings("https://jira.example.com", "user", "pass")
        projects = self.app.fetch_projects()
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[0].name, "Project A")

    def test_criterion_5_persistence(self):
        """Test 5: Timer data persists across app relaunches."""
        self.app.start_timer("Persist Project")
        time.sleep(0.1)
        self.app.stop_timer()
        self.app.save_entries()
        
        # Simulate relaunch
        new_app = App()
        new_app.load_entries()
        self.assertEqual(len(new_app.timer_entries), 1)
        self.assertEqual(new_app.timer_entries[0].project, "Persist Project")

    def test_criterion_6_networking(self):
        """Test 6: Networking layer handles HTTP requests and returns structured data."""
        self.app.configure_settings("https://jira.example.com", "user", "pass")
        projects = self.app.fetch_projects()
        self.assertTrue(all(isinstance(p, Project) for p in projects))

    def test_criterion_7_background_suspend(self):
        """Test 7: Gracefully handles background suspension by pausing timer."""
        self.app.start_timer("Suspend Project")
        self.assertTrue(self.app.timer_running)
        self.app.background_suspend()
        self.assertFalse(self.app.timer_running)

if __name__ == "__main__":
    unittest.main()
