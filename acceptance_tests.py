import os
import pytest

class TestSwiftFiles:
    def test_time_entry_exists(self):
        path = "/workspace/projects/TimeTracker/TimeEntry.swift"
        assert os.path.exists(path)
        with open(path) as f:
            content = f.read()
        assert "@Model" in content
        assert "class TimeEntry" in content

    def test_timer_view_model_exists(self):
        path = "/workspace/projects/TimeTracker/TimerViewModel.swift"
        assert os.path.exists(path)
        with open(path) as f:
            content = f.read()
        assert "class TimerViewModel" in content
        assert "func startTimer" in content
        assert "func stopTimer" in content

    def test_dashboard_view_exists(self):
        path = "/workspace/projects/TimeTracker/DashboardView.swift"
        assert os.path.exists(path)
        with open(path) as f:
            content = f.read()
        assert "struct DashboardView" in content
        assert "TimerDisplayView" in content
        assert "EntryListView" in content

    def test_timer_logic_simulation(self):
        import time
        
        class MockTimer:
            def __init__(self):
                self.start_time = None
                self.duration = 0
                self.is_running = False
            
            def start(self):
                self.start_time = time.time()
                self.is_running = True
            
            def stop(self):
                if self.start_time:
                    self.duration = time.time() - self.start_time
                    self.is_running = False
                    self.start_time = None
        
        timer = MockTimer()
        timer.start()
        time.sleep(0.1)
        timer.stop()
        
        assert timer.duration >= 0.09, "Duration should be at least 90ms"
        assert not timer.is_running, "Timer should be stopped"
