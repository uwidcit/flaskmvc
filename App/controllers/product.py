from App.database import db
from App.models.product import Product


def create_product(name, description, image, retail_price, product_quantity):
    product = Product(name, description, image, retail_price, product_quantity)
    db.session.add(product)
    db.session.commit()
    return product.to_json()


def get_all_products():
    return Product.query.all()


def get_all_products_json():
    return [product.to_json() for product in get_all_products()]


def get_product_by_id(id):
    return Product.query.get(id)


def get_product_by_id_json(id):
    return get_product_by_id(id).to_json()


def get_products_by_name(name):
    return Product.query.filter_by(name=name).all()


def get_products_by_name_json(name):
    return [product.to_json() for product in get_products_by_name(name)]


def update_product(id, name, description, image, retail_price, product_quantity):
    product = get_product_by_id(id)
    if product:
        product.name = name
        product.description = description
        product.image = image
        product.retail_price = retail_price
        product.product_quantity = product_quantity
        db.session.add(product)
        return db.session.commit()
    return None


def archive_product(id):
    product = get_product_by_id(id)
    if product:
        product.archived = True
        db.session.add(product)
        return db.session.commit()
    return None


def delete_product(id):
    product = get_product_by_id(id)
    if product:
        db.session.delete(product)
        return db.session.commit()
    return None
