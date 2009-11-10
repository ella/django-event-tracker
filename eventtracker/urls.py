from django.conf.urls.defaults import *
from eventtracker import views

urlpatterns = patterns('',
    url(r'^([\w-]+)/$', views.track_event, name='eventtracker-track-event'),
)
