from App.database import db
#from App.models import asset 
#from App.models import location
#from App.models import assignee
from sqlalchemy import *

conditions = ['Good', 'Missing', 'Misplaced']

class History(db.Model):
    id = db.Column(db.Integer, primary_key = True, Nullable = False, unique = True)
    
    #asset_id = db.Column(db.Integer,db.ForeignKey('asset.id'), nullable=False)
    #asset = db.relationship('Asset', back_populates='history', overlaps="asset")
    
    #dateUpdated = db.Column(db.DateTime, default=asset.dateUpdated)
   # location_name = db.Column(db.String(), db.ForeignKey('location.id), nullable = False)
   #location = db.relationship('Location', back_populates='history', overlaps="location")
   
    #assignee_name = db.Column(db.String(), db.ForeignKey('assignee.id), nullable = Fasle)
    #assignee = db.relationship('Assignee', back_populates='history', overlaps="assignee")
    
    #condition = db.Column(db.String(120))
    #changeLog = db.Column(db.String(200), nullable = True)
    
    
    #def __init__(self):
        #self.asset_id = asset_id
        #self.dateUpdated = dateUpdated
        #self.location = location
        #self.assignee = assignee
        # if condition is None:
        #     self.condition = 'Good'
        # else:
        #     self.validate_and_set_condition(condition)
        #self.changeLog = changeLog


    # def validate_and_set_condition(self, a_condition):
    # valid_condition = [condition for condition in a_condition if condition in conditions] 
    # self.condition ='|'.join(valid_condition)
    
    # def get_json(self):
    #     return{
    #         'id: ':self.id
    #         'asset_id: ':self.asset_id
    #         'date updated: ':self.dateUpdated
    #         'location: ':self.location
    #         'assignee: ':self.assignee
    #         'condition: ':self.condition
    #         'change log: ':self.changeLog
    #     }