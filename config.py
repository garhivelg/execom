import os
from datetime import timedelta


# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.getcwd())


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db/execom.db'
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


class ProductionConfig(Config):
    pass


class DebugConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
