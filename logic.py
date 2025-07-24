from models import db, RequestLog
from constants import TOTAL_BANDWIDTH
from datetime import datetime, timedelta
from sqlalchemy.sql import func
import threading
import time

PRIORITY_MAP = {
    'hospital': 1,
    'ambulance': 1,
    'fire-dept': 2,
    'police-department': 2,
    'traffic-control': 3,
    'public-transport':4,
    'emergency-alert': 1,
    'user': 5
}

def get_current_bandwidth_usage():
    now = datetime.utcnow()
    total = db.session.query(
        db.func.sum(RequestLog.required_bandwidth)
    ).filter(
        RequestLog.status == "granted",
        RequestLog.completion_time > now  # Only sum non-expired
    ).scalar()
    return int(total or 0)



def handle_request(source, req_type, required_bandwidth, duration):
    priority = PRIORITY_MAP.get(source, 5)

    current_usage = get_current_bandwidth_usage()
    
    if (priority <= 2 or req_type == "emergency") and (current_usage + required_bandwidth <= TOTAL_BANDWIDTH):
        status = "granted"
        completion_time = datetime.utcnow() + timedelta(seconds=duration)
    else:
        status = "delayed"
        completion_time = None

    log = RequestLog(
        source=source,
        request_type=req_type,
        required_bandwidth=required_bandwidth,
        duration=duration,
        status=status,
        timestamp=datetime.utcnow(),  # ✅ Explicitly add timestamp
        completion_time=completion_time
    )

    db.session.add(log)
    db.session.commit()

    return status


def free_expired_bandwidth(app):
    def task():
        print("Bandwidth cleanup thread started")
        while True:
            time.sleep(2)
            with app.app_context():
                now = datetime.utcnow()
                expired_logs = RequestLog.query.filter(
                    RequestLog.status == "granted",
                    RequestLog.completion_time != None,
                    RequestLog.completion_time <= func.datetime('now')
                ).all()
                print(f"🕒 Checking for expired logs at {now} — Found: {len(expired_logs)}")

                for log in expired_logs:
                    print(f"🧹 Removing: {log.source}, {log.required_bandwidth} Mbps")
                    db.session.delete(log)

                if expired_logs:
                    
                    db.session.commit()

    threading.Thread(target=task, daemon=True).start()
