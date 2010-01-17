from time import time
from datetime import datetime
from mock import patch, Mock, sentinel
from nose import tools

from eventtracker.tasks import track, collect_events
from eventtracker.models import save_event

@patch('eventtracker.tasks._get_carrot_object')
def test_track_sends_event(get_carrot_object):
    get_carrot_object.return_value = get_carrot_object
    args = ('event', {'some': 'params'})
    track(*args)
    tools.assert_true(get_carrot_object.send.called)
    cargs, ckwargs = get_carrot_object.send.call_args
    tools.assert_equals(1, len(cargs))
    cargs = cargs[0]
    tools.assert_equals({}, ckwargs)
    tools.assert_equals(args[0], cargs[0])
    tools.assert_true(time() > cargs[1] > time() - 1)
    tools.assert_equals(args[1], cargs[2])


@patch('eventtracker.tasks._get_carrot_object')
@patch('eventtracker.models.get_mongo_collection')
@patch('eventtracker.models.save_event')
def test_collect_events_calls_save_event_for_every_event_in_queue(save_event, get_mongo_collection, get_carrot_object):
    collection = Mock()
    get_mongo_collection.return_value = collection
    t1, t2 = time() - 1, time()
    m1, m2 = Mock(), Mock()
    m1.decode.return_value, m2.decode.return_value = ('event', t1, {'some': 'params'}), ('other_event', t2, {'other': 'params'})

    consumer = Mock()
    get_carrot_object.return_value = consumer

    consumer.iterqueue.return_value = [m1, m2]


    collect_events()

    tools.assert_equals([('decode', (), {}), ('ack', (), {})], m1.method_calls)
    tools.assert_equals([('decode', (), {}), ('ack', (), {})], m2.method_calls)

    tools.assert_equals(1, consumer.iterqueue.call_count)
    tools.assert_equals(2, save_event.call_count)
    tools.assert_equals([
            ((collection, 'event', t1, {'some': 'params'}), {}),
            ((collection, 'other_event', t2, {'other': 'params'}), {})
        ],
        save_event.call_args_list
    )

def test_save_event_inserts_into_collection():
    collection = Mock()
    t = time()
    save_event(collection, sentinel.event, t, sentinel.params)

    tools.assert_equals(1, len(collection.method_calls))
    method, args, kwargs = collection.method_calls[0]
    tools.assert_equals('insert', method)
    tools.assert_equals(1, len(args))
    tools.assert_equals({}, kwargs)
    tools.assert_equals(sentinel.params, args[0]['params'])
    tools.assert_equals(sentinel.event, args[0]['event'])
    tools.assert_equals(datetime.fromtimestamp(t), args[0]['timestamp'])




