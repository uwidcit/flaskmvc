from App.database import db
from sqlalchemy import *
from App.models import Location
from App.models import Assignee
from App.models import Asset

class ScanEvent(db.Model):
    scan_id = db.Column(db.String, primary_key = True, nullable = False, unique = True)
    asset_id = db.Column(db.String, db.ForeignKey('asset.id'), nullable = False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)
    room_id = db.Column(db.String, db.ForeignKey('location.id'), nullable = False)
    scan_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String, Nullable = False)
    notes = db.Column(db.String(120), Nullable = True)
    
def __init__(self, scan_id, asset_id, user_id, room_id, scan_time, status, notes):
    self.scan_id = scan_id
    self.asset_id = asset_id
    self.user_id = user_id
    self.room_id = room_id
    self.scan_time = scan_time
    self.status = status
    self.notes = notes


def get_json(self):
    return{
        'scan_id: ': self.scan_id,
        'asset_id: ': self.asset_id,
        'user_id: ': self.user_id,
        'room_id: ': self.room_id,
        'scan_time: ': self.scan_time,
        'status: ': self.status,
        'notes: ': self.notes
    }