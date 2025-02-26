from App.database import db

class Building(db.Model):
    building_id = db.Column(db.String(30), primary_key=True)
    building_name = db.Column(db.String(30), nullable=False)
    
    def __init__ (self, building_id, building_name):
        self.building_id = building_id
        self. building_name = building_name
        
    def get_json(self):
        return{
            'building_id':self.building_id,
            'building_name':self.building_name
        }