from App.models import Room
from App.database import db

def create_room(room_id, floor_id, room_name):
    new_room = Room(room_id=room_id, floor_id=floor_id, room_name=room_name)
    db.session.add(new_room)
    db.session.commit()
    return new_room

def get_room(room_id):
    return Room.query.get(room_id)

def get_rooms_by_floor(floor_id):
    return Room.query.filter_by(floor_id=floor_id)

def get_all_rooms():
    return Room.query.all()

def get_all_rooms_json():
    rooms=get_all_rooms()
    if not rooms: return None
    rooms = [room.get_json() for room in rooms]
    return rooms

def update_room(room_id, floor_id, room_name):
    room = get_room(room_id)
    if not room: return None
    room.floor_id = floor_id
    room.room_name = room_name