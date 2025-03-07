
from App.database import db
# from sqlalchemy import *



class History(db.Model):
    
    def __init__(self, asset_id,   status, changeLog):
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