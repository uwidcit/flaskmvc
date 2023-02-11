from App.database import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)

    def __init__(self, product_id, name, email, rating, comment):
        self.product_id = product_id
        self.name = name
        self.email = email
        self.rating = rating
        self.comment = comment

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "rating": self.rating,
            "comment": self.comment,
        }
