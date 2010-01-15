"""
Default settings for django-event-tracker. You can override any of these by
specifying EVENTS_<CONF_OPTION> in your projects' setting.py.
"""

from django.utils.importlib import import_module
from django.conf import settings

class Settings(object):
    "Simple wrapper around config."
    def __init__(self, module_name, prefix=''):
        self.module = import_module(module_name)
        self.prefix = prefix

    def __getattr__(self, name):
        p_name = ''.join((self.prefix, name))
        if hasattr(settings, p_name):
            return getattr(settings, p_name)
        return getattr(self.module, name)

    def __dir__(self):
        return dir(self.module) + dir(self.settings)


MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

RIGHT_MONGODB_HOST = None
RIGHT_MONGODB_PORT = 27017

MONGODB_DB = 'events'
MONGODB_COLLECTION = 'events'

ROUTING_KEY = 'events'
EXCHANGE = 'events'
QUEUE = 'events'
TASK_PERIOD = 3*60

TRACKER_BACKEND = 'celery'

settings = Settings(__name__, 'EVENTS_')
