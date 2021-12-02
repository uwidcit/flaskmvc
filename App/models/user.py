from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name =  db.Column(db.String, nullable=False)
    last_name =  db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    posts = db.relationship("Post", back_populates="user")
    subscriptions = db.relationship("Subscription", back_populates="user")


    def toDict(self):
        return{
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.email)
        return f"Register('{self.id}','{self.first_name}','{self.last_name}','{self.email}')"
