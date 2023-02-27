from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

ACCESS = {"user": 1, "farmer": 2, "admin": 3}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    username = db.Column(db.String, nullable=False)  # username of user
    password = db.Column(db.String(120), nullable=False)  # password of user
    access = db.Column(db.Integer, nullable=False)  # access level of user
    p_reviews = db.relationship("Review", backref="user", lazy=True)  # reviews of product
    p_replies = db.relationship("Reply", backref="user", lazy=True)  # replies to review
    products = db.relationship("Product", backref="user", lazy=True)  # products of farmer

    # email = db.Column(db.String(120), nullable=False)
    # phone = db.Column(db.String(120), nullable=False)
    # address = db.Column(db.String(120), nullable=False)
    # currency = db.Column(db.String(120), nullable=False)
    # units = db.Column(db.String(10), nullable=False)
    # avatar = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password, access="user"):
        self.username = username
        self.set_password(password)
        # self.email = email
        # self.phone = phone
        # self.address = address
        # self.currency = currency
        # self.units = units
        # self.avatar = avatar
        self.access = ACCESS[access]

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            # "email": self.email,
            # 'phone': self.phone,
            # 'address': self.address,
            # 'currency': self.currency,
            # 'units': self.units,
            # 'avatar': self.avatar,
            "access": self.access,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def get_access(self):
        return self.access
