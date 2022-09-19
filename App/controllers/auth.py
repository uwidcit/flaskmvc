import flask_login
from flask_jwt import JWT
from App.models import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload['identity'])

def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)


def logout_user():
    flask_login.logout_user()

def setup_jwt(app):
    return JWT(app, authenticate, identity)