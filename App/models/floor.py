from App.database import db

class Floor(db.Model):
    floor_id = db.Column(db.String(30), primary_key=True)
    building_id = db.Column(db.String(30), db.ForeignKey('building.building_id'), nullable=False)
    floor_name = db.Column(db.String(30), nullable=False)
    
    building = db.relationship('Building', backref=db.backref('floors', lazy=True))
    
    def __init__ (self, floor_id, building_id, floor_name):
        self.floor_id=floor_id
        self.building_id = building_id
        self.floor_name = floor_name
        
    def get_json(self):
        return{
            'floor_id':self.floor_id,
            'building_id':self.building_id,
            'floor_name':self.floor_name
        }