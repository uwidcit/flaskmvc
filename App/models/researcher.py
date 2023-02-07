from App.models import User
from .subject import Subject
from App.database import db
from flask_login import UserMixin

class Researcher(UserMixin, User, Subject):
    __tablename__="researcher"
    title = db.Column(db.String(8), nullable=False)
    position = db.Column(db.String(32), nullable=False)
    start_year = db.Column(db.String(8), nullable=False)
    qualifications = db.Column(db.String(300), nullable=False)
    certifications = db.Column(db.String(300), nullable=True)
    skills = db.Column(db.String(300), nullable=False)
    website_url = db.Column(db.String(120), nullable=True)
    introduction = db.Column(db.String(500), nullable=True)
    research_interests = db.relationship("ResearcherTag", backref="researcher", lazy=True, cascade="all, delete-orphan")
    pub_records = db.relationship("PubRecord", backref="researcher", lazy=True, cascade="all, delete-orphan")
    sub_records = db.relationship("ResearcherSubRecord", foreign_keys='ResearcherSubRecord.researcher_id', backref="researcher", lazy=True, cascade="all, delete-orphan")

    def __init__(self):
        pass

    # def __init__(self, email, password, first_name, middle_name, last_name, institution, faculty, department, title, position, start_year, qualifications, skills):
    #     super(Researcher, self).__init__(email, password, first_name, middle_name, last_name, institution, faculty, department) #need to populate arguments
    #     self.title = title
    #     self.position = position
    #     self.start_year = start_year
    #     self.qualifications = qualifications
    #     self.skills = skills

    # def __init__(self, title, position, start_year, qualifications, skills):
    #     super().__init__() #need to populate arguments
    #     self.title = title
    #     self.position = position
    #     self.start_year = start_year
    #     self.qualifications = qualifications
    #     self.skills = skills

    def toDict(self):
        return super().toDict() | {
            'title': self.title,
            'position': self.position,
            'start_year': self.start_year,
            'qualifications': self.qualifications,
            'skills': self.skills
        }