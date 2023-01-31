from App.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    retail_price = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    wholesale_price = db.Column(db.Float(decimal_return_scale=2), nullable=False)
    product_unit = db.Column(db.String, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Review', backref='product', lazy=True)

    def __init__(self, name, category, description, image, retail_price, wholesale_price, product_unit, product_quantity):
        self.name = name
        self.category = category
        self.description = description
        self.image = image
        self.retail_price = retail_price
        self.wholesale_price = wholesale_price
        self.product_unit = product_unit
        self.product_quantity = product_quantity

    def to_json(self):
        return{
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'image': self.image,
            'retail_price': round(self.retail_price, 2),
            'wholesale_price': round(self.wholesale_price, 2),
            'product_unit': self.product_unit,
            'product_quantity': self.product_quantity,
            'reviews': [review.to_json() for review in self.reviews]
        }

    # generate mutator functions for all attributes
    def set_name(self, name):
        self.name = name

    def set_category(self, category):
        self.category = category

    def set_description(self, description):
        self.description = description

    def set_image(self, image):
        self.image = image

    def set_retail_price(self, retail_price):
        self.retail_price = retail_price

    def set_wholesale_price(self, wholesale_price):
        self.wholesale_price = wholesale_price

    def set_product_unit(self, product_unit):
        self.product_unit = product_unit

    def set_product_quantity(self, product_quantity):
        self.product_quantity = product_quantity

    def add_review(self, review):
        self.reviews.append(review)

