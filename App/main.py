import os
from flask import Flask
from flask_login import LoginManager, current_user
from flask_uploads import DOCUMENTS, IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from datetime import timedelta
from flask import Flask, request, render_template
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from App.models.user import User
from App.database import create_db, get_migrate

from App.controllers import (
    setup_jwt
)

from App.views import (
    user_views,
    api_views
)

views = [
    user_views,
    api_views
]

def add_views(app, views):
    for view in views:
        app.register_blueprint(view)


def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    if app.config['ENV'] == "DEVELOPMENT":
        app.config.from_object('App.config')
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['JWT_EXPIRATION_DELTA'] =  timedelta(days=int(os.environ.get('JWT_EXPIRATION_DELTA')))
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['UPLOADED_PHOTOS_DEST'] = "App/uploads"
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    add_views(app, views)
    create_db(app)
    setup_jwt(app)
    app.app_context().push()
    return app

app = create_app()
migrate = get_migrate(app)

''' Set up JWT here '''
def authenticate(uname, password):
  #search for the specified user
  user = User.query.filter_by(username=uname).first()
  #if user is found and password matches
  if user and user.check_password(password):
    return user

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/app')
def client_app():
  return app.send_static_file('Login.html')

@app.route('/')
def login():
  return render_template('Login.html')

@app.route('/game')
#@jwt_required()
def playgame():
    with open("/workspace/flaskmvc/App/dictionary.txt",'r') as words:
        lines = words.readlines()

    wList=[]
    i=0
 
    while i<len(lines):
        if(len(lines[i])<=9 and len(lines[i])>=5 and lines[i].__contains__("-")==False and lines[i].__contains__("(")==False):
            wList.append(lines[i].rstrip())

        i+=1  
    return render_template('Game.html',word1=wList)

@app.route('/scores')
def showscores():
    result = []
    i=1
    while(i<20):
        result.append(User.query.get(i))
        i+=1
    
    return render_template('High Score.html',result=result)        

