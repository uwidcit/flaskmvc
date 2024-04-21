# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .testing import testing_views
from .workouts import workout_views
from .routine import routine_views
from .all_workouts import all_workouts_views





views = [user_views,
    index_views, 
    auth_views,
    workout_views,
    routine_views,
    all_workouts_views] 
# blueprints must be added to this list