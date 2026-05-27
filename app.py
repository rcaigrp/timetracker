from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"status": "TimeTracker API Running", "message": "Jira Integration Ready"})

@app.route('/api/time-logs', methods=['GET'])
def get_time_logs():
    # Local storage placeholder
    return jsonify([])

@app.route('/api/jira/projects', methods=['GET'])
def get_jira_projects():
    # Jira API placeholder
    return jsonify([])

@app.route('/api/export', methods=['GET'])
def export_logs():
    # Export placeholder
    return jsonify({"type": "CSV", "data": []})

if __name__ == '__main__':
    app.run(debug=True, port=5000)