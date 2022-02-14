import logging
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List

from flask_pymongo import DESCENDING
from flask_pymongo import PyMongo

logger = logging.getLogger(__name__)


class MongoClient:
    def __init__(self, flask_app, mongo_uri: str):
        self.client = PyMongo(
            flask_app, uri=mongo_uri, serverSelectionTimeoutMS=1000, connect=False
        )

    def record_response(self, handler_1: str, handler_2: str, response: Dict[str, Any]):
        self.client.db.register.insert_one(
            {
                "handler_1": handler_1,
                "handler_2": handler_2,
                "data": {"registered_at": datetime.now(), **response},
            }
        )

    def get_history(self, handler_1: str, handler_2: str) -> List[Dict[str, Any]]:
        return list(
            map(
                lambda x: x.get("data"),
                self.client.db.register.find(
                    {"handler_1": handler_1, "handler_2": handler_2}, {"data": 1}
                ).sort("data.registered_at", DESCENDING),
            )
        )
