// swift-tools-version:5.7
import PackageDescription

let package = Package(
    name: "TimeTracker",
    platforms: [
        .iOS(.v14)
    ],
    products: [
        .executable(name: "TimeTracker", targets: ["TimeTracker"])
    ],
    dependencies: [],
    targets: [
        .target(
            name: "TimeTracker",
            dependencies: [],
            path: ".",
            exclude: ["Info.plist"]
        )
    ]
)