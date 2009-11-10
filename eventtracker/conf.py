from mypage.utils.settings import Settings

MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'events'
MONGODB_COLLECTION = 'events'

ROUTING_KEY = 'events'
EXCHANGE = 'events'
QUEUE = 'events'
TASK_PERIOD = 10

settings = Settings(__name__, 'EVENTS_')
