import argparse

from gunicorn.app.base import BaseApplication

from app import settings
from app.api import flask_app


def run_server():
    flask_app.run(host=settings.APP_HOST, port=settings.APP_PORT)


def run_gunicorn_server():

    # Gunicorn relies on the operating system to provide all of the load balancing
    # when handling requests.
    # Generally we recommend (2 x $num_cores) + 1 as the number of workers
    WORKERS = 4  # (multiprocessing.cpu_count() * 2) + 1

    class GunicornApplication(BaseApplication):
        def load_config(self):
            self.cfg.set("bind", f"{settings.APP_HOST}:{settings.APP_PORT}")
            self.cfg.set("accesslog", "-")
            self.cfg.set("workers", WORKERS)

        def load(self):
            return flask_app

        def init(self, parser, opts, args):
            return


if __name__ == "__main__":
    command_map = {
        "runserver": run_server,
        "gunicornserver": run_gunicorn_server,
    }
    parser = argparse.ArgumentParser(
        prog="manage.py", description="This is the main entrypoint to the API"
    )
    parser.add_argument(
        "command", type=str, choices=command_map.keys(), help="what command would you like to run?"
    )
    args = parser.parse_args()
    command_map[args.command]()
