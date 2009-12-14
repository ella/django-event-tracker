import anyjson

from eventtracker.models import Event

def track(event, params):
    Event.objects.create(event=event, params=anyjson.serialize(params))
