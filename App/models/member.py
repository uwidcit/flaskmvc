from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
db = SQLAlchemy()

class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    memberName = db.Column(db.String(200), nullable = False)
    #Create a relationship between Member and Team
    team = db.relationship('Team', backref='member', lazy=True)
    

    def __init__(self, id, memberName):
        self.memberName = memberName
        self.id = id
    
    def get_json(self):
        return{
            "id": self.id,
            "memberName": self.memberName
        }