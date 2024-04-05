from App.database import db
from sqlalchemy.orm import validates

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    max_attempts = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.Integer, db.CheckConstraint("code_length >= 0123 AND code_length <= 9876543210"), nullable=False)
    answer_length = db.Column(db.Integer, db.CheckConstraint("code_length >= 3 AND code_length <= 10"), nullable=False)

    def __init__(self, max_attempts, answer):
        self.max_attmepts = max_attempts
        self.answer = answer
        self.answer_length = len(str(answer))
    
    def __repr__(self):
        return f'Game({self.max_attempts} : {self.answer})'
    
    def __str__(self):
        return f"""
Game Info:
    |- ID: {self.id}
    |- Max Attempts: {self.max_attempts}
    |- Answer: {self.answer}
    |- Answer length: {self.answer_length}
"""
    
    # Validation function source: https://stackoverflow.com/questions/73663939/is-there-a-way-to-specify-min-and-max-values-for-integer-column-in-slqalchemy
    # Related official documentation: https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html#simple-validators
    @validates("answer")
    def validate_answer(self, key, value):
        if not 123 < value < 9_876_543_210:    # valid codes range from 0123 (4 digits) to 9_876_543_210 (10 digits); all digits unique
            raise ValueError(f"answer <{value}> is invalid")
        return value

    def start_timer():
        pass

    def get_json(self):
        return {
            'id' : self.id,
            'puzzle_id': self.puzzle_id,
            'user_attempts': self.user_attempts,
            'gameNumber': self.gameNumber,
            'puzzle': self.puzzle.puzzle_code
        }

class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_code = db.Column(db.String(10), nullable=False, unique=True)

    def __init__(self, puzzle_code):
        self.puzzle_code = puzzle_code
    
    def generate_puzzle():
        pass

    def get_puzzle():
        pass
    
    def get_json(self):
        return {
            'id': self.id,
            'puzzle_code': self.puzzle_code
        }