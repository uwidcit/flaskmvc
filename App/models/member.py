from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
db = SQLAlchemy()

class Member(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(200), nullable = False)
    
    def __init__(self, memberName):
        self.memberName = memberName
    
    def to_json(self):
        return{
            "id": self.id,
            "memberName": self.memberName,
        }