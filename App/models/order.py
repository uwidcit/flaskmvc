from App.database import db
from datetime import datetime


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    date_placed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    products = db.relationship('OrderProduct', backref='order', lazy=True)
    total = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    status = db.Column(db.String, nullable=False)

    def __init__(self, user_id, total, status):
        self.user_id = user_id
        self.total = total
        self.status = status

    def to_json(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'date_placed': self.date_placed,
            'products': [product.to_json() for product in self.products],
            'total': round(self.total, 2),
            'status': self.status
        }
