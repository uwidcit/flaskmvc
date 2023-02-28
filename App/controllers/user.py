from App.models.user import User, ACCESS
from App.database import db


def create_user(username, email, password, access, phone="", address="", currency="USD", units="kg", avatar=""):
    new_user = User(username=username, email=email, password=password, access=access, phone=phone, address=address,
                    currency=currency, units=units, avatar=avatar)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def create_admin(username, email, password):
    return create_user(username, email, password, "admin", phone="", address="", currency="USD", units="kg", avatar="")


def create_farmer(username, email, password):
    return create_user(username, email, password, "farmer", phone="", address="", currency="USD", units="kg", avatar="")


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_by_id(id):
    return User.query.get(id)


def get_all_users():
    return User.query.all()


def get_all_users_json():
    return [user.to_json() for user in get_all_users()]


def update_user(id, username):
    user = get_user_by_id(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None


def is_admin(user):
    return user.get_access() == ACCESS["admin"]


def is_farmer(user):
    return user.get_access() == ACCESS["farmer"]
