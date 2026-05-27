import UIKit

let appDelegate = AppDelegate()
UIApplicationMain(
    CommandLine.argc,
    CommandLine.unsafeArgv,
    nil,
    String(describing: type(of: appDelegate))
)