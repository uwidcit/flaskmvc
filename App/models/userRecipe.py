from App.database import db

class UserRecipe(db.Model):
    user_recipe_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable = False)

    def __init__(self, user_id, recipe_id):
        self.user_id = user_id
        self.recipe_id = recipe_id

    def __repr__(self):
      return f'<UserRecipe {self.user_recipe_id} : {self.user_id} cook {self.recipe_id}>'

    def get_json(self):
        return{
            "user_id": self.user_id,
            "recipe_id": self.recipe_id
        }