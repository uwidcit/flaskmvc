from App.database import db
from sqlalchemy import *

class Acquisition(db.Model):

    acquisition_id = db.Column(db.String , primary_key=True, nullable = False, unique=True)
    asset_id = db.Column(db.String, db.ForeignKey('asset.asset_id'), nullable=False)
    provider_id = db.Column(db.String, db.ForeignKey('provider.provider_id'), nullable=False)
    purchase_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    cost = db.Column(db.Double, nullable=True)

    def __init__(self, id, asset, provider, date, cost):
        self.acquisition_id = id
        self.asset_id = asset
        self.provider_id = provider
        self.purchase_date = date
        self.cost = cost


    def get_json(self):
        return{
            "acquisition id: ": self.acquisition_id,
            "asset id: ": self.asset_id,
            "provider: ": self.provider_id,
            "purchase date: ": self.purchase_date,
            "cost: ": self.cost
        }

