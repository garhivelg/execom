import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)


# SQLALCHEMY_DATABASE_URI = 'sqlite:///db/privatisation.db'
SQLALCHEMY_DATABASE_URI = 'sqlite://'


LOG = {
    "FILENAME": os.path.join(basedir, "log", "privatisation.log"),
    "MAX_BYTES": 10000,
    "BACKUP_COUNT": 10,
    "FORMAT": "%(asctime)s[%(levelname)s]:\t%(message)s\tin %(module)s at %(lineno)d",
}

BACKUP_TIME = timedelta(minutes=30)
DB_PATH = os.path.join(basedir, "db")
BACKUP_PATH = os.path.join(DB_PATH, "backup")
DB_FILENAME = "privatisation.db"
BACKUP_FILENAME = "privatisation-%s.db"
