from os import path, environ
from dotenv import load_dotenv
import logging


BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, '.env'))


class Config:
    """ Flask configuration from environment variables """

    FLASK_APP = 'wsgi.py'
    SECRET_KEY = environ.get('SECRET_KEY')

    # Static assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # User session
    SESSION_PERMANENT = environ.get('SESSION_PERMANENT')


class Logging:
    """ Logging configuration """

    FILENAME = 'app.log'
    LEVEL = logging.INFO
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    DATE_FORMAT = '%d-%b-%y %H:%M:%S'
