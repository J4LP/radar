import datetime
import os


class BaseConfig(object):
    """File based configuration object."""

    #: Application absolute path
    APP_DIR = os.path.abspath(os.path.dirname(__file__))

    #: Project root
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    #: Turn on debug mode by environment
    DEBUG = os.getenv('DEBUG', True)

    #: Default SQLAlchemy database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + PROJECT_ROOT + '/radar.sqlite'

    #: Turn on debug mode for SQLAlchemy (prints out queries)
    SQLALCHEMY_ECHO = os.getenv('DEBUG', False)
