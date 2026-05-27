import PackageDescription

let package = Package(
    name: "TimeTracker",
    products: [
        .executable(name: "TimeTracker", targets: ["TimeTracker"]),
    ],
    dependencies: [],
    targets: [
        .target(
            name: "TimeTracker",
            dependencies: []
        ),
    ]
)