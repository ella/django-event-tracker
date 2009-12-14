from datetime import datetime

from django.db import models

def save_event(collection, event, params):
    collection.insert({
        'event': event,
        'timestamp': datetime.now(),
        'params': params
    }) 

class Event(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.SlugField()
    params = models.TextField()
