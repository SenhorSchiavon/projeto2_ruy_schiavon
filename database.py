from pymongo import MongoClient
import os

def get_database():
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = MongoClient(uri)
    db_name = os.getenv("MONGO_DB", "projeto2_app")
    return client[db_name]
