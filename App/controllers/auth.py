import flask_login
from flask_jwt import JWT

from App.models import Users


def authenticate(uname, password):
    user = Users.query.filter_by(uname=uname).first()
    if user and user.check_password(password):
        return user


# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return Users.query.get(payload["identity"])


def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)


def logout_user():
    flask_login.logout_user()


def setup_jwt(app):
    return JWT(app, authenticate, identity)


# for login manager
def load_user_from_id(user_id):
    return Users.query.get(user_id)