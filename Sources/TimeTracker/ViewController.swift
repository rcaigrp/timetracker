import UIKit

class ViewController: UIViewController {
    @IBOutlet weak var timeLabel: UILabel!
    @IBOutlet weak var startButton: UIButton!
    
    private var timer: Timer?
    private var seconds = 0
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
    }
    
    private func setupUI() {
        timeLabel.text = "00:00"
        startButton.setTitle("Start", for: .normal)
        startButton.backgroundColor = .systemBlue
        startButton.layer.cornerRadius = 8
    }
    
    @IBAction func startButtonTapped(_ sender: UIButton) {
        if timer == nil {
            startTimer()
            sender.setTitle("Stop", for: .normal)
        } else {
            stopTimer()
            sender.setTitle("Start", for: .normal)
        }
    }
    
    private func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { _ in
            self.seconds += 1
            let minutes = seconds / 60
            let seconds = seconds % 60
            self.timeLabel.text = String(format: "%02d:%02d", minutes, seconds)
        }
    }
    
    private func stopTimer() {
        timer?.invalidate()
        timer = nil
    }
}