// swift-tools-version: 5.9
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
    targets: [
        .target(
            name: "TimeTracker",
            dependencies: []
        )
    ]
)