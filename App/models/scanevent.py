from App.database import db
from sqlalchemy import *
from App.models import Assignee
from App.models import Asset
from datetime import datetime

class ScanEvent(db.Model):
    scan_id = db.Column(db.String, primary_key = True, nullable = False, unique = True)
    asset_id = db.Column(db.String, db.ForeignKey('asset.id'), nullable = False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)
    room_id = db.Column(db.String, db.ForeignKey('room.room_id'), nullable = False)
    scan_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String, nullable = False)
    notes = db.Column(db.String(120), nullable = True)
    asset = db.relationship('Asset', back_populates='scanevent', overlaps="asset")
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    changeLog = db.Column(db.String(200), nullable = True)
    
    
    def __init__(self, scan_id, asset_id, user_id, room_id, scan_time, status, notes, last_update, changeLog):
        self.scan_id = scan_id
        self.asset_id = asset_id
        self.user_id = user_id
        self.room_id = room_id
        self.scan_time = scan_time
        self.status = status
        self.notes = notes
        self.last_update = last_update
        self.changeLog = changeLog


    def get_json(self):
        return{
            'scan_id: ': self.scan_id,
            'asset_id: ': self.asset_id,
            'user_id: ': self.user_id,
            'room_id: ': self.room_id,
            'scan_time: ': self.scan_time,
            'status: ': self.status,
            'notes: ': self.notes,
            'last_update: ': self.last_update,
            'change log: ': self.changeLog
        }
    