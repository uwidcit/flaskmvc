from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

ACCESS = {
    'user': 1,
    'farmer': 2,
    'admin': 3
}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    currency = db.Column(db.String(120), nullable=False)
    units = db.Column(db.String(10), nullable=False)
    avatar = db.Column(db.String(120), nullable=False)
    access = db.Column(db.Integer, nullable=False, default=ACCESS['user'])

    def __init__(self, username, password, email, phone, address, currency, units, avatar, access=ACCESS['user']):
        self.username = username
        self.set_password(password)
        self.email = email
        self.phone = phone
        self.address = address
        self.currency = currency
        self.units = units
        self.avatar = avatar
        self.access = access

    def to_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'currency': self.currency,
            'units': self.units,
            'avatar': self.avatar,
            'access': self.access
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def set_email(self, email):
        self.email = email

    def set_phone(self, phone):
        self.phone = phone

    def set_address(self, address):
        self.address = address

    def set_currency(self, currency):
        self.currency = currency

    def set_units(self, units):
        self.units = units

    def set_avatar(self, avatar):
        self.avatar = avatar
