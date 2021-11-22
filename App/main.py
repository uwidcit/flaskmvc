import os
from flask import Flask
from flask_jwt import JWT
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, emit, join_room

from flask_uploads import (
    UploadSet,
    configure_uploads,
    IMAGES,
    TEXT,
    DOCUMENTS
)
from App.controllers.user_controller import get_user_by_id
from App.models.user import User

from App.modules.auth_module import (authenticate, identity)
from App.database import db

from App.views import (
    api_bp,
    user_bp,
    chatroom_bp,
    auth_bp
)


# place all views here
views = [api_bp, user_bp, chatroom_bp, auth_bp]


def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'development')
    if app.config['ENV'] == "development":
        app.config.from_object('App.config')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            'SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['JWT_EXPIRATION_DELTA'] = os.environ.get(
            'JWT_EXPIRATION_DELTA')
        app.config['DEBUG'] = os.environ.get('DEBUG')
        app.config['ENV'] = os.environ.get('ENV')

    for key, value in config.items():
        app.config[key] = config[key]


def init_db(app):
    db.init_app(app)
    db.create_all(app=app)


def create_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    return login_manager


def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    jwt = JWT(app, authenticate, identity)
    init_db(app)

    app.app_context().push()
    return app


def create_sockets(app):
    return SocketIO(app, cors_allowed_origins="*")


app = create_app()
socketio = create_sockets(app)
login_manager = create_login_manager(app)


# User login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Socket events
@socketio.on("join_room")
def handle_join_room(data):
    sender_id = str(current_user.id)
    to_id = str(data['to'])
    to_user = get_user_by_id(to_id)

    room = get_room(sender_id, to_id)
    join_room(room)

    emit("join_room", {'message': 'Now messaging ' +
         to_user.first_name, 'from': 'System', 'to': current_user.first_name}, room=room)


@socketio.event
def connect():
    print(
        f"User connected: {current_user.first_name} {current_user.last_name}")
    emit("user_connect", {"from": "System", "to": "", "message": f"User connected"})


@socketio.event
def message_send(context):
    sender_name = current_user.get_full_name()

    to_id = str(context['to'])
    to_user = get_user_by_id(to_id)
    to_user_name = to_user.get_full_name()

    message = context['message']
    room = get_room(str(current_user.id), to_id)

    print(f"Message from user: {sender_name} \t To user: {to_user_name}\t Content: {message}")
    emit("message_send", {"from": sender_name, "to": to_user_name, "message": message}, room=room)


def get_room(sender, receiver):
    list = [sender, receiver]
    list.sort()
    return '#'.join(list)


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host='localhost', port=8080,
                 debug=app.config['ENV'] == 'development')
