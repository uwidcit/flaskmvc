from flask_sqlalchemy import SQLAlchemy

# init db
db = SQLAlchemy()


class Admin(db.Model):
    level = db.Column(db.Integer, primary_key=True)
    

    def __init__(self, level):
        self.level = level
        

    def __repr__(self):
        return f"{self.level}"


    def toDict(self):
        return {
            "level": self.level
        }
