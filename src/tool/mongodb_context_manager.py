import certifi
from pymongo import MongoClient


mongo_db_url : str = "mongodb+srv://admin:emm05235@cluster0.umzeh.mongodb.net/" \
                             "myFirstDatabase?retryWrites=true&w=majority"


class MongodbContextManager:

    def __init__(self):
        self._ca = certifi.where()  # type: ignore
        self.client = MongoClient(mongo_db_url,tlsCAFile=self._ca)
        self._db = self.client.kumoh # type: ignore

    def __enter__(self):
        return self._db

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")