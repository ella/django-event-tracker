from datetime import timedelta

from celery.task import PeriodicTask
from celery.registry import tasks
from carrot.connection import DjangoBrokerConnection
from carrot.messaging import Publisher, Consumer
from pymongo.connection import Connection

from eventtracker.conf import settings
from eventtracker import models 

def _get_carrot_object(klass, **kwargs):
    return klass(
            connection=DjangoBrokerConnection(),
            exchange=settings.EXCHANGE,
            routing_key=settings.ROUTING_KEY,
            exchange_type="topic",
            **kwargs
        )
    
def _close_carrot_object(carobj):
    if carobj:
        try:
            carobj.close()
        except:
            pass
        try:
            carobj.connection.close()
        except:
            pass

def _get_mongo_collection():
    if settings.RIGHT_MONGODB_HOST:
        connection = Connection.paired(
                left=(settings.MONGODB_HOST, settings.MONGODB_PORT),
                right=(settings.RIGHT_MONGODB_HOST, settings.RIGHT_MONGODB_PORT)
            )
    else:
        connection = Connection(host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    return connection[settings.MONGODB_DB][settings.MONGODB_COLLECTION]
    


def track(event, params):
    """
    Dispatch a track event request into the queue
    """
    publisher = _get_carrot_object(Publisher)
    publisher.send((event, params))
    _close_carrot_object(publisher)


def collect_events():
    consumer = None
    collection = None
    try:
        consumer = _get_carrot_object(Consumer, queue=settings.QUEUE)
        collection = _get_mongo_collection()

        for message in consumer.iterqueue():
            e, p = message.decode()
            models.save_event(collection, e, p)
            message.ack()

    finally:
        _close_carrot_object(consumer)
        if collection:
            try:
                collection.connection.close()
            except:
                pass

class ProcessEventsTask(PeriodicTask):
    run_every = timedelta(minutes=settings.TASK_PERIOD)

    def run(self, **kwargs):
        collect_events()

tasks.register(ProcessEventsTask)
