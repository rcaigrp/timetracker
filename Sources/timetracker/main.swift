import Foundation
import TimeTrackerLib

let tracker = TimeTracker()

print("Time Tracker App")
print("1. Start")
print("2. Stop")
print("3. Reset")
print("4. Show Elapsed Time")
print("5. Exit")

while true {
    print("")
    print("Enter choice (1-5): ", terminator: "")
    
    if let input = readLine(), let choice = Int(input) {
        switch choice {
        case 1:
            tracker.start()
            print("Timer started.")
        case 2:
            tracker.stop()
            print("Timer stopped.")
        case 3:
            tracker.reset()
            print("Timer reset.")
        case 4:
            let time = tracker.getElapsedTime()
            print("Elapsed time: \(time) seconds")
        case 5:
            print("Exiting...")
            exit(0)
        default:
            print("Invalid choice. Please try again.")
        }
    } else {
        print("Invalid input. Please enter a number between 1 and 5.")
    }
}