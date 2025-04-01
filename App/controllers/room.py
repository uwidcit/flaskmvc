from App.models import Room
from App.controllers.asset import *
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

def delete_room(room_id):
    room = get_room(room_id)
    if room:
        assets = get_all_assets_by_room_id(room_id) # Check if there are any assets in the room
        if assets:
            return False  # Room is not empty, can't be deleted
        else:
            db.session.delete(room)
            db.session.commit()
            return True  # Room deleted successfully
    return False  # Room not found

