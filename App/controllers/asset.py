from App.models import Asset 
from App.database import db 


def add_asset(id, name, item_class, last_update, serial_number, change_log):
    newAsset = Asset(id, name, item_class, last_update, serial_number, change_log)
    try:
        db.session.add(newAsset)
        db.session.commit()
        return newAsset
    except:
        db.session.rollback()
        return None

def get_asset(id):
    return Asset.query.filter_by(id=id).first()

def get_all_assets():
    return Asset.query.all()

def get_all_assets_json():
    assets = get_all_assets()
    if not assets:
        return[]
    assets = [asset.get_json() for asset in assets]
    return assets

def update_condition(id, condition):
    asset = get_asset(id)
    asset.condition = condition
    
    return asset
    
    