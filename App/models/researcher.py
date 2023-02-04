from App.models import User
from flask_login import UserMixin

class Researcher(UserMixin, User, Subject):
    title = db.Column(db.String(8), nullable=False)
    position = db.Column(db.String(32), nullable=False)
    start_year = db.Column(db.String(8), nullable=False)
    qualifications = db.Column(db.String(300), nullable=False)
    certifications = db.Column(db.String(300), nullable=True)
    skills = db.Column(db.String(300), nullable=False)
    website_url = db.Column(db.String(120), nullable=True)
    introduction - db.Column(db.String(500), nullable=True)

    def __init__(self, title, position, start_year, qualifications, skills):
        super().__init__() #need to populate arguments
        self.title = title
        self.position = position
        self.start_year = start_year
        self.qualifications = qualifications
        self.skills = skills

    def __init__(self, title, position, start_year, qualifications, skills):
        super().__init__() #need to populate arguments
        self.title = title
        self.position = position
        self.start_year = start_year
        self.qualifications = qualifications
        self.skills = skills