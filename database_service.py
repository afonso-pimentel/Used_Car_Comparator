from dotenv import load_dotenv
from pymongo import MongoClient
import os

def connect_db(db_name):

    load_dotenv()
    CONNECTION_STRING = os.getenv("MONGO_STRING")
    client = MongoClient(CONNECTION_STRING)
    return client[db_name]

def write_to_db(client, db_name, collection_name, data):
    db = client[db_name]
    collection = db[collection_name]
    collection.insert_many(data)

def read_from_db(client, db_name, collection_name, pipeline):
    db = client[db_name]
    collection = db[collection_name]
    return collection.aggregate(pipeline)

def find_one(client, db_name, collection_name, query):
    db = client[db_name]
    collection = db[collection_name]
    result = collection.find(query)
    return result