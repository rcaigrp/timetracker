import UIKit
import SwiftUI

class ViewController: UIViewController {
    @IBOutlet weak var timerLabel: UILabel!
    @IBOutlet weak var startStopButton: UIButton!
    
    private let timerService = TimerService.shared
    private var timer: Timer?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        updateTimerDisplay()
    }
    
    private func setupUI() {
        timerLabel.text = "00:00:00"
        startStopButton.setTitle("Start", for: .normal)
        startStopButton.addTarget(self, action: #selector(startStopTapped), for: .touchUpInside)
    }
    
    @objc private func startStopTapped() {
        if timerService.isRunning {
            timerService.stop()
            startStopButton.setTitle("Start", for: .normal)
        } else {
            timerService.start()
            startStopButton.setTitle("Stop", for: .normal)
        }
        updateTimerDisplay()
    }
    
    private func updateTimerDisplay() {
        let formattedTime = formatTime(timerService.elapsedTime)
        timerLabel.text = formattedTime
        
        if timerService.isRunning {
            startStopButton.setTitle("Stop", for: .normal)
        } else {
            startStopButton.setTitle("Start", for: .normal)
        }
    }
    
    private func formatTime(_ timeInterval: TimeInterval) -> String {
        let hours = Int(timeInterval) / 3600
        let minutes = Int(timeInterval) / 60 % 60
        let seconds = Int(timeInterval) % 60
        return String(format: "%02d:%02d:%02d", hours, minutes, seconds)
    }
}