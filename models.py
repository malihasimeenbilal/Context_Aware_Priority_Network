from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RequestLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    request_type = db.Column(db.String(50))
    status = db.Column(db.String(20))
    required_bandwidth = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)
    completion_time = db.Column(db.DateTime)