from App.models import History
from App.database import db
from App.models import Asset 
from App.controllers import Asset

#def get_missing():

def get_all_assets_by_condition(condition):
    return Asset.query.filter_by(condition = condition).all()

def get_all_assets_by_assignee(id):
    return Asset.query.filter_by(id = id).all()

def get_all_assets_by_location(id):
    return Asset.query.filter_by(id = id).all()

def get_all_assets_by_date(date_updated):
    return Asset.query.filter_by(date_updated = date_updated).all()