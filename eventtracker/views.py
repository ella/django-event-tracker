import anyjson

from django.http import HttpResponse, HttpResponseBadRequest

from eventtracker import backend

def track_event(request, event):
    params = request.GET.get('params')
    if params:
        try:
            params = anyjson.deserialize(params)
        except ValueError, e:
            return HttpResponseBadRequest()
    else:
        params = {}

    backend.track(event, params)
    return HttpResponse('OK')

