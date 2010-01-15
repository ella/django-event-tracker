from datetime import datetime

from pymongo.connection import Connection

from django.db import models

from eventtracker.conf import settings

def get_mongo_collection():
    """
    Open a connection to MongoDB and return the collection to use.
    """
    if settings.RIGHT_MONGODB_HOST:
        connection = Connection.paired(
                left=(settings.MONGODB_HOST, settings.MONGODB_PORT),
                right=(settings.RIGHT_MONGODB_HOST, settings.RIGHT_MONGODB_PORT)
            )
    else:
        connection = Connection(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    return connection[settings.MONGODB_DB][settings.MONGODB_COLLECTION]
    

def save_event(collection, event, timestamp, params):
    "Save the event in MongoDB collection"
    collection.insert({
        'event': event,
        'timestamp': datetime.fromtimestamp(timestamp),
        'params': params
    }) 

class Event(models.Model):
    "Dummy model for development."
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.SlugField()
    params = models.TextField()
