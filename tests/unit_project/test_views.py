from django.test.client import Client

from nose import tools
from mock import patch

def test_track_event_returns_400_on_bad_json():
    c = Client()
    response = c.get('/event/', {'params': '{'})
    tools.assert_equals(400, response.status_code)

@patch('eventtracker.backend.track')
def test_track_event_calls_track_with_params_from_GET(track):
    c = Client()
    response = c.get('/event/', {'params': '{"some": "params"}'})
    tools.assert_equals(200, response.status_code)
    tools.assert_true(track.called)
    tools.assert_equals(((u'event', {'some': 'params'}), {}), track.call_args)
    
@patch('eventtracker.backend.track')
def test_track_event_calls_track_with_empty_params_if_no_GET(track):
    c = Client()
    response = c.get('/event/')
    tools.assert_equals(200, response.status_code)
    tools.assert_true(track.called)
    tools.assert_equals(((u'event', {}), {}), track.call_args)
    
