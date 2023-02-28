from App.database import db
import datetime


class Reply(db.Model):
    id = db.Column(
        db.Integer, primary_key=True
    )  # primary keys are required by SQLAlchemy
    review_id = db.Column(
        db.Integer, db.ForeignKey("review.id"), nullable=False
    )  # foreign key links to review.id in review table
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # foreign key links to user.id in user table
    body = db.Column(db.String(1024), nullable=False)  # body of reply
    timestamp = db.Column(db.DateTime, nullable=False)  # timestamp of reply

    def __init__(self, review_id, user_id, body):
        self.review_id = review_id
        self.user_id = user_id
        self.body = body
        self.timestamp = datetime.datetime.now()

    def to_json(self):
        return {
            "id": self.id,
            "review_id": self.review_id,
            "user_id": self.user_id,
            "body": self.body,
            "timestamp": self.timestamp,
        }
