import time
import unittest
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.viewmodel import TimeTrackerViewModel


class TestAC7BackgroundSuspension(unittest.TestCase):
    def test_timer_pauses_on_background(self):
        vm = TimeTrackerViewModel()
        with patch('time.time', return_value=1000.0):
            vm.start_timer()
        with patch('time.time', return_value=1005.0):
            vm.will_suspension_handler()
        self.assertEqual(vm.is_timer_running, False)
        self.assertEqual(vm.timer_elapsed, 5.0)
        self.assertTrue(vm.is_suspended)

    def test_timer_resumes_on_foreground_if_running_before(self):
        vm = TimeTrackerViewModel()
        with patch('time.time', return_value=1000.0):
            vm.start_timer()
        with patch('time.time', return_value=1005.0):
            vm.will_suspension_handler()
        with patch('time.time', return_value=1005.0):
            vm.did_activation_handler()
        self.assertEqual(vm.is_timer_running, True)
        self.assertEqual(vm.timer_start, 1005.0)

    def test_timer_does_not_resume_if_manually_paused_before_suspension(self):
        vm = TimeTrackerViewModel()
        with patch('time.time', return_value=1000.0):
            vm.start_timer()
        with patch('time.time', return_value=1003.0):
            vm.pause_timer()
        with patch('time.time', return_value=1003.0):
            vm.will_suspension_handler()
        with patch('time.time', return_value=1003.0):
            vm.did_activation_handler()
        self.assertEqual(vm.is_timer_running, False)

    def test_timer_does_not_resume_if_stopped_before_suspension(self):
        vm = TimeTrackerViewModel()
        with patch('time.time', return_value=1000.0):
            vm.start_timer()
        with patch('time.time', return_value=1005.0):
            vm.stop_timer()
        with patch('time.time', return_value=1005.0):
            vm.will_suspension_handler()
        with patch('time.time', return_value=1005.0):
            vm.did_activation_handler()
        self.assertEqual(vm.is_timer_running, False)
