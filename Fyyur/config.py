import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# ///TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@127.0.0.1:5432/test'

# Added to stop SQLALCHEMY_TRACK_MODIFICATIONS message on CMD from showing
SQLALCHEMY_TRACK_MODIFICATIONS = False