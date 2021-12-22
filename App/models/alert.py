from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from datetime import datetime

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.String(300), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    def __init__(self, userID, text, timestamp, longitude, latitude):
        self.userID = userID
        self.text = text
        self.timestamp = timestamp
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return f"{self.userID}"

    def sendNotification(self, notification, messenger):
        self.notified = True
        messenger.notify(self)

    def toDict(self):
        return {
            "userID": self.userID,
            "text": self.text,
            "timestamp": self.timestamp,
            "longitude": self.longitude
            "latitude": self.latitude
        }