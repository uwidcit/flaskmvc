from App.database import db

class Room(db.Model):
    room_id = db.Column(db.String(30), primary_key=True)
    floor_id = db.Column(db.String(30), db.ForeignKey('floor.floor_id'), nullable=False)
    room_name = db.Column(db.String(30), nullable=False)
    
def __init__(self, room_id, floor_id, room_name):
    self.room_id = room_id
    self.floor_id = floor_id
    self.room_name = room_name
    
def get_json(self):
    return{
        'room_id': self.room_id,
        'floor_id': self.floor_id,
        'room_name': self.room_name
    }