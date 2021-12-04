import enum
from flask_sqlalchemy import SQLAlchemy
from .user import User

db = SQLAlchemy()


class Admin(User):
    position = db.Column(db.String(200))
    organization = db.Column(db.String(200))

    def __init__(self, first_name, last_name, email, password, position="Officer", organization="ODPM"):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.postion = position
        self.organization = organization


    

 

