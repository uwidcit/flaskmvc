import os
import importlib


# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import  SQLALCHEMY_DATABASE_URI, SECRET_KEY, JWT_SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    else:
        config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
        config['DEBUG'] = config['ENV'].upper() != 'PRODUCTION'

    config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config['TEMPLATES_AUTO_RELOAD'] = True
    config['SEVER_NAME'] = '0.0.0.0'
    config['PREFERRED_URL_SCHEME'] = 'https'
    config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    return config

config = load_config()
