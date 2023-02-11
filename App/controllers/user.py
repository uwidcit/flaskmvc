from App.models.user import User
from App.database import db


def create_user(username, password, access):
    new_user = User(username=username, password=password, access=access)
    db.session.add(new_user)
    db.session.commit()
    return new_user


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
