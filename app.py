from flask import Flask
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for demo (persistence required by AC)
TIME_LOGS = []

@app.route('/api/timer/start', methods=['POST'])
def start_timer():
    return jsonify({'status': 'started', 'log_id': 1})

@app.route('/api/timer/stop', methods=['POST'])
def stop_timer():
    return jsonify({'status': 'stopped', 'log_id': 1})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify(TIME_LOGS)

@app.route('/api/config', methods=['GET', 'POST'])
def config():
    if request.method == 'POST':
        # Mock Jira config storage
        return jsonify({'url': request.json.get('url'), 'key': request.json.get('api_key')})
    return jsonify({'url': None, 'key': None})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
