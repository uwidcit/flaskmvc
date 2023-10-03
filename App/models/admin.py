from App.database import db
from App.models import User

class Admin(User):
    id=db.Column(db.ForeignKey('user.id'), primary_key=True)
    name=db.Column(db.String(120), nullable=False)
    # user=db.relationship('User',backref=db.backref('Admin'))

    def __init__(self, username, password, name):
        super().__init__(username=username,password=password)
        self.name=name
        self.id=id

    def get_json(self):
        return{
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Admin {self.id} - {self.name}>'

