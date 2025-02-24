from App.database import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(30), nullable=False)
    floor_name = db.Column(db.String(30), nullable=False)
    building_name = db.Column(db.String(30), nullable=False)
    

    #allows same room name to be used on different floors and
    #but prevent dupilcate combinations of buildings, floor and room
    #location with the same room, floor and building of a other location in the db will be rejected
    __table_args__ = (db.UniqueConstraint('room_name', 'building_name', 'floor_name', name='uq_room_building_floor'),)

    def __init__(self, room_name, floor_name, building_name):
        self.room_name = room_name
        self.building_name = building_name

    def get_json(self):
        return{
            'id': self.id,
            'room': self.room_name,
            'floor': self.floor_name,
            'building': self.building_name

        }