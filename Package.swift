// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "TimeTracker",
    platforms: [
        .iOS(.v14),
        .macOS(.v11)
    ],
    products: [
        .executable(name: "TimeTracker", targets: ["TimeTracker"])
    ],
    dependencies: [
        // Add any dependencies here
    ],
    targets: [
        .target(
            name: "TimeTracker",
            dependencies: [],
            path: "Sources/TimeTracker"
        )
    ]
)