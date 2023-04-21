# import os
# from flask import Flask
# #from flask_login import LoginManager, current_user
# from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
# from flask_cors import CORS
# from werkzeug.utils import secure_filename
# from werkzeug.datastructures import  FileStorage
# from datetime import timedelta

# from App.database import init_db
# from App.config import config

# # from App.controllers import (
# #     setup_jwt,
# #     setup_flask_login
# # )

# from App.controllers import setup_jwt

# from App.views import views

# def add_views(app):
#     for view in views:
#         app.register_blueprint(view)

# def configure_app(app, config, overrides):
#     for key, value in config.items():
#         if key in overrides:
#             app.config[key] = overrides[key]
#         else:
#             app.config[key] = config[key]

# def create_app(config_overrides={}):
#     app = Flask(__name__, static_url_path='/static')
#     configure_app(app, config, config_overrides)
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['TEMPLATES_AUTO_RELOAD'] = True
#     app.config['SEVER_NAME'] = '0.0.0.0'
#     app.config['PREFERRED_URL_SCHEME'] = 'https'
#     app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
#     CORS(app)
#     photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
#     configure_uploads(app, photos)
#     add_views(app)
#     init_db(app)
#     setup_jwt(app)
#     setup_flask_login(app)
#     app.app_context().push()
#     return app

# import os
# from flask import Flask
# from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
# from flask_cors import CORS
# from datetime import timedelta
# import flask_excel as excel

# from App.database import create_db

# from App.controllers import setup_jwt

# from App.views import views


# def add_views(app):
#     for view in views:
#         app.register_blueprint(view)


# def loadConfig(app, config):
#     app.config["ENV"] = os.environ.get("ENV", "DEVELOPMENT")
#     delta = 7
#     if app.config["ENV"] == "DEVELOPMENT":
#         app.config.from_object("App.config")
#         delta = app.config["JWT_EXPIRATION_DELTA"]
#     else:
#         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
#         app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
#         app.config["DEBUG"] = os.environ.get("ENV").upper() != "PRODUCTION"
#         app.config["ENV"] = os.environ.get("ENV")
#         delta = os.environ.get("JWT_EXPIRATION_DELTA", 7)

#     app.config["JWT_EXPIRATION_DELTA"] = timedelta(days=int(delta))

#     for key, value in config.items():
#         app.config[key] = config[key]


# def create_app(config={}):
#     app = Flask(__name__, static_url_path="/static")
#     CORS(app)
#     loadConfig(app, config)
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.config["TEMPLATES_AUTO_RELOAD"] = True
#     app.config["SEVER_NAME"] = "0.0.0.0"
#     app.config["PREFERRED_URL_SCHEME"] = "https"
#     app.config["UPLOADED_PHOTOS_DEST"] = "App/uploads"
#     photos = UploadSet("photos", TEXT + DOCUMENTS + IMAGES)
#     configure_uploads(app, photos)
#     excel.init_excel(app)
#     add_views(app)
#     create_db(app)
#     setup_jwt(app)
#     with app.app_context() as app_context:
#         from App.controllers.user import create_su, create_default_farmer
#         create_su()
#         create_default_farmer()
#         app_context.push()
#     return app

import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from flask_googlemaps import GoogleMaps
from flask_login import LoginManager

from App.controllers import setup_jwt, load_user_from_id
from App.database import init_db, get_migrate
from App.views import user_views, api_views

views = [user_views, api_views]


def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config["ENV"] = os.environ.get("ENV", "DEVELOPMENT")
    if app.config["ENV"] == "DEVELOPMENT":
        app.config.from_object("App.config")
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
        app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
        app.config["JWT_EXPIRATION_DELTA"] = timedelta(
            days=int(os.environ.get("JWT_EXPIRATION_DELTA"))
        )
        app.config["DEBUG"] = True
        app.config["ENV"] = "DEVELOPMENT"
        # app.config["GOOGLEMAPS_KEY"] = os.environ.get("GOOGLEMAPS_KEY")
    for key, value in config.items():
        app.config[key] = config[key]


def create_app(config={}):
    app = Flask(__name__, static_url_path="/static")
    CORS(app)
    loadConfig(app, config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["WTF_CSRF_ENABLED"] = False
    add_views(app, views)
    init_db(app)
    setup_jwt(app)
    app.app_context().push()
    return app


app = create_app()
login_manager = LoginManager(app)
GoogleMaps(app, key=os.environ.get("GOOGLEMAPS_KEY"))


@login_manager.user_loader
def load_user(user_id):
    return load_user_from_id(user_id)


migrate = get_migrate(app)