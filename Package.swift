// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "TimeTracker",
    platforms: [
        .iOS(.v16)
    ],
    products: [
        .library(
            name: "TimeTrackerLib",
            targets: ["TimeTrackerLib"]
        ),
        .executable(
            name: "timetracker",
            targets: ["TimeTracker"]
        )
    ],
    dependencies: [
        // Add any dependencies here
    ],
    targets: [
        .target(
            name: "TimeTrackerLib",
            dependencies: []
        ),
        .executableTarget(
            name: "TimeTracker",
            dependencies: ["TimeTrackerLib"]
        )
    ]
)