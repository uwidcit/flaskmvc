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

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

exercise_routine = db.Table('exercise_routine',
    db.Column('routine_id', db.Integer, db.ForeignKey('routine.id'), primary_key=True),
    db.Column('exercise_id', db.Integer, db.ForeignKey('exercise.id'), primary_key=True)
)

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('routines', lazy=True))
    exercises = db.relationship('Exercise', secondary=exercise_routine, backref=db.backref('routines', lazy=True))

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'exercises': [exercise.to_dict() for exercise in self.exercises]
        }

    def add_exercise(self, exercise):
        if exercise not in self.exercises:
            self.exercises.append(exercise)
            db.session.commit()

    def remove_exercise(self, exercise):
        if exercise in self.exercises:
            self.exercises.remove(exercise)
            db.session.commit()