from App.database import db

class UserFoodList(db.Model):
    __tablename__ = 'user_food_list'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ingredient = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, ingredient):
        self.user_id = user_id
        self.ingredient = ingredient

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'ingredient': self.ingredient
        }