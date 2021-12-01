from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    level = db.relationship("Admin",back_populates="topic")
    posts = db.relationship("Post", back_populates="topic")
            

    def __repr__(self):
        return f"{self.text}"

    @property
    def post_count(self):
        return len(self.posts)

    # TODO: Implement observer pattern
    def subscribe(self, userId):
        self.text = userId

    def unsubscribe(self, userId):
        self.text = userId

    def toDict(self):
        return {
            "text": self.text,
            "level": self.level
        }
