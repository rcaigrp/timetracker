from flask import Flask, request, jsonify
import time

class TimeTracker:
    def __init__(self):
        self.start_time = None
        self.total_time = 0
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            return True
        return False

    def stop(self):
        if self.is_running and self.start_time:
            self.total_time += time.time() - self.start_time
            self.is_running = False
            return True
        return False

    def get_total_time(self):
        if self.is_running and self.start_time:
            return self.total_time + (time.time() - self.start_time)
        return self.total_time

app = Flask(__name__)
time_tracker = TimeTracker()

@app.route('/start', methods=['POST'])
def start_timer():
    if time_tracker.start():
        return jsonify({'status': 'started', 'message': 'Timer started successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Timer already running'}), 400

@app.route('/stop', methods=['POST'])
def stop_timer():
    if time_tracker.stop():
        return jsonify({'status': 'stopped', 'message': 'Timer stopped successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Timer not running'}), 400

@app.route('/time', methods=['GET'])
def get_time():
    total_seconds = time_tracker.get_total_time()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return jsonify({
        'total_seconds': total_seconds,
        'formatted_time': f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
