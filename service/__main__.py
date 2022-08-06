import logging

from service import config
from service.app import create_app

app_config = config.load_from_env()

logging.basicConfig(level=logging.DEBUG)


def run() -> None:
    web_config = app_config.web
    app = create_app()
    app.run(host=web_config.app_host, port=web_config.app_port, debug=web_config.debug)


if __name__ == '__main__':
    run()
