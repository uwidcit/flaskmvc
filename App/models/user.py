from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_name = db.Column(db.String, nullable=False)
    exercise_image1 = db.Column(db.String, nullable=True)
    exercise_image2 = db.Column(db.String, nullable=True)
    muscle_group = db.Column(db.String, nullable=False)
    equipment = db.Column(db.String, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    description = db.Column(db.String, nullable=True)

    def __init__(self, exercise_name, exercise_image1, exercise_image2, muscle_group, equipment, rating, description):
        self.exercise_name = exercise_name
        self.exercise_image1 = exercise_image1
        self.exercise_image2 = exercise_image2
        self.muscle_group = muscle_group
        self.equipment = equipment
        self.rating = rating
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'exercise_name': self.exercise_name,
            'exercise_image1': self.exercise_image1,
            'exercise_image2': self.exercise_image2,
            'muscle_group': self.muscle_group,
            'equipment': self.equipment,
            'rating': self.rating,
            'description': self.description
        }

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    workout = db.relationship('Workout')

    def __init__(self, user_id, workout_id):
        self.user_id = user_id
        self.workout_id = workout_id

    def get_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'workout': self.workout.get_json()
        }

