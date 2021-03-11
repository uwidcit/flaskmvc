import os
from flask import Flask
from flask_jwt import JWT
from datetime import timedelta 
from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT, DOCUMENTS

from App.models import db

from App.views import (
    api_views,
    user_views
)

def loadConfig(app):
    #try to load config from file, if fails then try to load from environment
    try:
        app.config.from_object('App.config')
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' if app.config['SQLITEDB'] else app.config['DBURI']
    except:
        print("config file not present using environment variables")
        DBURI = os.environ.get("DBURI")
        app.config['ENV'] = os.environ.get("ENV")
        SQLITEDB = os.environ.get("SQLITEDB", default="true")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' if SQLITEDB in {'True', 'true', 'TRUE'} else DBURI

def create_app():
    app = Flask(__name__, static_url_path='/static')
    loadConfig(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    db.init_app(app)
    return app

app = create_app()

app.app_context().push()

app.register_blueprint(api_views)
app.register_blueprint(user_views)

''' Set up JWT here (if using flask JWT)'''
# def authenticate(uname, password):
#   pass

# #Payload is a dictionary which is passed to the function by Flask JWT
# def identity(payload):
#   pass

# jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''