from App.database import db
from sqlalchemy import ForeignKey

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    message = db.Column(db.String(120), nullable=False)
    notification_records = db.relationship("NotificationRecord", backref="notification", lazy=True, cascade="all, delete-orphan")