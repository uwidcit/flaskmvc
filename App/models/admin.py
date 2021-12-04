import enum
from flask_sqlalchemy import SQLAlchemy
from .user import User

db = SQLAlchemy()


class Admin(User):
    position = db.Column(db.String(200))
    organization = db.Column(db.String(200))
    

 

