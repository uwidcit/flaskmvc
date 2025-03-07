from App.models import ScanEvent
from App.database import db


def add_scan_event(asset_id, user_id, room_id, scan_time, status, notes, last_update, changeLog):
   
    
    newScan = ScanEvent(asset_id, user_id, room_id, scan_time, status, notes, last_update, changeLog)
    
    
    try:
        db.session.add(newScan)
        db.session.commit()
        return newScan
    except:
        db.session.rollback()
        return None

def get_all_scans():
    events = ScanEvent.query.all()
    return events

def get_scan_event(id):
    event = ScanEvent.query.filter_by(id = id).first()
    return event

def get_scans_by_status(status):
    event = ScanEvent.query.filter_by(status = status).all()
    return event

def get_scans_by_last_update(last_update):
    event = ScanEvent.query.filter_by(last_update = last_update).all()
    return event

def get_scans_by_changelog(changeLog):
    event = ScanEvent.query.filter_by(changeLog = changeLog).all()
    return event
