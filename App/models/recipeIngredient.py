from App.database import db

class RecipeIngredient(db.Model):
    ri_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable = False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.ingredient_id'), nullable = False)

    def __init__(self, recipe_id, ingredient_id):
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id

    def get_json(self):
        return{
            "recipe_ingredient_id": self.ri_id,
            "recipe_id": self.recipe_id,
            "ingredient_id": self.ingredient_id
        }
