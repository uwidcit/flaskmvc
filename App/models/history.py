from datetime import datetime
from App.database import db
from App.models import asset 
from App.models import assignee
from sqlalchemy import *



class History(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    
    asset_id = db.Column(db.Integer,db.ForeignKey('asset.id'), nullable=False)
    asset = db.relationship('Asset', back_populates='history', overlaps="asset")
    
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   
    changeLog = db.Column(db.String(200), nullable = True)
    
    
    def __init__(self, asset_id, last_update,  status, changeLog):
        self.asset_id = asset_id
        self.last_update = last_update
        self.status = status
        self.changeLog = changeLog



    
    def get_json(self):
        return{
            'id: ':self.id,
            'asset_id: ':self.asset_id,
            'last_update: ':self.last_update,
            'status: ':self.status,
            'change log: ':self.changeLog
        }