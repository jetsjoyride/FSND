import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

PGHOST = 'localhost'
PGDATABASE = 'trivia'
PGUSER = 'postgres'
PGPASSWORD = 'postgres'
connection = 'postgresql://' + PGUSER + ':' + PGPASSWORD + '@' + PGHOST + ':5432/' + PGDATABASE

SQLALCHEMY_DATABASE_URI = connection
SQLALCHEMY_TRACK_MODIFICATIONS = False
