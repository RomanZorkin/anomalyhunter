import logging

from service import config
from service.app import create_app

app_config = config.load_from_env()

logging.basicConfig(level=logging.DEBUG)


def run() -> None:
    app = create_app()
    app.run(host=app_config.app_host, port=app_config.app_port, debug=app_config.debug)


if __name__ == '__main__':
    run()
