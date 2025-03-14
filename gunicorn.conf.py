import multiprocessing

import environ

# Take environment variables from .env file
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env('.env')

# A WSGI application path in pattern $(MODULE_NAME):$(VARIABLE_NAME)
wsgi_app = "mes.wsgi:application"
# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1
# The socket to bind
bind = "0.0.0.0:8000"
# Restart workers when code changes (development only!)
reload = env('GUNICORN_RELOAD')
# The Access log file to write to.
accesslog = env('GUNICORN_ACCESS_LOG')
# The Error log file to write to.
errorlog = env('GUNICORN_ERROR_LOG')
# Redirect stdout/stderr to log file
capture_output = True
# A filename to use for the PID file.
pidfile = env('GUNICORN_PID_FILE')
# Daemonize the Gunicorn process (detach & enter background)
daemon = False
