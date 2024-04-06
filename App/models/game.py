from App.database import db
from App.constants import MIN_CODE_VALUE, MAX_CODE_VALUE, MIN_CODE_LENGTH, MAX_CODE_LENGTH
from sqlalchemy.orm import validates
from random import randint
from datetime import date

class Game(db.Model):
    __MIN_ATTEMPTS = 5

    @property
    def answer_length(self):
        return len(self.answer)

    id = db.Column(db.Integer, primary_key=True)
    creation_date = db.Column(db.Date, nullable=False, unique=True, default=date.today)
    max_attempts = db.Column(db.Integer, db.CheckConstraint(f"max_attempts >= {__MIN_ATTEMPTS}"), nullable=False)

    # NOTE: Answer must be stored as a string instead of an int to preserve any leading zeroes
    answer = db.Column(db.String(MAX_CODE_LENGTH), db.CheckConstraint(
        f"answer >= {MIN_CODE_VALUE} AND answer <= {MAX_CODE_VALUE} AND LENGTH(answer) >= {MIN_CODE_LENGTH} AND LENGTH(answer) <= {MAX_CODE_LENGTH}"),
        nullable=False)

    guesses = db.relationship('UserGuess', back_populates='game_relation', cascade="all, delete-orphan")

    def __init__(self, max_attempts, preset_answer=None, answer_length=None):
        self.max_attempts = max_attempts

        # To preset an answer instead of randomly generating one, provide a value to the answer field.
        # Note that if an answer is preset, the value of the answer length parameter is discarded/ignored.
        if preset_answer is not None:
            self.answer = preset_answer
        
        # If a specific answer is not provided, the answer is randomly generated using the provided answer
        #     length which MUST be provided (see generate_answer() method for error handling).
        else:
            try:
                self.answer = self.generateAnswer(answer_length)
            except ValueError as e:
                raise ValueError(e)    # Error handling done by the object instatiator

    def __repr__(self):
        return f'Game({self.max_attempts} : {self.answer})'
    
    def __str__(self):
        return f"""
Game Info:
    |- ID: {self.id}
    |- Creation Date: {self.creation_date}
    |- Max Attempts: {self.max_attempts}
    |- Answer: {self.answer}
"""
    
    def get_json(self):
        return {
            'id' : self.id,
            'creation_date': {self.creation_date},
            'max_attempts': self.max_attempts,
            'answer': self.answer,
        }
    
    # Validation decorator function guide: https://stackoverflow.com/questions/73663939/is-there-a-way-to-specify-min-and-max-values-for-integer-column-in-slqalchemy
    # Related official documentation: https://docs.sqlalchemy.org/en/14/orm/mapped_attributes.html#simple-validators

    # Note these functions are NOT called directly, but are instead invoked automatically by SQLAlchemy when assigning the respective attribute

    @validates("max_attempts")
    def validate_max_attempts(self, key, value):
        if value < self.__MIN_ATTEMPTS:
            raise ValueError(f"expected max_attempts to have a minimum value of <{self.__MIN_ATTEMPTS}>; recieved <{value}>")
        return value
    
    @validates("answer")
    def validate_answer(self, key, value):
        """
        Validate a preset answer to ensure adherance to game constraints.

        Args:
            key (str or int): The user's guess, which should be convertible to an integer in the valid range
            value (str or int): The user's guess, which should be convertible to an integer in the valid range

        Returns:
            bool: True if the guess passes all validation checks.

        Raises:
            ValueError: If the guess fails any of the validation constraints.
        """
        try:
            # Attempt to convert the answer string to an integer to check range validity
            value_int = int(value)
        except ValueError:
            # Answer contained invalid characters or was the wrong type
            raise ValueError(f"could not cast answer of type <{value.__class__.__name__}> to type int")
        
        if not MIN_CODE_VALUE <= value_int <= MAX_CODE_VALUE:
            raise ValueError(f"expected answer to be within the range <{MIN_CODE_VALUE:0{MIN_CODE_LENGTH}d}> to <{MAX_CODE_VALUE}>, inclusive; recieved <{value}>")
        
        if not MIN_CODE_LENGTH <= value_int <= MAX_CODE_LENGTH:
            raise ValueError(f"expected answer length to be within <{MIN_CODE_LENGTH}> to <{MAX_CODE_LENGTH}> digits, inclusive; recieved <{value}>")
        
        # Return the original string if all validation checks succeeded
        return value
    
    @validates("answer_length")
    def validate_answer_length(self, key, value):
        if not MIN_CODE_LENGTH <= value <= MAX_CODE_LENGTH:
            raise ValueError(f"expected answer length to be within the range <{MIN_CODE_LENGTH}> to <{MAX_CODE_LENGTH}> digits, inclusive; recieved <{value}> digits")
        return value
    
    def generate_answer(self, answer_length):
        """
        Generate a random answer with the specified number of digits that adheres to the game's constraints.

        Args:
            answer_length (str or int): The number of digits which should be convertible to a positive integer.

        Returns:
            bool: True if the guess passes all validation checks.

        Raises:
            ValueError: If the guess fails any of the validation constraints.
        """
        if answer_length is None:
            raise ValueError("MUST provide an answer length for random generation if not providing a specific answer")

        try:
            answer_length = int(answer_length)
        except ValueError:
            # answer_length contained invalid characters or was the wrong type
            raise ValueError(f"could not cast answer length of type <{answer_length.__class__.__name__}> to type int")
        
        if not (MIN_CODE_LENGTH <= answer_length <= MAX_CODE_LENGTH):
            raise ValueError(f"expected answer length to be within <{MIN_CODE_LENGTH}> and <{MAX_CODE_LENGTH}> digits, inclusive; recieved <{answer_length}> digits")
        
        used_digits = set()
        result = 0
        
        # Each position should have a unique digit
        while len(result) < answer_length:
            temp = randint(0, 9)
            if temp not in used_digits:
                used_digits.add(temp)
                result = (result * 10) + temp

        return result        
    
    def __validateGuess(self, guess):
        """
        Validate a user guess to ensure adherance to game constraints.

        Args:
            guess (str or int): The user's guess, which should be convertible to an integer in the valid range

        Returns:
            bool: True if the guess passes all validation checks.

        Raises:
            ValueError: If the guess fails any of the validation constraints.
        """
        try:
            guess = int(guess)

        except ValueError:
            # guess contained invalid characters or was the wrong type
            raise ValueError(f"guess of type <{guess.__class__.__name__}> could not be cast to type int")
        
        # Convert guess to a string to count its digits
        guess_str = str(guess)
        guess_length = len(guess_str)

        # Check if the guess length is the same as the answer length
        if guess_length != self.answer_length:
            raise ValueError(f"expected guess to have <{self.answer_length}> digits; recieved <{guess_length}> digits; )")
        
        # Check if the guess value is within the valid range
        if not (MIN_CODE_LENGTH <= guess <= MAX_CODE_LENGTH):
            raise ValueError(f"expected guess to be within <{MIN_CODE_LENGTH:0{MIN_CODE_LENGTH}d}> and <{MAX_CODE_LENGTH}>, inclusive; recieved <{guess}>)")
        
        # Check if all digits in the guess are unique
        used_digits = set()
        for digit in guess_str:
            if digit in used_digits:
                raise ValueError(f"expected each digit of the guess <{guess}> to be unique")
            used_digits.add(digit)

        return True       
        
    # Evaluates the bull, cow, and milk values for the given guess, assuming __validateGuess() returns True,
    # If the guess is valid, the above values are returned using a dictionary
    def evaluateGuess(self, guess):
        """
        Evaluates the accuracy of a user's guess compared to the correct answer

        Args:
            guess (str or int): The user's guess, which should be convertible to an integer in the valid range

        Returns:
            dict: A dictionary containing the evaluation results with the following keys:
                - "bulls": Number of correct characters in the correct position.
                - "cows": Number of correct characters in the wrong position.
                - "milk": Number of incorrect characters.

        Raises:
            ValueError: If the guess fails any of the validation constraints.
        """
        results = {"bulls" : 0, "cows" : 0, "milk" : 0,}

        try:
            if (self.__validateGuess(guess)):
                guess = str(guess)
                ans_str = str(self.answer)

                for g, a in zip(guess, ans_str):
                    if g == a:
                        results["bulls"] += 1
                    else:
                        if g in ans_str:
                            results["cows"] += 1
                        else:
                            results["milk"] += 1

                return results          
        except ValueError as e:
            # Error handling done by the caller function (i.e., the route)
            raise e
