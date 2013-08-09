import pytz
from django.conf import settings

def timezone (request):
    """Adds the current timezone to the session."""
    return { "timezone" : request.session.get("timezone", settings.TIME_ZONE) }