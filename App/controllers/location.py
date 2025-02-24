from sqlite3 import IntegrityError #THIS MAY HAVE TO CHANGE DEPENDING ON THE DB
from App.models import Location
from App.database import db

def create_location(room_name, floor_name, building_name):
    try:
        new_location = Location(room_name=room_name, floor_name=floor_name, building_name=building_name)
        db.session.add(new_location)
        db.session.commit()
        return new_location  # Return the created location
    except IntegrityError:
        db.session.rollback()
        return None
    

def get_locations_by_building(building_name):
    return Location.query.filter_by(building_name=building_name).all()

def get_locations_by_floor(floor_name):
    return Location.query.filter_by(floor_name=floor_name).all()

def get_location(id):
    return Location.query.get(id)

def get_all_locations():
    return Location.query.all()

def get_all_locations_json():
    locs = Location.query.all()
    if not locs:
        return []
    return[loc.get_json() for loc in locs]

def update_location_room(id, room_name):
    loc = get_location(id)

    if not loc:
        return None
    
    loc.room_name = room_name
    db.session.add(loc)
    return db.session.commit()

def update_location_floor(id, floor_name):
    loc = get_location(id)

    if not loc:
        return None
    
    loc.floor_name = floor_name
    db.session.add(loc)
    return db.session.commit()

def update_location_building(id, building_name):
    loc = get_location(id)

    if not loc:
        return None
    
    loc.building_name = building_name
    db.session.add(loc)
    return db.session.commit()

#finds all buildings in the db
def get_all_buildings():
    return db.session.query(Location.building_name).distinct().all()

#finds all the floors for a given building
def get_floors_by_building(building_name):
    return [row[0] for row in db.session.query(Location.floor_name)
            .filter_by(building_name=building_name)
            .distinct()
            .all()]

#finds all rooms for a given floor
def get_rooms_by_floor(building_name, floor_name):
    return [row[0] for row in db.session.query(Location.room_name)
            .filter_by(building_name=building_name, floor_name=floor_name)
            .distinct()
            .all()]
