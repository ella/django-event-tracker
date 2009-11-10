import anyjson

from django.http import HttpResponse, HttpResponseBadRequest

from eventtracker import tasks

def track_event(request, event):
    params = request.GET.get('params')
    if params:
        try:
            params = anyjson.deserialize(params)
        except ValueError, e:
            return HttpResponseBadRequest()
    else:
        params = {}

    tasks.track(event, params)
    return HttpResponse('OK')

