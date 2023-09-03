import os
from mongoengine import connect

def initMongoDB():
    # Extract database name from the URI
    db_name = os.environ.get('MONGO_DB', 'crime_db')
    #
    return connect(
        db=db_name,
        host=os.environ.get('MONGO_URI', 'mongodb://admin:admin@3.27.142.150:27017/crime_db')
    )