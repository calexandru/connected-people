import logging
from datetime import datetime

from flask import Flask
from flask import jsonify

from app import settings
from app.connect import UserConnectionException
from app.connect import UsersConnection
from app.mongo import MongoClient

logger = logging.getLogger(__name__)
flask_app = Flask(__name__)
mongo_client = MongoClient(flask_app, settings.MONGO_URI)


@flask_app.get("/health")
def health():
    stats = {"status": "running", "server_date": datetime.datetime.now()}
    if settings.APP_VERSION:
        stats["version"] = settings.APP_VERSION
    return stats


@flask_app.route("/connected/realtime/<dev1>/<dev2>", methods=["GET"])
def connected(dev1, dev2):
    try:
        users_connection = UsersConnection(dev1, dev2)
        result = users_connection.check()
        response = result.to_dict()
    except UserConnectionException as ex:
        response = {"errors": ex.errors_list}
    except Exception as ex:
        logger.error("Failed to find connection between %s and %s. Reason: %s", dev1, dev2, ex)
        response = {"errors": [f"error trying to find connection between {dev1} and {dev2}"]}
    mongo_client.record_response(dev1, dev2, response)
    return jsonify(response)


@flask_app.route("/connected/register/<dev1>/<dev2>", methods=["GET"])
def register(dev1, dev2):
    try:
        response = mongo_client.get_history(dev1, dev2)
    except Exception as ex:
        logger.error("Failed to find connection between %s and %s. Reason: %s", dev1, dev2, ex)
        response = {
            "errors": [f"error trying to find history invocation for handlers {dev1} and {dev2}"]
        }
    return jsonify(response)
