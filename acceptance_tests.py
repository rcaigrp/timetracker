import unittest
from unittest.mock import patch, MagicMock
from Sources.TimeTrackerLib.TaskManager import TaskManager


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.task_manager = TaskManager()
    
    def test_criterion_1_start_task_successfully(self):
        # Mock the Date() call to return a fixed time for testing
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0)
            result = self.task_manager.startTask("Test Task")
            self.assertTrue(result)
            
    def test_criterion_2_stop_task_successfully(self):
        # First start a task
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0)
            self.task_manager.startTask("Test Task")
            
            # Then stop it
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 5, 0)
            result = self.task_manager.stopTask("Test Task")
            self.assertTrue(result)
            
    def test_criterion_3_list_tasks_returns_correctly(self):
        # Test that listTasks returns the correct number of tasks
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0)
            self.task_manager.startTask("Test Task 1")
            self.task_manager.startTask("Test Task 2")
            
            tasks = self.task_manager.listTasks()
            self.assertEqual(len(tasks), 2)
            
    def test_criterion_4_prevent_duplicate_running_tasks(self):
        # Test that we can't start a task that's already running
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 1, 1, 10, 0, 0)
            self.task_manager.startTask("Test Task")
            
            # Try to start the same task again
            result = self.task_manager.startTask("Test Task")
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
