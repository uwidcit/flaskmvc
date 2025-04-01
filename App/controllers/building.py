from App.models import Building
from App.database import db
from App.controllers.floor import *

def create_building(building_id, building_name):
    new_building = Building(building_id=building_id, building_name=building_name)
    db.session.add(new_building)
    db.session.commit()
    return new_building

def get_building(building_id):
    return Building.query.get(building_id)

def edit_building(building_id, building_name):
    building = get_building(building_id)
    if not building:
        return None
    else:
        building.building_name = building_name
        db.session.add(building)
        return db.session.commit()

def get_all_building_json():
    buildings = Building.query.all()
    if not buildings:
        return[]
    buildings = [building.get_json() for building in buildings]
    return buildings

def update_building(building_id, building_name):
    building = get_building(building_id)
    if not building: return None
    building.building_name = building_id
    return db.session.commit()

def delete_building(building_id):
    building = get_building(building_id)
    if building:
        floors = get_floors_by_building(building_id) # Check if there are any floors in the building
        if floors:
            return False  # Building has floors, can't be deleted
        else:
            db.session.delete(building)
            db.session.commit()
            return True  # Building deleted successfully
    return False  # Building not found

