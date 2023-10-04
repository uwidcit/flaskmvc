# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .course import course_views
from .staff import staff_views


views = [user_views, index_views, auth_views, course_views, staff_views] 
# blueprints must be added to this list