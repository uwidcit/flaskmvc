from App.database import db
from .user import User

class Employer(User):
    __tablename__ = 'employer'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)

    internship = db.relationship('Internship', backref=db.backref('employer', lazy='joined'))

    __mapper_args__ = {
        "polymorphic_identity": 'employer',
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.role = "employer"

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
        }



