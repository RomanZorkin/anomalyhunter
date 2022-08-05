from flask import Flask

from service import config
from service.views import index

app_config = config.load_from_env()


def create_app() -> Flask:
    app = Flask(__name__)

    app.config['SECRET_KEY'] = app_config.secret_key

    app.register_blueprint(index.view, url_prefix='/')

    return app
