from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
db = SQLAlchemy()

class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adminId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    compName = db.Column(db.String(120), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    teams = db.relationship("Team", backref="competition", lazy=True, cascade = "all, delete-orphan")

    def __init__(self, adminId, compName, startDate, endDate):
        self.adminId = adminId
        self.compName = compName
        self.startDate = startDate
        self.endDate = endDate
        
    def to_json(self):
        return{
            "id": self.id,
            "adminId": self.adminId,
            "compName": self.compName,
            "startDate": self.startDate,
            "endDate": self.endDate,
            "teams": [team.to_json() for team in self.teams],
        }