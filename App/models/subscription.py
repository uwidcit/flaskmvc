import enum
from datetime import datetime
from App.database import db


class Status(int, enum.Enum):
    INACTIVE = 0
    ACTIVE = 1


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    topicId = db.Column(db.Integer, db.ForeignKey('topic.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Enum(Status), default=Status.ACTIVE)

    def __init__(self, userId, topicId):
        self.userId = userId
        self.topicId = topicId

    def __repr__(self):
        return f"Subscription(userId={self.userId}, topicId={self.topicId}, created={self.created}, status={self.status})"

    def set_active(self):
        self.status = Status.ACIVE

    def set_inactive(self):
        self.status = Status.INACTIVE

    def get_created_string(self):
        return self.created.strftime("%Y-%m-%dT%H:%M:%SZ")

    def toDict(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "topicId": self.topicId,
            "created": self.get_created_string(),
            "status": self.status
        }
