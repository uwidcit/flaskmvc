from App.database import db

class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(225), nullable=False)
    ingredient_recipe = db.relationship('RecipeIngredient', backref='ingredient', lazy=True)

    def __init__(self, name):
        self.ingredient_name = name

    def get_json(self):
        return{
            "ingredient_id": self.ingredient_id,
            "ingredient_name": self.ingredient_name
        }
