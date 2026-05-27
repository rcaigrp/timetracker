// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "TimeTracker",
    platforms: [
        .macOS(.v12)
    ],
    products: [
        .executable(name: "TimeTracker", targets: ["TimeTracker"]),
        .library(name: "TimeTrackerLib", targets: ["TimeTrackerLib"])
    ],
    dependencies: [
        // Add any dependencies here
    ],
    targets: [
        .executableTarget(
            name: "TimeTracker",
            dependencies: ["TimeTrackerLib"],
            path: "Sources/TimeTracker"
        ),
        .target(
            name: "TimeTrackerLib",
            dependencies: [],
            path: "Sources/TimeTrackerLib"
        )
    ]
)