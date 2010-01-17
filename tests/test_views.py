# -*- coding: utf-8 -*-
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
    

@patch('eventtracker.backend.track')
def test_track_event_calls_track_with_params_from_GET_including_weird_chars(track):
    c = Client()
    url = '/content_link/?params=%7B%22isIcqUser%22%3A%20false%2C%20%22source%22%3A%20%22centrum.cz%22%2C%20%22version%22%3A%20%22none%22%2C%20%22url%22%3A%20%22http%3A%2F%2Faktualne.centrum.cz%2Fdomaci%2Fkauzy%2Fclanek.phtml%3Fid%3D655866%22%2C%20%22widget%22%3A%20%22Aktu%C3%A1ln%C4%9B.cz%22%2C%20%22isAboveFold%22%3A%20true%2C%20%22linksInWidget%22%3A%209%2C%20%22linkPosition%22%3A%200%2C%20%22hasIllustration%22%3A%20true%7D'
    response = c.get(url)
    tools.assert_equals(200, response.status_code)
    tools.assert_true(track.called)
    args, kwargs = track.call_args
    tools.assert_equals(2, len(args))
    tools.assert_equals('content_link', args[0])
    params = args[1]
    tools.assert_equals(u'Aktuálně.cz', params['widget'])
    
