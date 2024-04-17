from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Double, nullable=True)
    weight = db.Column(db.Double, nullable=True)
    videos = db.relationship('Video', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120))
    image = db.Column(db.String(120))
    description = db.Column(db.String(120))
    url = db.Column(db.String(120))

    def __init__(self, title, image, description, url, user_id):
        self.title = title
        self.image = image
        self.description = description
        self.url = url
        self.user_id = user_id





