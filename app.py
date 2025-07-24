import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, RequestLog
from logic import handle_request, get_current_bandwidth_usage, free_expired_bandwidth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///requests.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) #initialize the app 

@app.before_request
def initialize():
    db.create_all()
    free_expired_bandwidth(app)  #freeing extra bandwidths

@app.route('/request', methods=['POST'])
def request_bandwidth():
    data = request.get_json()
    source = data['source']
    req_type = data['type']
    required_bandwidth = data['required_bandwidth']
    duration = data.get('duration', 20)
    result = handle_request(source, req_type, required_bandwidth, duration)
    return jsonify({'status': result})




@app.route('/')
def index():
    logs = RequestLog.query.order_by(RequestLog.timestamp.desc()).limit(30).all()
    current_usage = get_current_bandwidth_usage()
    return render_template("index.html", logs=logs, current_usage=get_current_bandwidth_usage())


@app.route('/clear_expired')
def clear_expired():
    now = datetime.utcnow()
    expired_logs = RequestLog.query.filter(
        RequestLog.status == "granted",
        RequestLog.completion_time != None,
        RequestLog.completion_time <= now
    ).all()

    for log in expired_logs:
        db.session.delete(log)
    db.session.commit()

    return "Expired bandwidth freed!"

if __name__ == '__main__':
   
    free_expired_bandwidth(app)
    app.run(debug=True)