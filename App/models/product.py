from App.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    farmer_id = db.Column(db.Integer, db.ForeignKey("user.id"),
                          nullable=False)  # foreign key links to user.id in user table
    name = db.Column(db.String, nullable=False)  # name of product
    description = db.Column(db.String, nullable=False)  # description of product
    image = db.Column(db.String, nullable=False)  # image of product
    retail_price = db.Column(db.Float(decimal_return_scale=2), nullable=False)  # price of product
    product_quantity = db.Column(db.Integer, nullable=False)  # quantity of product available
    reviews = db.relationship("Review", backref="product", lazy=True)  # reviews of product
    archived = db.Column(db.Boolean, nullable=False, default=False)  # archived status of product

    # wholesale_price = db.Column(db.Float(decimal_return_scale=2), nullable=False) # wholesale price of product
    # product_unit = db.Column(db.String, nullable=False) # unit of product

    def __init__(self, name, description, image, retail_price, product_quantity, farmer_id):
        self.name = name
        self.description = description
        self.image = image
        self.retail_price = retail_price
        self.product_quantity = product_quantity
        self.farmer_id = farmer_id
        self.archived = False

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "image": self.image,
            "retail_price": round(self.retail_price, 2),
            # "wholesale_price": round(self.wholesale_price, 2),
            "product_quantity": self.product_quantity,
            "reviews": [review.to_json() for review in self.reviews],
            "archived": self.archived,
        }
