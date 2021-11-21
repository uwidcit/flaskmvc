from App.models import User

def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user

# Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload['identity'])
