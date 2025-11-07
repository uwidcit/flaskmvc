from App.database import db
from .user import User

class Student(User):
    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    university = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(100), nullable=False)
    gpa = db.Column(db.Float, nullable=False) 

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, username, password, university, degree, gpa):
        self.username = username
        self.set_password(password)
        self.role = "student"
        self.university = university
        self.degree = degree   
        self.gpa = gpa 

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'university': self.university,
            'degree': self.degree,
            'gpa': self.gpa
        }
    
