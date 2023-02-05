from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

def create_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def drop_db():
    db.drop_all()
    
def init_db(app):
    db.init_app(app)