import os

from pydantic import BaseModel


class AppConfig(BaseModel):
    app_host: str
    app_port: str
    debug: bool
    secret_key: str


def load_from_env() -> AppConfig:
    return AppConfig(
        app_host=os.environ['APP_HOST'],
        app_port=os.environ['APP_PORT'],
        debug=os.getenv('DEBUG', 'False'),
        secret_key=os.environ['SECRET_KEY'],
    )


config = load_from_env()