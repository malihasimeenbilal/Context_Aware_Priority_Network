from models import db, RequestLog
from constants import TOTAL_BANDWIDTH
from datetime import datetime, timedelta
import threading
import time

CURRENT_BANDWIDTH_USAGE = 0
PRIORITY_MAP = {
    'hospital': 1,
    'ambulance': 1,
    'fire-dept': 2,
    'user': 5
}

def handle_request(source, req_type, required_bandwidth, duration):
    global CURRENT_BANDWIDTH_USAGE
    priority = PRIORITY_MAP.get(source, 5)

    if (priority <= 2 or req_type == "emergency") and (CURRENT_BANDWIDTH_USAGE + required_bandwidth <= TOTAL_BANDWIDTH):
        CURRENT_BANDWIDTH_USAGE += required_bandwidth
        status = "granted"
        completion_time = datetime.utcnow() + timedelta(seconds=duration)
    else:
        status = "delayed"
        completion_time = None

    log = RequestLog(
        source=source,
        request_type=req_type,
        status=status,
        required_bandwidth=required_bandwidth,
        duration=duration,
        completion_time=completion_time
    )
    db.session.add(log)
    db.session.commit()

    return status

def free_bandwidth_task():
    global CURRENT_BANDWIDTH_USAGE
    while True:
        time.sleep(5)
        now = datetime.utcnow()
        expired_logs = RequestLog.query.filter(
            RequestLog.status == "granted",
            RequestLog.completion_time != None,
            RequestLog.completion_time <= now
        ).all()
        for log in expired_logs:
            CURRENT_BANDWIDTH_USAGE -= log.required_bandwidth
            print(f"[Freed] {log.required_bandwidth} Mbps from {log.source} @ {log.completion_time}")
            db.session.delete(log)
        db.session.commit()

threading.Thread(target=free_bandwidth_task, daemon=True).start()