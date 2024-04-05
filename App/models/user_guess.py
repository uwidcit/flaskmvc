from App.database import db

class UserGuess(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    user_attempts = db.Column(db.Integer, nullable=False)
    gameNumber = db.Column(db.Integer, nullable=False, unique=True)
    puzzle = db.relationship('Puzzle', backref='Game', lazy=True)

    def __init__(self, puzzle_id, user_attempts, gameNumber, puzzle):
        self.puzzle_id = puzzle_id
        self.user_attempts = user_attempts
        self.gameNumber = gameNumber
        self.puzzle = puzzle
    
    def __repr__(self):
        return f'Game {self.id} : {self.puzzle_id} Game Count: {self.gameNumber}>'

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