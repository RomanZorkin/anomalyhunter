from flask import Flask

from service import config

app_config = config.load_from_env()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = app_config.secret_key

    return app
