from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name =  db.Column(db.String, nullable=False)
    last_name =  db.Column(db.String, nullable=False)

    def toDict(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
