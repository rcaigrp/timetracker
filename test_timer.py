import sys
sys.path.insert(0, '/workspace/projects/TimeTracker')

from TimerService import TimerService
import pytest

def test_timer_service_initialization():
    service = TimerService()
    assert service is not None

def test_timer_service_has_correct_attributes():
    service = TimerService()
    assert hasattr(service, 'current_project')
    assert hasattr(service, 'is_running')
    assert hasattr(service, 'start_time')
    assert hasattr(service, 'data')

def test_timer_service_start_stop_timer():
    service = TimerService()
    service.start_timer('test_project')
    assert service.is_running is True
    assert service.current_project == 'test_project'
    
    service.stop_timer()
    assert service.is_running is False
    assert service.current_project is None