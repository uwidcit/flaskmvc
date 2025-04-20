from App.database import db

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(225))
    directions = db.Column(db.String(1000))
    total_time_taken = db.Column(db.Integer)
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) #not using it like this as the todo list allocation is predefined
    ingredients = db.relationship('Ingredient', backref='recipe', cascade="all, delete-orphan")
    user = db.relationship('UserRecipe', backref='recipe', lazy=True)

    def __init__(self, name, directions, time):
        self.recipe_name = name
        self.directions = directions
        self.total_time_taken = time

    def get_json(self):
        return{
            "recipe_id": self.recipe_id,
            "recipe_name": self.recipe_name,
            "directions": self.directions,
            "total_time_taken": self.total_time_taken
        }