from App.database import db
from sqlalchemy import *
from App.models import Location
from App.models import Assignee

class Asset(db.Model):
    id = db.Column(db.String, primary_key = True, nullable = False, unique = True)
    description = db.Column(db.String(200), Nullable = True, Unique=False)
    model = db.Column(db.String(120), Nullable = True, Unique = False)
    brand = db.Column(db.String(120), Nullable = True)
    serial_number = db.Column(db.String(20), Nullable = True)
    
    
    
    room_id = db.Column(db.String, db.ForeignKey('room.room_id'), nullable = False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('assignee.id'), nullable = False)
    last_update = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    
   
    notes = db.Column(db.String(300), Nullable = True)
    status = db.Column(db.String(120), Nullable = False)
    
def __init__(self,description, model, brand, serial_number, room_id, assignee_id, last_update, notes, status):
    self.description = description
    self.model = model
    self.brand  = brand
    self.serial_number = serial_number
    self.room_id = room_id
    self.assignee_id = assignee_id
    self.last_updated = last_update
    self.notes = notes
    self.status = status
    
def get_json(self):
    return{
        'id: ': self.id,
        'description': self.description,
        'model': self.model,
        'brand': self.brand,
        'serial_number': self.serial_number,
        'room_id': self.room_id,
        'assignee_id':self.assignee_id,
        'last_update': self.last_update,
        'notes': self.notes,
        'status': self.status
        
    }
    

    