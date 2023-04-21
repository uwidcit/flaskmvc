from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.string(90), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
            'email': self.email
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class RegularUser(User):
  __tablename__='regular_user'
  competitions = db.relationship('Competition', backref='user', lazy=True) # sets up a relationship to competitions which references User

  def get_json(self):
    return {
      "id": self.id,
      "username": self.username,
      "email": self.email,
      "role": 'regular user'
    }

  def __repr__(self):
    return f'<RegularUser {self.id} : {self.username} - {self.email}>' 