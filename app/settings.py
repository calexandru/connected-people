import os
from logging.config import dictConfig

# FLASK
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")  # nosec
APP_PORT = int(os.getenv("APP_PORT", "5000"))

# LOGGING
LOG_LEVEL = os.getenv("LOG_LEVEL") or "DEBUG"
LOGGING = {
    "version": 1,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s: %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "worker": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
            "propagate": False,
        }
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}
dictConfig(LOGGING)
