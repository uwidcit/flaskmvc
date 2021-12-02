import flask_login
from App.models import User


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload['identity'])

def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)

  
def validate_user_credentials(email, password):
    return authenticate(email, password)


def logout_user():
    flask_login.logout_user()
