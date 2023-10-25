from .user import User 
from App.database import db

class Staff(User):

    
    id = db.Column(db.String(10), db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, password, staff_id, name):
        super().__init__(staff_id, password)
        self.id = staff_id
        self.name = name

    def get_json(self):
        return{
            'staff_id': self.id,
            'name': self.name,
        }

