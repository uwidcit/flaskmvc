from .user import User 
from App.database import db

class Staff(User):

    
    id = db.Column(db.String(10), db.ForeignKey('user.id'), primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, username, password, staff_id, name):
        super().__init__(username, password)
        self.id = staff_id
        self.name = name

    def get_json(self):
        user_json = super().get_json()
        user_json['staff_id'] = self.id
        user_json['name'] = self.name
        return user_json

