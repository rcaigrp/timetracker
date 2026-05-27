// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "TimeTracker",
    platforms: [
        .macOS(.v12),
        .iOS(.v15)
    ],
    products: [
        .library(
            name: "TimeTrackerLib",
            targets: ["TimeTrackerLib"]),
        .executable(
            name: "TimeTrackerCLI",
            targets: ["TimeTrackerCLI"])
    ],
    dependencies: [
        // Add any dependencies here
    ],
    targets: [
        .target(
            name: "TimeTrackerLib",
            dependencies: []),
        .target(
            name: "TimeTrackerCLI",
            dependencies: ["TimeTrackerLib"]),
        .testTarget(
            name: "TimeTrackerTests",
            dependencies: ["TimeTrackerLib"])
    ]
)