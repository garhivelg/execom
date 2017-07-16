from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_script import Manager
from config import BASE_DIR, app_config


import logging
from logging.handlers import RotatingFileHandler


def create_logger(log_config=dict()):
    handler = RotatingFileHandler(
        log_config.get("FILENAME"),
        maxBytes=log_config.get("MAX_BYTES"),
        backupCount=log_config.get("BACKUP_COUNT"),
    )
    formatter = logging.Formatter(log_config.get("FORMAT"))
    handler.setFormatter(formatter)
    return handler


def create_app(debug=False, config_name='production'):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.static_folder = os.path.join(BASE_DIR, app.config.get('STATIC_FOLDER', 'static'))
    app.template_folder = os.path.join(BASE_DIR, app.config.get('TEMPLATE_FOLDER', 'templates'))
    
    # Session(app)

    db = SQLAlchemy(app)
    db.create_all()

    log_config = app.config.get("LOG", dict())
    app.logger.addHandler(create_logger(log_config))

    migrate = Migrate(app, db)

    # from execom import models

    return app, db


import os


debug = os.environ.get('FLASK_DEBUG', False)
config_name = os.environ.get('FLASK_CONFIG', 'production')
app, db = create_app(config_name=config_name)
manager = Manager(app)


from execom.commands import *
from execom.views import *
from case.views import *
