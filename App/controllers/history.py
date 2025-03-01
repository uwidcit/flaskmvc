from App.models import History
from App.database import db
from App.models import Asset 
from App.controllers.asset import *



def get_all_history_by_condition(condition):
    return History.query.filter_by(condition = condition).all()

def get_all_history_by_date(last_update):
    return History.query.filter_by(last_update = last_update).all()

def get_all_history_by_asset(asset_id):
    return History.query.filter_by(asset_id = asset_id).all()

