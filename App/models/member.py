from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
db = SQLAlchemy()

class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    adminId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable = False)
    
    def __init__(self, teamId, adminId, memberName):
        self.teamId = teamId
        self.adminId = adminId
        self.memberName = memberName
    
    def to_json(self):
        return{
            "id": self.id,
            "teamId": self.teamId,
            "adminId": self.admin,
            "memberName": self.memberName,
        }