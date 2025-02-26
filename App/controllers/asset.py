from App.models import Asset 
from App.controllers.assignee import *
from App.database import db 


# def add_asset(description, model, brand, serial_number, room_id, assignee_id, last_update, notes, status):


    
#     newAsset = Asset (description, model, brand, serial_number, room_id, assignee_id, last_update, notes, status)
    
    
#     try:
#         db.session.add(newAsset)
#         db.session.commit()
#         return newAsset
#     except:
#         db.session.rollback()
#         return None
    


def get_asset(id):
    return Asset.query.filter_by(id=id).first()

def get_all_assets():
    return Asset.query.all()

def get_all_assets_by_room_id(room_id):
    assets = Asset.query.filter_by(room_id=room_id).all()
    return assets

def get_all_assets_json():
    assets = get_all_assets()
    if not assets:
        return[]
    assets = [asset.get_json() for asset in assets]
    return assets


def get_all_assets_by_room_json(room_id):
    assets = get_all_assets_by_room_id(room_id)
    if not assets:
        return[]
    assets = [asset.get_json() for asset in assets]
    return assets


def add_asset(id, description, model, brand, serial_number, room_id, assignee_id, last_update, notes, status):


    
    newAsset = Asset(id, description, model, brand, serial_number, room_id, assignee_id, last_update, notes, status)
    
    
    try:
        db.session.add(newAsset)
        db.session.commit()
        return newAsset
    except:
        db.session.rollback()
        return None
    


    
    
    