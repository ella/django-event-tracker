import anyjson

from eventtracker.models import Event

def track(event, params):
    """
    Dummy track event to be used in development only. It will store the events
    in the database.
    """
    Event.objects.create(event=event, params=anyjson.serialize(params))
