import time
from unittest.mock import patch
from timer_app import TimerService

def test_timer_initialization():
    timer = TimerService()
    assert timer.get_elapsed_time() == 0
    assert not timer.is_timer_running()

def test_timer_start_stop():
    timer = TimerService()
    
    # Start the timer
    timer.start()
    assert timer.is_timer_running()
    
    # Let it run for a bit
    time.sleep(0.1)
    
    # Stop the timer
    timer.stop()
    assert not timer.is_timer_running()
    
    # Check that elapsed time is positive
    elapsed = timer.get_elapsed_time()
    assert elapsed > 0

def test_timer_reset():
    timer = TimerService()
    
    # Start and stop timer
    timer.start()
    time.sleep(0.1)
    timer.stop()
    
    # Reset the timer
    timer.reset()
    assert timer.get_elapsed_time() == 0
    assert not timer.is_timer_running()

def test_timer_get_elapsed_time():
    timer = TimerService()
    
    # Test elapsed time when stopped
    elapsed = timer.get_elapsed_time()
    assert elapsed == 0
    
    # Start timer and check that elapsed time increases
    timer.start()
    time.sleep(0.1)
    timer.stop()
    
    elapsed = timer.get_elapsed_time()
    assert elapsed > 0