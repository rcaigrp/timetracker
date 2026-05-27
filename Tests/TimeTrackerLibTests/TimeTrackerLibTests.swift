//
// TimeTrackerLibTests.swift
// TimeTracker
//

import XCTest
@testable import TimeTrackerLib

final class TimeTrackerLibTests: XCTestCase {
    func testExample() throws {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct
        // results.
        XCTAssertEqual(TimeTrackerLib().text, "Hello, World!")
    }
    
    func testTimerServiceStartStop() throws {
        let timerService = TimerService()
        timerService.startTimer()
        XCTAssertNotNil(timerService)
        timerService.stopTimer()
    }
}
