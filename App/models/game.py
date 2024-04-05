from App.database import db
from sqlalchemy.orm import validates
from random import randint

class Game(db.Model):
    MIN_ANSWER_LENGTH = 4
    MAX_ANSWER_LENGTH = 10

    id = db.Column(db.Integer, primary_key=True)
    max_attempts = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.Integer, db.CheckConstraint("code_length >= 0123 AND code_length <= 9876543210"), nullable=False)
    answer_length = db.Column(db.Integer, db.CheckConstraint(f"answer_length >= {MIN_ANSWER_LENGTH} AND answer_length <= {MAX_ANSWER_LENGTH}"), nullable=False)
    guess = db.relationship('UserGuess', back_populates='game_relation', cascade="all, delete-orphan")

    def __init__(self, max_attempts, answer=None, answer_length=None):
        self.max_attempts = max_attempts

        # To specify an answer, provide a value to the answer field.
        # Note that in this case, the value in the answer length field will be discarded
        #   in favour of calculating it from the specified answer.
        if answer is not None:
            self.answer = answer
            self.answer_length = len(str(answer))
        
        # If a specific answer is not provided, the answer is randomly generated
        #   using the provided answer length which MUST be provided.
        else:
            if answer_length is None:
                raise ValueError("MUST provide an answer length for random generation if not providing a specific answer")
            self.answer = self.generateAnswer(answer_length)

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
    
    def get_json(self):
        return {
            'id' : self.id,
            'max_attempts': self.max_attempts,
            'answer': self.answer,
            'answer_length': self.answer_length
        }
    
    # Validation function source: https://stackoverflow.com/questions/73663939/is-there-a-way-to-specify-min-and-max-values-for-integer-column-in-slqalchemy
    # Related official documentation: https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html#simple-validators
    @validates("answer")
    def validate_answer(self, key, value):
        if not 123 <= value <= 9_876_543_210:    # valid codes range from 0123 (4 digits) to 9_876_543_210 (10 digits); all digits unique
            raise ValueError(f"answer <{value}> is invalid")
        return value
    
    def generate_answer(self, answer_length):
        try:
            answer_length = int(answer_length)
        except ValueError as e:
            raise ValueError(e)
        
        if not (self.MIN_ANSWER_LENGTH <= answer_length <= self.MAX_ANSWER_LENGTH):
            raise ValueError("invalid answer length provided")
        
        used_digits = []
        result = 0
        
        while len(result) < answer_length:
            temp = randint(0, 9)
            if temp not in used_digits:
                used_digits.append(temp)
                result = (result * 10) + temp
        return result        
    
    """
    def start_timer():
        pass
    """

"""
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
"""