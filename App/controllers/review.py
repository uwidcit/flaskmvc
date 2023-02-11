from App.models.review import Review
from App.database import db


def create_review(product_id, name, email, rating, comment):
    new_review = Review(
        product_id=product_id, name=name, email=email, rating=rating, comment=comment
    )
    db.session.add(new_review)
    db.session.commit()
    return new_review


def get_all_reviews():
    return Review.query.all()


def get_all_reviews_json():
    return [review.to_json() for review in get_all_reviews()]


def get_review_by_id(id):
    return Review.query.get(id)


def get_review_by_id_json(id):
    return get_review_by_id(id).to_json()


def get_reviews_by_product_id(product_id):
    return Review.query.filter_by(product_id=product_id).all()


def get_reviews_by_product_id_json(product_id):
    return [review.to_json() for review in get_reviews_by_product_id(product_id)]


def update_review(id, name, email, comment):
    review = get_review_by_id(id)
    if review:
        review.name = name
        review.email = email
        review.text = comment
        db.session.add(review)
        return db.session.commit()
    return None


def delete_review(id):
    review = get_review_by_id(id)
    if review:
        db.session.delete(review)
        return db.session.commit()
    return None
