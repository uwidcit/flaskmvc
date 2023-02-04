from App.database import db

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    abstract = db.Column(db.String(500), nullable=False)
    
