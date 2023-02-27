from App.models.review import Review
from App.database import db


def create_review(product_id, user_id, body, timestamp):
    new_review = Review(product_id=product_id, user_id=user_id, body=body, timestamp=timestamp)
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


def get_reviews_by_user_id(user_id):
    return Review.query.filter_by(user_id=user_id).all()


def get_reviews_by_user_id_json(user_id):
    return [review.to_json() for review in get_reviews_by_user_id(user_id)]


def update_review(id, body):
    review = get_review_by_id(id)
    if review:
        review.body = body
        db.session.add(review)
        return db.session.commit()
    return None


def delete_review(id):
    review = get_review_by_id(id)
    if review:
        db.session.delete(review)
        return db.session.commit()
    return None
