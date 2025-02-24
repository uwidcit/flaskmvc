from App.database import db
from sqlalchemy import *
#from App.models import Location
#from App.models import Assignee

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False, unique = True)
    name = db.Column(db.String(120), Nullable = False, unique=False)
    item_class = db.Column(db.String(120), Nullable = False)
    
    #location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable = False)
    #assignee_id = db.Column(db.Integer, db.ForeignKey('assignee.id'), nullable = False)
    lastUpdate = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    serial_number = db.Column(db.Integer, Nullable = False)
    change_log = db.Column(db.String(300), Nullable = True)
    
def __init__(self, name, item_class, lastUpdate, serial_number):
    self.name = name
    self.item_class = item_class
    self.lastUpdate = lastUpdate
    self.serial_number = serial_number
    
def get_json(self):
    return{
        'id: ': self.id,
        'name: ': self.name,
        'item_class: ': self.item_class,
        #'location_id: ': self.location_id,
        #'assignee_id: ': self.assignee_id,
        'lastUpdate: ': self.lastUpdate,
        'serial_number: ': self.serial_number,
        'change_log: ': self.change_log
    }
    

    