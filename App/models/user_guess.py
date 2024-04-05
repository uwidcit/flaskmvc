from App.database import db
from sqlalchemy.orm import validates

class UserGuess(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    guess = db.Column(db.Integer, db.CheckConstraint("guess >= 0123 AND guess <= 9876543210"), nullable=False)
    user_relation = db.relationship("User", back_populates="guess")
    game_relation = db.relationship("Game", back_populates="guess")

    def __init__(self, user_id, game_id, guess):
        self.user_id = user_id
        self.user_attempts = game_id
        self.guess = guess
    
    def __repr__(self):
        return f'UserGuess({self.user_id}, {self.game_id}, {self.guess})'
    
    def __str__(self):
        return f"""
User Guess Info:
    |- User ID: {self.user_id}
    |- Game ID: {self.game_id}
    |- Guess: {self.guess}
"""
    
    def get_json(self):
        return {
            'user_id' : self.user_id,
            'game_id': self.game_id,
            'guess': self.guess
        }
    
    # Validation function source: https://stackoverflow.com/questions/73663939/is-there-a-way-to-specify-min-and-max-values-for-integer-column-in-slqalchemy
    # Related official documentation: https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html#simple-validators
    @validates("guess")
    def validate_guess(self, key, value):
        # Only checks to see if the guess matches the same general constraints applied to the answer
        # DOES NOT evaluate to check if the guess is right or wrong regarding the game

        if not 123 <= value <= 9_876_543_210:    # valid codes range from 0123 (4 digits) to 9_876_543_210 (10 digits); all digits unique
            raise ValueError(f"answer <{value}> is invalid")
        return value
