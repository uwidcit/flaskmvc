from App.models import Asset 
import os, csv
from App.models.asset import *
from App.controllers.assignee import *
from App.database import db 


    


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


def add_asset(id, description, model, brand, serial_number, room_id, last_located, assignee_id, last_update, notes, status):


    
    newAsset = Asset(id, description, model, brand, serial_number, room_id, last_located, assignee_id, last_update, notes, status)
    
    
    try:
        db.session.add(newAsset)
        db.session.commit()
        return newAsset
    except:
        db.session.rollback()
        return None
    
def set_last_located(id,last_located):
    new_asset = get_asset(id)
    new_asset.last_located = last_located
    
def set_status(id):
    new_asset= Asset.query.filter_by(id = id).first()
    if new_asset.room_id == new_asset.last_located :
        new_asset.status = "Found"
    else:
        new_asset.status = "Misplaced"
        
    return new_asset
    
def upload_csv(self):
    with open('CSVsample.csv') as file:
     reader = csv.DictReader(file)
     for row in reader:
         

      new_asset = Asset(description=row['item'],
                            id=row['Asset Tag'],
                            model= row['Model'],
                            brand=row['Brand'],
                            serial_number=row['Serial Number'],
                            room_id=row['Location'],
                            last_located=row['Location'],
                            status=row['Condition'],
                            assignee_id=row['Assignee'],
                            last_update=db.func.current_timestamp(),
                            notes=null
                            
      )
    
     db.session.add(new_asset)
     db.session.commit()
        
    