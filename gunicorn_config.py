# gunicorn_config.py
import multiprocessing

# The socket to bind.
# "0.0.0.0" to bind to all interfaces. 8000 is the port number.
bind = "0.0.0.0:8080"

# The number of worker processes for handling requests.
workers = 4

# Use the 'gevent' worker type for async performance.
worker_class = 'gevent'

# Log level
loglevel = 'info'

# Where to log to
accesslog = '-'  # '-' means log to stdout
errorlog = '-'  # '-' means log to stderr