from App.models import User
from flask_login import UserMixin

class Student(UserMixin, User):
    
    def __init__(self):
        super().__init__() #need to populate arguments