from App.database import db
from .user import User

class Staff(User):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    shortlist = db.relationship('Shortlist', backref=db.backref('staff', lazy='joined'))

    __mapper_args__ = {
        "polymorphic_identity": 'staff',
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.role = "staff"

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role
        }



