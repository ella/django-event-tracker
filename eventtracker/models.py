from datetime import datetime

def save_event(collection, event, params):
    collection.insert({
        'event': event,
        'timestamp': datetime.now(),
        'params': params
    }) 
