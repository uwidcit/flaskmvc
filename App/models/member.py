from App.database import db
from datetime import datetime

class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    teamId = db.Column(db.Integer, db.ForeignKey("team.id"), nullable=False)
    adminId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(200), nullable = False)
    
    def __init__(self, teamId, adminId, name):
        self.teamId = teamId
        self.adminId = adminId
        self.name = name
    
    def to_json(self):
        return{
            "id": self.id,
            "teamId": self.teamId,
            "adminId": self.adminId,
            "name": self.name,
        }