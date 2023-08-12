from pymongo.errors import ConnectionFailure
from pymongo.errors import ServerSelectionTimeoutError
from pymongo import MongoClient
import os

def initMongoDB():
    mongo = MongoClient(os.environ.get('MONGO_URI', 'mongodb://admin:admin@3.27.142.150:27017/crime_db'))
    users = None
    crime = None
    try:
        users = mongo.db.crime_db.users
        crime = mongo.db.crime_db.crime
    except Exception:
        print("Server not available")
    return {
        "users": users,
        "crime": crime
    }