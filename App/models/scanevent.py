from App.database import db
from sqlalchemy import *
from App.models import Location
from App.models import Assignee
from App.models import Asset

class Scanevent(db.Model):
    scan_id = db.Column(db.String, primary_key = True, nullable = False, unique = True)
    asset_id = db.Column(db.String, db.ForeignKey('asset.id'), nullable = False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable = False)
    location_id = db.Column(db.String, db.ForeignKey('location.id'), nullable = False)
    status = db.Column(db.String, Nullable = False)
    last_update = db.Column(db.DateTime, default=db.func.current_timestamp())
    change_log = db.Column(db.String(120), Nullable = True)
    
def __init__(self, scan_id, asset_id, user_id, location_id, status, last_update, change_log):
    self.scan_id = scan_id
    self.asset_id = asset_id
    self.user_id = user_id
    self.location_id = location_id
    self.status = status
    self. last_update = last_update
    self.change_log = change_log


def get_json(self):
    return{
        'scan_id: ': self.scan_id,
        'asset_id: ': self.asset_id,
        'user_id: ': self.user_id,
        'location_id: ': self.location_id,
        'status: ': self.status,
        'last_update: ': self.last_update,
        'change_log: ': self.change_log
    }