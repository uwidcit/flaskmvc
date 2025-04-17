from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request

from App.models import User

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Convert user.id to string for JWT subject
        return create_access_token(identity=str(user.id))
    return None


def setup_jwt(app):
    jwt = JWTManager(app)

    # Identity handler - we store user ID in the token
    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return user_id

    # User lookup handler - we use the ID to get the user
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        # Convert string ID back to integer for database lookup
        return User.query.get(int(identity))

    return jwt


# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          user_id = get_jwt_identity()
          # Convert string ID to integer for database lookup
          current_user = User.query.get(int(user_id)) if user_id else None
          is_authenticated = current_user is not None
      except Exception as e:
          print(f"Auth error: {e}")
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)