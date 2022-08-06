import os
from pathlib import Path

from pydantic import BaseModel


class WebConfig(BaseModel):
    app_host: str
    app_port: int
    debug: bool
    secret_key: str


class PathConfig(BaseModel):
    upload_dir = Path('service/data/import')


class AppConfig(BaseModel):
    web: WebConfig
    path: PathConfig


def load_from_env() -> AppConfig:
    return AppConfig(
        web=WebConfig(
            app_host=os.environ['APP_HOST'],
            app_port=int(os.environ['APP_PORT']),
            debug=os.getenv('DEBUG', 'False'),
            secret_key=os.environ['SECRET_KEY'],
        ),
        path=PathConfig(),
    )


config = load_from_env()
