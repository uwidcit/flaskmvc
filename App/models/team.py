from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
db = SQLAlchemy()

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    teamName = db.Column(db.String(120), nullable=False)
    score = db.Column(db.String(120), nullable = False)
    #memberID = db.Column(db.String(120), db.ForeignKey("member.id"), nullable = False)
    comps = db.relationship('Competition', backref='team', lazy=True)
    members = db.relationship('Member', backref='team', lazy=True)
    
    def __init__(self, teamName, members, score):
        self.teamName = teamName
        #self.members = members
        self.score = score
    
    def get_json(self):
        return{
            "id": self.id,
            "teamName": self.teamName,
            "members": self.members,
            "score": self.score,
        }