from App.database import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)

    def __init__(self, name, email, text):
        self.name = name
        self.email = email
        self.text = text

    def to_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'text': self.text
        }
