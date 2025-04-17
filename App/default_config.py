SQLALCHEMY_DATABASE_URI="sqlite:///temp-database.db"
SECRET_KEY="secret key"

# JWT settings
JWT_SECRET_KEY = "your-super-secret-key"  # Change this in production!
JWT_TOKEN_LOCATION = ["headers", "cookies"]  # Accept JWT from both headers and cookies
JWT_ACCESS_COOKIE_NAME = "access_token"
JWT_COOKIE_CSRF_PROTECT = False  # Disable CSRF protection for development
JWT_COOKIE_SECURE = False  # Don't require HTTPS for cookies in development