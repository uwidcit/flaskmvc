from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import random

db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

def create_db(app):
    db.init_app(app)
    db.create_all(app=app)
    
def init_db(app):
    db.init_app(app)


with open("/workspace/flaskmvc/App/dictionary.txt",'r') as words:
  lines = words.readlines()

  wList=[]
  i=0
  while i<len(lines):
    if(len(lines[i])<=9 and len(lines[i])>=5 and lines[i].__contains__("-")==False):
        print(lines[i][0:len(lines)-1])
      #try:
       #     db.session.add(lines[0:len(lines)-1])
        #    db.session.commit()
        #except IntegrityError:
         #   db.session.rollback()
          #  print('Pokemon exists No change')
    
    i+=1
