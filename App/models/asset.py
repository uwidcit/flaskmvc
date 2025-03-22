from App.database import db
from sqlalchemy import *


class Asset(db.Model):
    id = db.Column(db.String, primary_key = True, nullable = False, unique = True)
    description = db.Column(db.String(200), nullable = True, unique=False)
    model = db.Column(db.String(120), nullable = True, unique = False)
    brand = db.Column(db.String(120), nullable = True)
    serial_number = db.Column(db.String(20), nullable = True)
    
    
    
    room_id = db.Column(db.String, db.ForeignKey('room.room_id'), nullable = False)
    last_located = db.Column(db.String, db.ForeignKey('room.room_id'), default = room_id)
    assignee_id = db.Column(db.Integer, db.ForeignKey('assignee.id'), nullable = False)
    last_update = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    
   # change_log = db.Column(db.String(300), Nullable = True)
    notes = db.Column(db.String(300), nullable = True)
    status = db.Column(db.String(120), nullable = False)
    
    scanevent = db.relationship('ScanEvent', back_populates='asset')
    
    
    def __init__(self, id, description, model, brand, serial_number, room_id, last_located, assignee_id, last_update, notes, status):
        self.id = id
        self.description = description
        self.model = model
        self.brand  = brand
        self.serial_number = serial_number
        self.room_id = room_id
        self.last_located = last_located
        self.assignee_id = assignee_id
        self.last_update = last_update
        self.notes = notes
        self.status = status
        
    def get_json(self):
        return{
            'id': self.id,
            'description': self.description,
            'model': self.model,
            'brand': self.brand,
            'serial_number': self.serial_number,
            'room_id': self.room_id,
            'last_located': self.last_located,
            'assignee_id':self.assignee_id,
            'last_update': self.last_update,
            'notes': self.notes,
            'status': self.status
            
        }
        

        