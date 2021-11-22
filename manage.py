from flask_login import login_manager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from App.controllers.user_controller import create_user
from App.main import create_app, init_db, create_sockets, create_login_manager, socketio, app
from App.controllers import create_users
from App.database import db

# app = create_app()
# init_db(app)
# socketio = create_sockets(app)
# login_manager = create_login_manager(app)

manager = Manager(app)
migrate = Migrate(app, db)

# add migrate command
manager.add_command('db', MigrateCommand)

# initDB command


@manager.command
def initDB():
    db.create_all(app=app)
    print('database initialized!')

# serve command


@manager.command
def serve():
    print('Application running in '+app.config['ENV']+' mode')
    socketio.run(app, host='localhost', port=8080,
                 debug=app.config['ENV'] == 'development')


@manager.command
def addAdmin():
    admin = create_user("Jo", "Slam", "joslam@test.com", "password123")
    return admin


@manager.command
def make_users():
    create_users([
        {
            'first_name': 'Bob',
            'last_name': 'Smith',
            'email': 'bob@mail.com',
            'password': 'bobpass',
        },
        {
            'first_name': 'Jame',
            'last_name': 'Smith',
            'email': 'jane@mail.com',
            'password': 'janepass',
        },
        {
            'first_name': 'Rick',
            'last_name': 'Smith',
            'email': 'rick@mail.com',
            'password': 'rickpass',
        }
    ])
    print("users created")


if __name__ == "__main__":
    manager.run()
