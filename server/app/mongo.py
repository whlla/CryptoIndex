from pymongo import MongoClient

from app.config import get_mongo_config


def initialize():
    global mongo_db
    mongo_db = MongoDb()


class MongoDb:
    def __init__(self):
        # get mongo configuration
        user, passwd, auth_db, host = get_mongo_config()

        # create mongo client
        self.client = MongoClient("mongodb://{}:{}@{}/{}".format(
            user,
            passwd,
            host,
            auth_db
        ))
