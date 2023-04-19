from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    competitionId = db.Column(db.Integer, db.ForeignKey("compCode"),nullable=False)
    teamName = db.Column(db.String(120), nullable=False)
    score = db.Column(db.String(120), nullable = False)
    members = db.relationship('Member', backref='team', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, competitionId, teamName, score):
        self.competitionId = competitionId
        self.teamName = teamName
        self.score = score
    
    def to_json(self):
        return{
            "id": self.id,
            "competitionId": self.competitionId,
            "teamName": self.teamName,
            "score": self.score,
            "members": [member.to_json() for member in self.members],
            
        }