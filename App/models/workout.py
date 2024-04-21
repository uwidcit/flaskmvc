from App.database import db

class Workout(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    muscle=db.Column(db.String(20),nullable=False)
    exercise=db.Column(db.String(30),nullable=False)
    difficulty=db.Column(db.String(20),nullable=False)
    beginner_sets=db.Column(db.String(50),nullable=False)
    intermediate_sets=db.Column(db.String(50),nullable=False)
    expert_sets=db.Column(db.String(50),nullable=False)
    equipment=db.Column(db.String(50),nullable=True)
    description=db.Column(db.String(1000),nullable=False)
    video=db.Column(db.String(120),nullable=False)
    # duration=db.Column(db.Integer,nullable=True,default=0)
    routine_id=db.Column(db.Integer, db.ForeignKey('routine.id'))
  

    def __init__(self,muscle,exercise,difficulty,beginner_sets,intermediate_sets,expert_sets,equipment,description,video, routine_id):
        self.muscle=muscle
        self.exercise=exercise
        self.difficulty=difficulty
        self.beginner_sets=beginner_sets
        self.intermediate_sets=intermediate_sets
        self.expert_sets=expert_sets
        self.equipment=equipment
        self.description=description
        self.video=video
        self.routine_id = routine_id

        
    def get_json(self,level=None):
        sets=None
        if level == 1:
            sets=f'Beginner:{self.beginner_sets}'
        if level == 2:
            sets=f'Intermediate:{self.intermediate_sets}'
        if level == 3:
            sets=f'Expert:{self.expert_sets}' 
        else:
            sets={
                'Beginner: ':self.beginner_sets,
                'Intermediate: ':self.intermediate_sets,
                'Expert: ':self.expert_sets
            }
        return {
            'Muscle: ':self.muscle,
            'Workout: ':self.exercise,
            'Difficulty: ':self.difficulty,
            'Sets:':sets,
            'Equipment: ':self.equipment,
            'Description: ':self.description,
            'Youtube Link: ':self.video
        }

###API TAGS####
# Muscles
# WorkOut
# Intensity_Level
# Beginner Sets
# Intermediate Sets
# Expert Sets
# Equipment
# Explaination
# Video
        