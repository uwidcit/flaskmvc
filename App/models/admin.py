from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from models import User, Competition
db = SQLAlchemy()

class Admin(User):
    __tablename__='admin_user'
    comps = db.relationship('Competition', backref='user', lazy=True, cascade = "all, delete-orphan") 
    
    def add_comp(self, compName, startDate, endDate, teamID):
        new_comp = Competition(compName=compName, startDate=startDate, endDate=endDate, teamID = teamID)
        self.comps.append(new_comp)
        db.session.add(self)
        db.session.commit()
        return new_comp
    
    #update comp with user data
    def update_comp(self, compCode, compName, startDate, endDate, teamID):
        for comp in self.comps:
            if comp.compCode == compCode:
                comp.compName = compName
                comp.startDate = startDate
                comp.endDate = endDate
                comp.teamID = teamID
        db.session.add(self)
        db.session.commit()
        return self.comps
    
    def delete_comp(self, compCode):
        for comp in self.comps:
            if comp.compCode == compCode:
                self.comps.remove(comp)
        db.session.add(self)
        db.session.commit()
        return self.comps

    
    def to_json(self):
        return{
            "id": self.id,
            "username": self.username,
            "email":self.email,
            "role": 'admin user'
        }