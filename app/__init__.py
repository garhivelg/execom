from flask import Flask
from flask_sqlalchemy import SQLAlchemy


import os
import logging
from logging.handlers import RotatingFileHandler


def create_app(debug=False, config='config.ProductionConfig'):
    app = Flask(__name__)
    if debug:
        app.config.from_object('config.DebugConfig')
    else:
        app.config.from_object(config)

    # Session(app)

    db = SQLAlchemy(app)
    db.create_all()

    log_config = app.config.get("LOG", dict())
    handler = RotatingFileHandler(
        log_config.get("FILENAME"),
        maxBytes=log_config.get("MAX_BYTES"),
        backupCount=log_config.get("BACKUP_COUNT"),
    )
    formatter = logging.Formatter(log_config.get("FORMAT"))
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    return app, db


debug = os.environ.get('FLASK_DEBUG', False)
app, db = create_app(debug=debug)


from case import views
