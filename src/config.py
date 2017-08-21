# import sys
import os
from datetime import timedelta
import locale


# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASE_DIR = os.path.abspath(os.getcwd())
# if getattr(sys, 'frozen', False):
#     BASE_DIR = os.path.dirname(sys.executable)
# else:
#     BASE_DIR = os.path.dirname(__file__)

try:
    locale.setlocale(locale.LC_ALL, 'russian')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "ThereIsNoSpoon"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///db/execom.db'

    LOG = {
        "FILENAME": os.path.join(BASE_DIR, "log", "execom.log"),
        "MAX_BYTES": 1024 * 1024,
        "BACKUP_COUNT": 10,
        "FORMAT": "%(asctime)s[%(levelname)s]:\t%(message)s\tin %(module)s at %(lineno)d",
    }

    BACKUP_TIME = timedelta(minutes=30)
    DB_PATH = os.path.join(BASE_DIR, "db")
    BACKUP_PATH = os.path.join(BASE_DIR, "db", "backup")
    DB_FILENAME = "execom.db"
    BACKUP_FILENAME = "execom-%s.db"
    # SQLALCHEMY_DATABASE_URI = "sqlite:////%s/%s" % (DB_PATH, DB_FILENAME)
    SQLALCHEMY_DATABASE_URI = "sqlite:///../db/%s" % (DB_FILENAME)
    # SQLALCHEMY_DATABASE_URI = "sqlite:///db/%s" % (DB_FILENAME)

    VIEW_CASE = "edit_case"

    UPLOAD_PATH = os.path.join(BASE_DIR, "upload")

    RECORDS_ON_PAGE = 50


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
