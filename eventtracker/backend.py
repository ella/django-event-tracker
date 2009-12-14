from eventtracker.conf import settings

__all__ = ['track']

if settings.TRACKER_BACKEND == 'celery':
    from eventtracker.tasks import track
else:
    from eventtracker.dummy import track
