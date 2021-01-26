from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uwi_id =  db.Column(db.String, nullable=False)
    
    def toDict(self):
        return{
            'id': self.id,
            'uwi_id': self.uwi_id,
        }
