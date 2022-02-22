import os
from logging.config import dictConfig

# FLASK
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")  # nosec
APP_PORT = int(os.getenv("APP_PORT", "5000"))
APP_VERSION = os.getenv("APP_VERSION")

# MONGO
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")  # nosec
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))
MONGO_DB = os.getenv("MONGO_DB", "connection_app")
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASS = os.getenv("MONGO_PASS", "password")
MONGO_URI = (
    f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
)

# TWITTER
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "fake_token")

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
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
}
dictConfig(LOGGING)
