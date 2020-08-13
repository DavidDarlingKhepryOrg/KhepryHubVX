import os
from random import randrange

FLASK_DEBUG = True
FLASK_ENV = 'development'
FLASK_RUN_PORT = randrange(9000, 9999)
FLASK_SERVER_NAME = 'localhost'
SECRET_KEY = os.urandom(24).hex()
TEMPLATES_FOLDER = '../templates'

if FLASK_DEBUG:
    print(f"FLASK_DEBUG: {FLASK_DEBUG}")
    print(f"FLASK_ENV: {FLASK_ENV}")
    print(f"FLASK_RUN_PORT: {FLASK_RUN_PORT}")
    print(f"FLASK_SERVER_NAME: {FLASK_SERVER_NAME}")
