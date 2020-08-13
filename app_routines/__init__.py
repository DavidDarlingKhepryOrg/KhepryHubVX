import os
from random import randrange
from flask import Flask

from dbase_routines import init_app
from app_settings import flask_settings


def create_app(test_config=None):
    _app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder=flask_settings.TEMPLATES_FOLDER
    )
    _app.config.from_mapping(
        DATABASE=os.path.join(_app.instance_path, 'voters.sqlite3'),
        FLASK_DEBUG=flask_settings.FLASK_DEBUG,
        FLASK_RUN_PORT=flask_settings.FLASK_RUN_PORT,
        FLASK_SERVER_NAME=flask_settings.FLASK_SERVER_NAME,
        SECRET_KEY=flask_settings.SECRET_KEY
    )

    if test_config is None:
        _app.config.from_object(flask_settings)
    else:
        _app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(_app.instance_path)
    except OSError:
        pass

    init_app(_app)

    return _app
