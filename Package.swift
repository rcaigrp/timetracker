// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "TimeTracker",
    platforms: [
        .iOS(.v16)
    ],
    products: [
        .executable(name: "timetracker", targets: ["TimeTracker"])
    ],
    targets: [
        .executableTarget(
            name: "TimeTracker",
            dependencies: [
                .target(name: "TimeTrackerLib")
            ]
        ),
        .target(
            name: "TimeTrackerLib",
            dependencies: []
        )
    ]
)