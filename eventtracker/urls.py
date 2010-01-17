from django.conf.urls.defaults import *
from eventtracker import views

urlpatterns = patterns('',
    url(r'^(?P<event>[\w-]+)/$', views.track_event, name='eventtracker-track-event'),
)
