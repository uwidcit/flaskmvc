# from flask_login import login_user, login_manager, logout_user, LoginManager
# from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from flask_jwt import JWT
from App.models import User
from App.controllers import get_user_by_username

# from App.models import User

# def jwt_authenticate(username, password):
#   user = User.query.filter_by(username=username).first()
#   if user and user.check_password(password):
#     return create_access_token(identity=username)
#   return None

# def login(username, password):
#     user = User.query.filter_by(username=username).first()
#     if user and user.check_password(password):
#         return user
#     return None

# def setup_flask_login(app):
#     login_manager = LoginManager()
#     login_manager.init_app(app)
    
#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(user_id)
    
#     return login_manager

# def setup_jwt(app):
#     jwt = JWTManager(app)

#     @jwt.user_identity_loader
#     def user_identity_lookup(identity):
#         user = User.query.filter_by(username=identity).one_or_none()
#         if user:
#             return user.id
#         return None

#     @jwt.user_lookup_loader
#     def user_lookup_callback(_jwt_header, jwt_data):
#         identity = jwt_data["sub"]
#         return User.query.get(identity)

#     return jwt

def authenticate(username, password):
    user = get_user_by_username(username)
    if user and user.check_password(password):
        return user
    return None


# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload["identity"])


def setup_jwt(app):
    return JWT(app, authenticate, identity)