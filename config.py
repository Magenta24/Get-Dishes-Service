import os
from pathlib import Path

# Enabling CSRF protection
WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret-key-1234-#$%^'

# setting prject's base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True    