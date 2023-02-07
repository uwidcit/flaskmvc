from App.database import db
from sqlalchemy import ForeignKey

class NotificationRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    notification_id = db.Column(db.Integer, ForeignKey("notification.id"), nullable=False)

    def __init__(self, user_id, notification_id):
        self.user_id = user_id
        self.notification_id = notification_id