### app.py
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, RequestLog
from logic import handle_request, CURRENT_BANDWIDTH_USAGE

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/request', methods=['POST'])
def request_bandwidth():
    data = request.get_json()
    source = data['source']
    req_type = data['type']
    required_bandwidth = data['required_bandwidth']
    duration = data.get('duration', 20)  # Default duration if not provided
    result = handle_request(source, req_type, required_bandwidth, duration)
    return jsonify({'status': result})

@app.route('/')
def index():
    logs = RequestLog.query.order_by(RequestLog.timestamp.desc()).limit(20).all()
    return render_template("index.html", logs=logs, current_usage=CURRENT_BANDWIDTH_USAGE)

if __name__ == '__main__':
    app.run(debug=True)
