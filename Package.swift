// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "TimeTracker",
    platforms: [
        .iOS(.v14)
    ],
    products: [
        .library(
            name: "TimeTracker",
            targets: ["TimeTracker"]
        )
    ],
    dependencies: [
        .package(url: "https://github.com/pointfreeco/swift-composable-architecture", from: "0.51.0")
    ],
    targets: [
        .target(
            name: "TimeTracker",
            dependencies: [],
            path: "Sources"
        )
    ]
)