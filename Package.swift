// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "TimeTracker",
    products: [
        .executable(name: "TimeTracker", targets: ["TimeTracker"]),
    ],
    dependencies: [
        // No external dependencies needed for basic functionality
    ],
    targets: [
        .target(
            name: "TimeTracker",
            dependencies: []
        )
    ]
)