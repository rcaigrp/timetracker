import XCTest
@testable import TimeTracker

class TimeTrackerTests: XCTestCase {
    func testStartTrackingCreatesEntry() {
        let tracker = TimeTracker()
        let entry = tracker.startTracking(description: "Test Description")
        XCTAssertEqual(entry.description, "Test Description")
        XCTAssertNotNil(entry.startTime)
        XCTAssertNil(entry.endTime)
    }
    
    func testStopTrackingSetsEndTime() {
        let tracker = TimeTracker()
        var entry = tracker.startTracking(description: "Test Description")
        tracker.stopTracking(&entry)
        XCTAssertNotNil(entry.endTime)
    }
}
