from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from App.main import create_app, init_db
from App.models import db, User
from App.controllers import create_users
from App.controllers import register_admin

app = create_app()
init_db(app)

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
    app.run(host='0.0.0.0', port=8080, debug=app.config['ENV']=='development')

@manager.command
def make_users():
    create_users([
        {
            'first_name':'Bob',
            'last_name':'Smith',
            'email':'bob@mail.com',
            'password':'bobpass'
        },
        {
            'first_name':'Jame',
            'last_name':'Smith',
            'email':'jane@mail.com',
            'password':'janepass'
        },
        {
            'first_name':'Rick',
            'last_name':'Smith',
            'email':'rick@mail.com',
            'password':'rickpass'
        }
    ])
    print("users created")


# CREATE ADMIN FROM CONTROLLER
@manager.command
def createAdmin():
    n1 = input('Enter ADMIN firstname :')
    print (n1)
    n2 = input('Enter ADMIN lastname :')
    print (n2)
    e1 = input('Enter ADMIN email :')
    print (e1)
    p1 = input('Enter ADMIN password :')
    print (p1)

    fname1 = User(first_name=n1)
    fname2 = User(last_name=n2)
    email1 = User(email=e1)
    pass1 = User(password=p1)
    
    admin = register_admin(n1,n2,e1,p1)
    return admin

if __name__ == "__main__":
    manager.run()
