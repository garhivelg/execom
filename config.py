import os
from datetime import timedelta
import locale


# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.getcwd())

try:
    locale.setlocale(locale.LC_ALL, 'russian')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "ThereIsNoSpoon"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db/execom.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite://'

    LOG = {
        "FILENAME": os.path.join(BASE_DIR, "log", "execom.log"),
        "MAX_BYTES": 10000,
        "BACKUP_COUNT": 10,
        "FORMAT": "%(asctime)s[%(levelname)s]:\t%(message)s\tin %(module)s at %(lineno)d",
    }

    BACKUP_TIME = timedelta(minutes=30)
    DB_PATH = os.path.join(BASE_DIR, "db")
    BACKUP_PATH = os.path.join(BASE_DIR, "db", "backup")
    DB_FILENAME = "privatisation.db"
    BACKUP_FILENAME = "privatisation-%s.db"

    VIEW_CASE = "edit_case"

    UPLOAD_PATH = os.path.join(BASE_DIR, "upload")


class ProductionConfig(Config):
    pass


class DebugConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True


app_config = {
    'development': DebugConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
