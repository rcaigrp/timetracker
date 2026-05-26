import SwiftUI
import UIKit

@main
class AppDelegate: NSObject, UIApplicationDelegate {
    func applicationDidEnterBackground(_ application: UIApplication) {
        TimerManager.shared.pause()
    }
    
    func applicationWillEnterForeground(_ application: UIApplication) {
        TimerManager.shared.resume()
    }
}
