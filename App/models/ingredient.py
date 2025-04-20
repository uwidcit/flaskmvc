from App.database import db

class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(225), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable = False)

    def __init__(self, name, recipe_id):
        self.ingredient_name = name
        self.recipe_id = recipe_id

    def get_json(self):
        return{
            "ingredient_id": self.ingredient_id,
            "ingredient_name": self.ingredient_name
        }