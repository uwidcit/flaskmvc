from App.database import db

class RecipeIngredient(db.Model):
    __tablename__ = 'recipe_ingredient'
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity_required = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, recipe_id, name, quantity_required=1):
        self.recipe_id = recipe_id
        self.name = name
        self.quantity_required = quantity_required

    def to_json(self):
        return {
            'id': self.id,
            'recipe_id': self.recipe_id,
            'name': self.name,
            'quantity_required': self.quantity_required
        }
